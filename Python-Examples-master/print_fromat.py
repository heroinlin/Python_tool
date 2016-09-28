# -*- coding:utf-8 -*-
"""
根据用户输入的宽度打印格式化的列表
'-'用于左对齐，'*'作为宽度或者精度(或者两个都使用)
"""


def main():
    width = input("Enter the width: ")
    price_width = 10
    item_width = width - price_width
    header_format = "%-*s%*s"
    format = "%-*s%*.2f"
    print('='*width)
    print header_format % (item_width, "Item", price_width, "Price")
    print('-'*width)
    print format % (item_width, "Apple", price_width, 0.4)
    print format % (item_width, "Pear", price_width, 0.5)
    print format % (item_width, "Banana", price_width, 0.6)
    print format % (item_width, "Orange", price_width, 2)
    print format % (item_width, "Lemon", price_width, 12)
    print("="*width)
if __name__ == "__main__":
    main()
