from bs4 import BeautifulSoup, NavigableString
import re
import yaml
from utils.gpt import translate as gpt_translate


class HTMLParser:

    def __init__(self, html=None, path=None, skip_tags=[]):
        
        if path:
            self.path = path
            with open(path, 'r', encoding='utf-8') as file:
                html = file.read()
        else:
            self.path = None
        
            

        self.soup = BeautifulSoup(html, 'html.parser')
        self.html = html
        self.tag_list = []
        self.index = 0
        self.skip_tags = skip_tags
        self.errors = []

    def parse(self):
        tag = self.soup.contents[0]

        for element in tag.next_elements:
            if type(element) is NavigableString and re.search(r'\w', element) and not self._in_skip_tags(element.previous.name, element):
                self.index += 1
                # self.tag_list.append({'tag': element.previous.name,'text': element, 'text_new': text_new})
                self.tag_list.append({'tag': element.previous.name,'text': element, 'index': self.index})

        print("1. parse done")

    def _in_skip_tags(self, tag, text):
        elements = ["<|im_end|>", "<|im_start|>"]
        if any(element in text for element in elements):
            return True

        for skip_tag in self.skip_tags:
            if skip_tag['tag'] == tag:
                if not skip_tag['text'] or skip_tag['text'] == text:
                    return True
        return False


    def _replace(self, tag_name="translation"):
        for tag_info in self.tag_list:
            element = tag_info['text']
            parent = element.parent
            
            if tag_name in tag_info:
                text_new = tag_info[tag_name]
            else:
                self.errors.append({
                    "path": self.path,
                    "tag": tag_info
                })
                print("tag_name not found: ", tag_info)
                continue  # 如果键不存在，跳过当前循环

            if parent and text_new:
                # Check if the element is still part of the parent's contents
                if element in parent.contents:
                    element.replace_with(NavigableString(text_new.strip("'").strip('"')))
        
        print("3. replace done")

    def translate(self):
        filtered_texts = [{"index": item["index"], "text": str(item["text"])} for item in self.tag_list]

        # 将 filtered_texts 数据按 200 一组拆分
        chunk_size = 200
        chunks = [filtered_texts[i:i + chunk_size] for i in range(0, len(filtered_texts), chunk_size)]

        responses = []
        for i, chunk in enumerate(chunks):
            # 转换为 YAML 格式
            yaml_data = yaml.dump(chunk, allow_unicode=True, default_flow_style=False)

            responses.append(gpt_translate(yaml_data))
            print(f"2. translate-{i}: done")

        response = "\n".join(responses)

        # translated_texts = yaml.safe_load(response)

        pattern = re.compile(r'- index: (\d+)\n  translation: (.+)')
        matches = pattern.findall(response)
        translated_texts = [{"index": int(index), "translation": text} for index, text in matches]
        # 将 source_texts 和 translated_texts 通过index 合并
        for source_text in self.tag_list:
            for translated_text in translated_texts:
                if source_text["index"] == translated_text["index"]:
                    source_text["translated"] = translated_text["translation"]

        self._replace(tag_name="translated")
    
    def save(self, file_path):
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(self.soup))
        
        print("4. save done")
        


if __name__ == '__main__':
    content = """
    <!-- Sidebar component -->
    <div>
    <h1>abc</h1><h2>def</h2>
    <!-- Sidebar component -->
    <h1><span>Test2 <strong>Test3</strong></span> Test1<div>Test4</div><h2>Test5</h2></h1>
    <h3>Test6 <b>Test7</b></h3>
    </div>
    """

    file_path1 = '/Users/barry/Code/ipynb/web-translator/docs.sillytavern.app/usage/api-connections/dreamgen/index.html'
    with open(file_path1, 'r', encoding='utf-8') as file:
        content = file.read()


    html_parser = HTMLParser(content)
    html_parser.parse()
    # html_parser.translate()

    for tag in html_parser.tag_list:
        print(tag)

    print(str(html_parser.soup))
