from utils.gpt import translate_content
from utils.markdown_spliter import split_text_v1


def md_translate(content):
    docs = split_text_v1(content.strip())

    translated_sentences = []
    for i, doc in enumerate(docs):
        print(f"Translating document {i + 1} of {len(docs)}")
        translated_text = translate_content(doc)
        translated_sentences.append(translated_text.strip())

    return "\n\n".join(translated_sentences)

#%%
