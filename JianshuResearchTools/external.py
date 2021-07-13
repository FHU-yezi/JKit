import JianshuResearchTools as jrt
import os
import requests
from lxml import etree
from datetime import datetime
import json
import io

#namespace JianshuResearchTools

class ModelNotFoundError(Exception):
    pass

class JVIT:

    def __init__(self) -> None:
        try:
            f = open('D:/ELPATH.txt')
            self.Path = f.read()
            f.close()
        except:
            print('未找到指定文件，读取失败！')
   
    #加载Exe文件路径
    def PathLocation(self,path):
        if path != "":
            self.Path = path
        else:
            print('不接受空参数！')

    #加载模式
    def SetPattern(self,model):
        #Model:User/Article/Island/BeiKeIsland
        if model != 'User' and model != 'Article' and model != 'Island' and model != 'BeikaIsland':
            print(self.model + '不是一个有效的模式！')
        else:
            self.model = model

    #获取网址
    def SetUrl(self,url):
        self.url = url
        if self.model == 'User':
            f = open(self.Path + '\\UserAddress.txt','w')
            f.write(self.url)
            f.close()
            fi = open(self.Path + '\\TabIndex.txt','w')
            fi.write('2')
            fi.close()
        elif self.model == 'Article':
            f = open(self.Path + '\\ArticleAddress.txt','w')
            f.write(self.url)
            f.close()
            fi = open(self.Path + '\\TabIndex.txt','w')
            fi.write('1')
            fi.close()
        elif self.model == 'Island':
            f = open(self.Path + '\\IslandAddress.txt','w')
            f.write(self.url)
            f.close()
            fi = open(self.Path + '\\TabIndex.txt','w')
            fi.write('3')
            fi.close()
        elif self.model == 'BeikeIsland':
            fi = open(self.Path + '\\TabIndex.txt','w')
            fi.write('4')
            fi.close()
        else:
            raise ModelNotFoundError(self.model + "不是一个有效的模式")

    #检查

    def Check(self):
        try:
            print(self.model,self.Path,self.url)
            self.res = 0
        except:
            self.res = -1
    

    #启动
    def Start(self):
        #@Check TODO:使用函数装饰器来写
        if (self.res == -1):
            print('缺少路径或模式或网址！')
        else:
            os.system('start' + self.Path + "\\JVIT_GUI.exe")

