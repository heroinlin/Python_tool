# -*- coding: utf-8 -*-
# 字典用于html中的例子
# "%(key)s"%{key:value} 以字符串形式输出字典里key对应的value
template = ''' <html>
    <head><title>%(title)s</title></head>
    <body>
    <h1>%(title)s</h1>
    <p>%(text)s</p>
    </body>'''


def main():
    data = {'title': 'My Home Page', 'text': 'Welcome to my home page!'}
    print (template % data)
    out_html = open("my_home_page.html", 'w')
    out_html.write(template % data)
    out_html.close()
if __name__ == '__main__':
    main()
