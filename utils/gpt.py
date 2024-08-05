import os
import dotenv
from langchain_openai import ChatOpenAI
from portkey_ai import PORTKEY_GATEWAY_URL, createHeaders
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser

dotenv.load_dotenv()


def portkey_llm():
    return portkey_llm_openai()
    # return portkey_llm_openrouter()


def portkey_llm_openrouter(model="openai/gpt-4o-mini", temperature=0.5):
    PORTKEY_API_KEY = os.getenv("PORTKEY_API_KEY")
    OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER_API_KEY")

    headers = createHeaders(provider="openrouter", api_key=PORTKEY_API_KEY)
    base_url = PORTKEY_GATEWAY_URL

    chat = ChatOpenAI(model=model,
                      api_key=OPEN_ROUTER_API_KEY,
                      base_url=base_url,
                      default_headers=headers,
                      temperature=temperature)
    return chat


def portkey_llm_openai(model="gpt-4o-mini", temperature=0.5):
    PORTKEY_API_KEY = os.getenv("PORTKEY_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    congif = {
        "retry": {
            "attempts": 5
        }
    }

    headers = createHeaders(provider="openai", api_key=PORTKEY_API_KEY, congif=congif)
    # base_url = "http://localhost:8787/v1"
    base_url = PORTKEY_GATEWAY_URL

    chat = ChatOpenAI(model=model,
                      api_key=OPENAI_API_KEY,
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
    response = chain.invoke(
        {"yaml": yaml_data, "to": to, "imt_source_field": imt_source_field, "imt_trans_field": imt_trans_field})

    return response


def translate_content(text):
    if not text:
        return ""

    # 初始化OpenAI语言模型
    chat = portkey_llm()
    # chat = llm_loader.open_router_llm()
    # chat = ChatOpenAI(temperature=0.1, model="Qwen/Qwen1.5-72B-Chat",
    #                   base_url="https://api.together.xyz/v1", api_key=TOGETHER_API_KEY)
    # chat = ChatOpenAI(temperature=0.1, model="gpt-3.5-turbo",
    #                   base_url=DEV_GPT_URL, api_key=DEV_GPT_API_KEY)
    # chat = ChatOpenAI(temperature=0)

    template = (
        """You are a professional technical translator and have translated the following Markdown snippet from 
        {input_language} to {output_language}:
1. Professional and technical terms are not translated
2. The translation should be more suitable for the Chinese context
3. Keep all symbols, numbers, and special characters without any changes
4. The content in the code block is not translated
5. Make sure that the content in the code block has not been translated and remains unchanged. 
That is, the content starting and ending with ``` does not need to be translated and remains unchanged.
6. Ensure that the translation format is consistent with the original document, and there must be no new or missing 
format content, such as ```, #, *, -, etc.
7. Do not add any other content or sentences other than the translated content, and do not add any additional content.
8. Don’t have an opening statement or a blank space at the beginning.
    """
    )

    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    # get a chat completion from the formatted messages
    response = chat.invoke(
        chat_prompt.format_prompt(
            input_language="English", output_language="Chinese", text=text
        ).to_messages()
    )

    return response.content
