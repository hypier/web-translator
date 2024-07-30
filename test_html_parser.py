import unittest
from html_parser import HTMLParser

class TestHTMLParser(unittest.TestCase):
    
    user_cases = [
        {
            'desc': "单个标签",
            'html': """
            <h1>Test</h1>
            """,
            'tags': [{
                'tag': 'h1',
                'text': 'Test'
            }],
            'expected': True
        },
        {
            'desc': "多个标签",
            'html': """
            <h1>Test</h1>
            <h2>Test2</h2>
            """,
            'tags': [{
                'tag': 'h1',
                'text': 'Test'
            }, {
                'tag': 'h2',
                'text': 'Test2'
            }],
            'expected': True
        },
        {
            'desc': "嵌套标签-1 文本在前",
            'html': """
            <h1>Test <span>Test2</span></h1>
            """,
            'tags': [{
                'tag': 'h1',
                'text': 'Test <span>Test2</span>'
            }],
            'expected': True
        },
        {
            'desc': "嵌套标签-2 文本在中",
            'html': """
            <h1><span><h2>Test2</h2></span></h1>
            """,
            'tags': [{
                'tag': 'h2',
                'text': 'Test2'
            }],
            'expected': True
        },
        {
            'desc': "嵌套标签-3 文本在后",
            'html': """
            <h1><span>Test2</span> Test</h1>
            """,
            'tags': [{
                'tag': 'h1',
                'text': '<span>Test2</span> Test'
            }],
            'expected': True
        },
        {
            'desc': "多个嵌套标签-1 单行",
            'html': """
            <h1>Test <span>Test2 <strong>Test3</strong></span></h1>
            """,
            'tags': [{
                'tag': 'h1',
                'text': 'Test <span>Test2 <strong>Test3</strong></span>'
            }],
            'expected': True
        },
        {
            'desc': "多个嵌套标签-2 多行",
            'html': """
            <h1>Test <span>Test2 <strong>Test3</strong></span></h1>
            <h2>Test4</h2>
            """,
            'tags': [{
                'tag': 'h1',
                'text': 'Test <span>Test2 <strong>Test3</strong></span>'
            }, {
                'tag': 'h2',
                'text': 'Test4'
            }],
            'expected': True
        },
        {
            'desc': "多个嵌套标签-3 标签嵌套多行",
            'html': """
            <h1><span>Test2 <strong>Test3</strong></span></h1>
            <h2>Test4</h2>
            <h3>Test5</h3>
            """,
            'tags': [{
                'tag': 'span',
                'text': 'Test2 <strong>Test3</strong>'
            }, {
                'tag': 'h2',
                'text': 'Test4'
            }, {
                'tag': 'h3',
                'text': 'Test5'
            }],
            'expected': True
        },
        {
            'desc': "多个嵌套标签-4 文本嵌套多行",
            'html': """
            <h1><span>Test2 <strong>Test3</strong></span> Test1</h1>
            <h2>Test4</h2>
            <h3>Test5</h3>
            """,
            'tags': [{
                'tag': 'span',
                'text': '<span>Test2 <strong>Test3</strong></span> Test1'
            }, {
                'tag': 'h2',
                'text': 'Test4'
            }, {
                'tag': 'h3',
                'text': 'Test5'
            }],
            'expected': True
        },    
        {
            'desc': "多个嵌套标签-5 文本嵌套多行分拆",
            'html': """
            <h1><span>Test2 <strong>Test3</strong></span> Test1<div>Test4</div></h1>
            """,
            'tags': [{
                'tag': 'span',
                'text': '<span>Test2 <strong>Test3</strong></span> Test1'
            }, {
                'tag': 'div',
                'text': 'Test4'
            },],
            'expected': True
        },
        {
            'desc': "多个嵌套标签-6 文本嵌套多行分拆",
            'html': """
            <h1><span>Test2 <strong>Test3</strong></span> Test1<div>Test4</div></h1>
            <h2>Test5</h2>
            """,
            'tags': [{
                'tag': 'span',
                'text': '<span>Test2 <strong>Test3</strong></span> Test1'
            }, {
                'tag': 'div',
                'text': 'Test4'
            }, {
                'tag': 'h2',
                'text': 'Test5'
            }],
            'expected': True
        },
        {
            'desc': "多个嵌套标签-7 文本嵌套多行分拆",
            'html': """
            <h1><span>Test2 <strong>Test3</strong></span> Test1<div>Test4</div><h2>Test5</h2></h1>
            <h3>Test6</h3>
            """,
            'tags': [{
                'tag': 'span',
                'text': '<span>Test2 <strong>Test3</strong></span> Test1'
            }, {
                'tag': 'div',
                'text': 'Test4'
            }, {
                'tag': 'h2',
                'text': 'Test5'
            }, {
                'tag': 'h3',
                'text': 'Test6'
            }],
            'expected': True
        }
        
    ]
    
    def test_parse(self):
        for user_case in self.user_cases:
            html_parser = HTMLParser(user_case['html'])
            html_parser.parse()
            self.assertEqual(html_parser.tag_list, user_case['tags'])