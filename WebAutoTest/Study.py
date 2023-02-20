# ustr = u"中国人"
# def test_value(v):
#     v = 2
#
# value = 1
# test_value(value)
# print(value)
#
#
# def test_ref(v):
#     v['a'] = 'test_ref'
#
# value = {'a': 1}
# test_ref(value)
# print(value)
#
# def demo(*arg, **cms, ***kwargs):
#     print(arg)
#     print(cms)
#     print(kwargs)
#
# demo(12, 3, a='te2' , b=3, c=3)


class CLanguage :
    def __init__(self):
        self.name = "C语言中文网"
        self.add = "http://c.biancheng.net"
    # 下面定义了一个say实例方法
    def say(self):
        self.catalog = 13

clang = CLanguage()
print(clang.name)
print(clang.add)
clang.say()
print(clang.catalog)