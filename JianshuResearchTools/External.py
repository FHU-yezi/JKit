import JianshuResearchTools as jrt
import os

#namespace JianshuResearchTools

class ModelNotFoundError(Exception):
    pass

class JVIT:

    def __init__(self) -> None:
        try:
            f = open('D:/ELPATH.txt')
            self.path = f.read()
            f.close()
        except:
            print('未找到指定文件，读取失败！')
   
    #加载Exe文件路径
    def PathLocation(self,path):
        if path != "":
            self.path = path
        else:
            print('不接受空参数！')

    #加载模式
    def SetPattern(self,model):
        #Model:User/Article/Island/BeiKeIsland
        if model != 'User' and model != 'Article' and model != 'Island' and model != 'BeikaIsland':
            print(self.model + '不是一个有效的模式！')
        else:
            self.model = model

    #获取网址
    def SetUrl(self,url):
        self.url = url
        if self.model == 'User':
            f = open(self.path + '\\UserAddress.txt')
            f.write(self.url)
            f.close()
        elif self.model == 'Article':
            f = open(self.path + '\\ArticleAddress.txt')
            f.write(self.url)
            f.close()
        elif self.model == 'Island':
            f = open(self.path + '\\IslandAddress.txt')
            f.write(self.url)
            f.close()
        elif self.model == 'BeikeIsland':
            pass
        else:
            raise ModelNotFoundError(self.model + "不是一个有效的模式")

    #检查

    def Check(self):
        try:
            print(self.model,self.path,self.url)
            self.res = 0
        except:
            self.res = -1
    

    #启动
    def Start(self):
        #@Check TODO:使用函数装饰器来写
        if (self.res == -1):
            print('缺少路径或模式或网址！')
        else:
            os.system('start' + self.path + "\\JVIT_GUI.exe")
