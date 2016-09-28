# -*- coding: utf-8 -*-

# 简单数据库，电话本示例
# 使用人名作为键的自动，每个人用一字典表示，其键'phone'和'addr'分别表示他们的电话和地址
people = {
    'Alice': {
        'phone': '2341',
        'addr': 'foo drive 23'
    },
    'Beth': {
        'phone': '9102',
        'addr': 'bar street 42'
    },
    'Cecil': {
        'phone': '3158',
        'addr': 'Baz avenue 90'
    }
}


def main():
    # 针对电号码和地址使用的描述性标签，在打印输出时会用到
    labels = {
        'phone': 'phone number',
        'addr': 'address'
    }
    name = raw_input("Name: ")
    # 如果名字是字典里的有效键菜打印信息
    if name in people:
        request = raw_input("Find the phone number or address?(p/a): ")
        # 查找电话号码还是地址？使用正确的键：
        if request == 'p': key = 'phone'
        if request == 'a': key = 'addr'
        print("%s's %s is %s." % (name, labels[key], people[name][key]))
    else:
        print("people not in dictionary!")
if __name__ == '__main__':
        main()