class Run():
    def __init__(self,RunArgs) -> None:
        self.model = RunArgs.model
        self.Path = RunArgs.Path

    def Island(self):

        PC_header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        }
        
        Path = self.Path

        #定义未提供的函数
        def GetIslandName(island_url: str) -> str:
            source = requests.get(island_url, headers=PC_header).content.decode()  # TODO: 不知道为什么会出现编码问题
            html_obj = etree.HTML(source)
            result = html_obj.xpath("//div[@class='nickname']/text()")[0]
            result = result.strip()
            return result

        def GetIslandIntroduction(island_url: str) -> str:
            source = requests.get(island_url, headers=PC_header).content.decode()  # TODO: 不知道为什么会出现编码问题
            html_obj = etree.HTML(source)
            result = html_obj.xpath("//div[@class='info']/text()")[0]
            result = result.strip()
            return result


        #打开获取小岛链接的文件
        fi = open(Path + "\\IslandAddress.txt")
        island_address = fi.read()

        #打开写入通道
        f = open(Path + "\\Island.txt",encoding="utf-8")

        #info-1 小岛名称
        island_name = GetIslandName(island_address)
        f.write(island_name)
        f.write(";")

        #info-2 小岛简介
        island_introduction = GetIslandIntroduction(island_address)
        f.write(island_introduction)
        f.write(";")

    def User(self):
         #定义常量
        Path = self.Path
        jianshu_request_header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57",
                          "X-INFINITESCROLL": "true",
                          "X-Requested-With": "XMLHttpRequest"}

        #打开读取网址通道
        address_file = open(Path + "\\UserAddress.txt")
        user_address = address_file.read()
        address_file.close()

        #打开写入通道
        f = open(Path + "\\User.txt","w",encoding = "utf-8")

        #info-1 用户名
        user_name = jrt.user.GetUserName(user_address)
        f.write(user_name)
        f.write(";")

        #info-2 关注数
        user_attention_count = jrt.user.GetUserFollowersCount(user_address)
        f.write(str(user_attention_count))
        f.write(";")

        #info-3 粉丝数
        user_fans_count = jrt.user.GetUserFansCount(user_address)
        f.write(str(user_fans_count))
        f.write(";")

        #info-4 文章数
        user_article_count = jrt.user.GetUserArticlesCount(user_address)
        f.write(str(user_article_count))
        f.write(";")

        #info-5 文章总字数
        user_article_chars_count = jrt.user.GetUserAssetsCount(user_address)
        f.write(str(user_article_chars_count))
        f.write(";")

        #info-6 总点赞数
        user_likes = jrt.user.GetUserLikesCount(user_address)
        f.write(str(user_likes))
        f.write(";")

        #info-7 总资产
        user_shell = jrt.user.GetUserAssetsCount(user_address)
        f.write(str(user_shell))
        f.write(";")

        #info-8 简书钻
        user_c = jrt.user.GetUserFPCount(user_address)
        f.write(str(user_c))
        f.write(";")

        #info-9 简书贝
        user_e = jrt.user.GetUserFTNCount(user_address)
        f.write(str(user_e))
        f.write(";")

        #info-10 徽章个数
        user_b = jrt.user.GetUserBadgesList(user_address)
        user_b_c = len(user_b)
        f.write(str(user_b_c))
        f.write(";")

        #info-11 个人简介
        user_says = jrt.user.GetUserIntroductionText(user_address)
        f.write(user_says)
        f.write(";")

        #info-12 文章列表
        user_article_list = jrt.user.GetUserArticlesInfo(user_address)
        for article in user_article_list:
            f.write(str(article['title']))
            f.write("-")
        f.write(";")
        f.close()

    def SheelIsland(self):
        Path = self.Path
        #打开写入文件通道
        f = open(Path + "\\BeikeIsland.txt","w",encoding="utf-8")

        #info-1 总蕉♂易量
        count_count = jrt.GetBeiKeIslandTotalTradeAmount()
        f.write(str(count_count))
        f.write(";")

        #info-2 总交易笔数
        count_total = jrt.GetBeiKeIslandTotalTradeCount()
        f.write(str(count_total))
        f.write(";")

        #info-3 交易列表
        trade_list = jrt.GetBeiKeIslandTradeList("buy")
        i = 0
        
        #解析交易列表
        for trade in trade_list:
            i += 1
            f.write(str(i))
            f.write("-")
            f.write(str(trade['UserLevel']))
            f.write("-")
            f.write(str(trade['Price']))
            f.write("%")

    def Artical(self):
        Path = self.Path
        jianshu_request_header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57",
                          "X-INFINITESCROLL": "true",
                          "X-Requested-With": "XMLHttpRequest"}

        #定义未提供的函数

        def GetArticleTotalFPCount(article_url: str) -> int:

            request_url = article_url.replace("https://www.jianshu.com/", "https://www.jianshu.com/asimov/")
            source = requests.get(request_url, headers=jianshu_request_header).content
            json_obj = json.loads(source)
            result = json_obj["total_fp_amount"] / 1000
            return result

        def GetArticleMostValuableCommentsCount(article_url: str) -> int:
            request_url = article_url.replace("https://www.jianshu.com/", "https://www.jianshu.com/asimov/")
            source = requests.get(request_url, headers=jianshu_request_header).content
            json_obj = json.loads(source)
            result = json_obj["featured_comments_count"]
            return result

        def GetArticleUpdateTime(article_url: str) -> datetime:
            request_url = article_url.replace("https://www.jianshu.com/", "https://www.jianshu.com/asimov/")
            source = requests.get(request_url, headers=jianshu_request_header).content
            json_obj = json.loads(source)
            result = datetime.fromtimestamp(json_obj["last_updated_at"])
            return result

        def GetArticleDescription(article_url: str) -> str:
            request_url = article_url.replace("https://www.jianshu.com/", "https://www.jianshu.com/asimov/")
            source = requests.get(request_url, headers=jianshu_request_header).content
            json_obj = json.loads(source)
            result = json_obj["description"]
            return result

        #打开读取网址通道
        address_file = open(Path + "\\ArticleAddress.txt")
        article_address = address_file.read()
        address_file.close()

        #打开写入通道
        article_info_file = open(Path + "\\Article.txt","w",encoding="utf-8")

        #info-1 文章标题
        article_title = jrt.article.GetArticleTitle(article_address)
        article_info_file.write(article_title)
        article_info_file.write(";")

        #info-2 文章点赞量
        article_likes = jrt.article.GetArticleLikesCount(article_address)
        article_info_file.write(str(article_likes))
        article_info_file.write(";")

        #info-3 文章获钻量
        article_ifp = GetArticleTotalFPCount(article_address)
        article_info_file.write(str(article_ifp))
        article_info_file.write(";")

        #info-4 文章评论量
        article_says = jrt.article.GetArticleCommentsCount(article_address)
        article_info_file.write(str(article_says))
        article_info_file.write(";")

        #info-5 文章精选评论
        article_value_says = GetArticleMostValuableCommentsCount(article_address)
        article_info_file.write(str(article_value_says))
        article_info_file.write(";")

        #info-6 文章发布时间
        article_time = jrt.GetArticlePublishTime(article_address)
        article_info_file.write(str(article_time))
        article_info_file.write(";")

        #info-7 文章最近更新时间
        article_new_time = GetArticleUpdateTime(article_address)
        article_info_file.write(str(article_new_time))
        article_info_file.write(";")

        #info-8 文章是否收费
        article_payable = jrt.article.GetArticlePaidStatus(article_address)
        if (article_payable):
            article_info_file.write("是")
        else:
            article_info_file.write("否")
        article_info_file.write(";")

        #info-9 文章是否可转载
        article_reprintable = jrt.article.GetArticleReprintStatus(article_address)
        if (article_reprintable):
            article_info_file.write("是")
        else:
            article_info_file.write("否")
        article_info_file.write(";")

        #info-10 文章是否可评论
        article_sayable = jrt.article.GetArticleCommentStatus(article_address)
        if (article_sayable):
            article_info_file.write("是")
        else:
            article_info_file.write("否")
        article_info_file.write(";")

        #info-11 纯文本文章内容
        artical_text = jrt.article.GetArticleText(article_address)
        article_info_file.write(artical_text)
        article_info_file.write(";")

    def IRun(self):
        if (self.model == 'Article'): #文章模式
            Run.Artical(self)
            os.system('cmd.exe start ' + self.Path + '\\JVIT_GUI.exe')
        elif (self.model == 'User'):#用户模式
            Run.User(self)
            os.system('cmd.exe start ' + self.Path + '\\JVIT_GUI.exe')
        elif (self.model == 'Island'): #小岛模式
            Run.Island(self)
            os.system('cmd.exe start ' + self.Path + '\\JVIT_GUI.exe')
        elif (self.model == 'BeiKeIsland'): #贝壳小岛
            Run.SheelIsland(self)
            os.system('cmd.exe start ' + self.Path + '\\JVIT_GUI.exe')
        else:
            raise ModelNotFoundError(self.model + '不是一个有效的模式。')
