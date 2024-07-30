from bs4 import BeautifulSoup, NavigableString, Tag
import re


class HTMLParser:

    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')
        self.html = html
        self.tag_list = []
        self.index = 0

    def parse(self):
        tag = self.soup.contents[0]

        for element in tag.next_elements:
            if type(element) == NavigableString and re.search(r'\w', element):
                self.index = self.index + 1
                text_new = f"{element}-{self.index}"

                if isinstance(element.previous, Tag):
                    self.tag_list.append({'tag': element.previous, 'text': element, 'text_new': text_new})
                elif isinstance(element.previous, NavigableString):
                    self.tag_list.append({'tag': element.previous, 'text': element, 'text_new': text_new})
                

    def replace(self):
        for tag_info in self.tag_list:
            tag = tag_info['tag']
            text = tag_info['text']
            text_new = tag_info['text_new']

            if isinstance(tag, Tag):
                if tag.string and text in tag.string:
                    new_string = tag.string.replace(text, text_new)
                    tag.string.replace_with(NavigableString(new_string))
                else:
                    self.get_text(tag, text, text_new)
            elif isinstance(tag, NavigableString):
                parent = tag.parent
                if parent and tag in parent.contents:
                    tag.replace_with(NavigableString(text_new))

    def get_text(self, tag, text, text_new):
        if tag.next:
            if tag.next.string == text:
                tag.next.string.replace_with(NavigableString(text_new))
            else:
                self.get_text(tag.next, text, text_new)


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

    # file_path = './docs.sillytavern.app/index.html'
    # file_path1 = './docs.sillytavern.app/index.html'

    # with open(file_path1, 'r', encoding='utf-8') as file:
    #     content = file.read()

    html_parser = HTMLParser(content)
    html_parser.parse()
    html_parser.replace()

    for tag in html_parser.tag_list:
        print(tag)

    print(str(html_parser.soup))
