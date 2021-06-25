from time import sleep
class test():
    def __init__(self):
        pass
    def __getattribute__(self, item):
        super(self.__getattribute__)
        itemdict = {
            "Name": "Daming", 
            "sex": "male"
        }
        try:
            print("获取中......")
            sleep(0.3)
            result = itemdict[item]
            print("self." + item + " = '" + result + "'")
            exec("self." + item + " = '" + result + "'")
            return result
        except KeyError:
            print("没有该属性！")

person = test()
print(person.Name)
print(person.Name)
print(person.Name)
print(person.sex)
print(person.girlfriend)
