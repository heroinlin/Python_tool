# -*- coding: utf-8 -*-
"""
检查用户名和PIN码,用于登录
"""


def _init_(self):
    self.data = []


# 在self后添加一user
def add_user(self, name, password):
    # 添加一项
    self.append([name, password])

    # 添加多项
    # self.extend([[name, password], [name, password]])

    # self += [[name, password]]


def del_user(self, name, password):
    # 返回[name,password]在self中的索引
    index = self.index([name, password])
    del self[index]


def main():
    database = [['Jack', '1587'], ['Rose', '1698'], ['Jame', '1326'], ['House', '6688']]
    num = raw_input("Enter to sign in or sign up(1 or 2).\n\
    sign in please input number '1',\n\
    sign up please input number '2',\n\
    delete the user please input number '3':\n")
    if '1'in num:
        name = raw_input("Enter the name: ")
        password = raw_input("Enter the PIN code:")
        if [name, password] in database:
            print("Login success! Hello " + name)
        else:
            print("Name is not exist or password is wrong !")
    elif '2' in num:
        name = raw_input("Enter the name: ")
        password = raw_input("Enter the PIN code:")
        add_user(database, name, password)
        print("Hello, " + name + "! Welcome to join!")
    elif '3' in num:
        name = raw_input("Enter the name: ")
        password = raw_input("Enter the PIN code:")
        if [name, password] in database:
            del_user(database, name, password)
            print("Delete success! " + name + " has remove the database!")
        else:
            print("Delete error!Name is not exist or password is wrong !")
    else:
        print("Input error!Please enter 1 or 2 or 3!")
    print(database)

if __name__ == "__main__":
    main()

