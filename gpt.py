import os
import dotenv
from langchain_openai import ChatOpenAI
from portkey_ai import PORTKEY_GATEWAY_URL, createHeaders
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

dotenv.load_dotenv()


def portkey_llm(model="openai/gpt-4o-mini", temperature=0.5):
    PORTKEY_API_KEY = os.getenv("PORTKEY_API_KEY")
    OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER_API_KEY")
    OPEN_ROUTER_URL = os.getenv("OPEN_ROUTER_URL")

    headers = createHeaders(provider="openrouter", api_key=PORTKEY_API_KEY)
    # base_url = "http://localhost:8787/v1"
    # base_url = OPEN_ROUTER_URL
    base_url = PORTKEY_GATEWAY_URL
    # print(headers)

    chat = ChatOpenAI(model=model,
                      api_key=OPEN_ROUTER_API_KEY,
                      base_url=base_url,
                      default_headers=headers,
                      temperature=temperature)
    return chat


def translate(yaml_data, to="chinese", imt_source_field="text", imt_trans_field="translation"):

    system_template = """
    You will be given a YAML formatted input containing entries with "index" and "{imt_source_field}" fields. 

    For each entry in the YAML, translate the contents of the "{imt_source_field}" field into {to}. Write the translation back into the "{imt_trans_field}" field for that entry.

    Here is an example of the expected format:

    <example>
    Input:
    - index: 1
        {imt_source_field}: Source
    Output:
    - index: 1
        {imt_trans_field}: Translation
    </example>

    Please return the translated YAML directly without wrapping <yaml> tag or include any additional information.
    """

    user_template = """
    Here is the input:

    <yaml>
    {yaml}
    </yaml>
    """

    prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_template), ("user", user_template)]
    )

    parser = StrOutputParser()
    chain = prompt_template | portkey_llm() | parser
    response = chain.invoke({"yaml": yaml_data, "to": to, "imt_source_field": imt_source_field, "imt_trans_field": imt_trans_field})

    return response
