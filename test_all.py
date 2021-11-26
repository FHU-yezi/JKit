from datetime import datetime

import pytest

import JianshuResearchTools as jrt
from JianshuResearchTools.assert_funcs import *
from JianshuResearchTools.convert import *
from JianshuResearchTools.exceptions import *


class TestArticleModule():
    def test_GetArticleTitle(self):
        assert isinstance(jrt.article.GetArticleTitle("https://www.jianshu.com/p/52698676395f"), str)
        assert jrt.article.GetArticleTitle("https://www.jianshu.com/p/52698676395f") == "科技赋能创作星辰，简书分析工具集 JRT 发布"
        assert jrt.article.GetArticleTitle("https://www.jianshu.com/p/2c2b76a1d0ae") == "你好，简书贝"
        assert jrt.article.GetArticleTitle("https://www.jianshu.com/p/0589bd2ac952") == "【教程】贝壳小岛使用攻略"
        with pytest.raises(ResourceError):
            jrt.article.GetArticleTitle("https://www.jianshu.com/p/1b9ad61ade73")
    
    def test_GetArticleAuthorName(self):
        assert isinstance(jrt.article.GetArticleAuthorName("https://www.jianshu.com/p/52698676395f"), str)
        assert jrt.article.GetArticleAuthorName("https://www.jianshu.com/p/52698676395f") == "初心不变_叶子"
        assert jrt.article.GetArticleAuthorName("https://www.jianshu.com/p/2c2b76a1d0ae") == "简书钻首席小管家"
        assert jrt.article.GetArticleAuthorName("https://www.jianshu.com/p/0589bd2ac952") == "ChinaKingKong"
        with pytest.raises(ResourceError):
            jrt.article.GetArticleAuthorName("https://www.jianshu.com/p/1b9ad61ade73")
            
    def test_GetArticleReadsCount(self):
        assert isinstance(jrt.article.GetArticleReadsCount("https://www.jianshu.com/p/52698676395f"), int)
        assert jrt.article.GetArticleReadsCount("https://www.jianshu.com/p/52698676395f") > 900
        assert jrt.article.GetArticleReadsCount("https://www.jianshu.com/p/2c2b76a1d0ae") > 300000
        assert jrt.article.GetArticleReadsCount("https://www.jianshu.com/p/0589bd2ac952") > 24000
        with pytest.raises(ResourceError):
            jrt.article.GetArticleReadsCount("https://www.jianshu.com/p/1b9ad61ade73")
    
    def test_GetArticleWordage(self):
        assert isinstance(jrt.article.GetArticleWordage("https://www.jianshu.com/p/52698676395f"), int)
        assert jrt.article.GetArticleWordage("https://www.jianshu.com/p/52698676395f") == 1068
        assert jrt.article.GetArticleWordage("https://www.jianshu.com/p/2c2b76a1d0ae") == 321
        assert 700 < jrt.article.GetArticleWordage("https://www.jianshu.com/p/0589bd2ac952") < 1000
        with pytest.raises(ResourceError):
            jrt.article.GetArticleWordage("https://www.jianshu.com/p/1b9ad61ade73")

    def test_GetArticleLikesCount(self):
        assert isinstance(jrt.article.GetArticleLikesCount("https://www.jianshu.com/p/52698676395f"), int)
        assert 300 > jrt.article.GetArticleLikesCount("https://www.jianshu.com/p/52698676395f") > 40
        assert 20000 > jrt.article.GetArticleLikesCount("https://www.jianshu.com/p/2c2b76a1d0ae") > 6200
        assert 1000 > jrt.article.GetArticleLikesCount("https://www.jianshu.com/p/0589bd2ac952") > 330
        with pytest.raises(ResourceError):
            jrt.article.GetArticleLikesCount("https://www.jianshu.com/p/1b9ad61ade73")
    
    def test_GetArticleCommentsCount(self):
        assert isinstance(jrt.article.GetArticleCommentsCount("https://www.jianshu.com/p/52698676395f"), int)
        assert 50 > jrt.article.GetArticleCommentsCount("https://www.jianshu.com/p/52698676395f") >= 13
        assert 500 > jrt.article.GetArticleCommentsCount("https://www.jianshu.com/p/2c2b76a1d0ae") > 350
        assert 200 > jrt.article.GetArticleCommentsCount("https://www.jianshu.com/p/0589bd2ac952") > 40
        with pytest.raises(ResourceError):
            jrt.article.GetArticleCommentsCount("https://www.jianshu.com/p/1b9ad61ade73")
    
    def test_GetArticleMostValuableCommentsCount(self):
        assert isinstance(jrt.article.GetArticleMostValuableCommentsCount("https://www.jianshu.com/p/52698676395f"), int)
        assert 20 > jrt.article.GetArticleMostValuableCommentsCount("https://www.jianshu.com/p/52698676395f") >= 0
        assert 120 > jrt.article.GetArticleMostValuableCommentsCount("https://www.jianshu.com/p/2c2b76a1d0ae") > 90
        assert 20 > jrt.article.GetArticleMostValuableCommentsCount("https://www.jianshu.com/p/0589bd2ac952") >= 0
        with pytest.raises(ResourceError):
            jrt.article.GetArticleMostValuableCommentsCount("https://www.jianshu.com/p/1b9ad61ade73")
    
    def test_GetArticleTotalFPCount(self):
        assert isinstance(jrt.article.GetArticleTotalFPCount("https://www.jianshu.com/p/52698676395f"), float)
        assert 120 > jrt.article.GetArticleTotalFPCount("https://www.jianshu.com/p/52698676395f") >= 80
        assert 1300 > jrt.article.GetArticleTotalFPCount("https://www.jianshu.com/p/2c2b76a1d0ae") > 1000
        assert 250 > jrt.article.GetArticleTotalFPCount("https://www.jianshu.com/p/0589bd2ac952") >= 210
        with pytest.raises(ResourceError):
            jrt.article.GetArticleTotalFPCount("https://www.jianshu.com/p/1b9ad61ade73")
    
    def test_GetArticleDescription(self):
        assert isinstance(jrt.article.GetArticleDescription("https://www.jianshu.com/p/52698676395f"), str)
        assert len(jrt.article.GetArticleDescription("https://www.jianshu.com/p/52698676395f")) == 90
        assert len(jrt.article.GetArticleDescription("https://www.jianshu.com/p/2c2b76a1d0ae")) == 90
        assert len(jrt.article.GetArticleDescription("https://www.jianshu.com/p/0589bd2ac952")) == 90
        with pytest.raises(ResourceError):
            jrt.article.GetArticleDescription("https://www.jianshu.com/p/1b9ad61ade73")
            
    def test_GetArticlePublishTime(self):
        assert isinstance(jrt.article.GetArticlePublishTime("https://www.jianshu.com/p/52698676395f"), datetime)
        assert jrt.article.GetArticlePublishTime("https://www.jianshu.com/p/52698676395f").strftime(r"%Y.%m.%d %H:%M:%S") == "2021.05.01 11:34:19"
        assert jrt.article.GetArticlePublishTime("https://www.jianshu.com/p/2c2b76a1d0ae").strftime(r"%Y.%m.%d %H:%M:%S") == "2018.11.29 17:15:29"
        assert jrt.article.GetArticlePublishTime("https://www.jianshu.com/p/0589bd2ac952").strftime(r"%Y.%m.%d %H:%M:%S") == "2019.09.22 22:04:03"
        with pytest.raises(ResourceError):
            jrt.article.GetArticlePublishTime("https://www.jianshu.com/p/1b9ad61ade73")
    
    def test_GetArticleUpdateTime(self):
        assert isinstance(jrt.article.GetArticleUpdateTime("https://www.jianshu.com/p/52698676395f"), datetime)
        assert jrt.article.GetArticleUpdateTime("https://www.jianshu.com/p/52698676395f") >= datetime.fromisoformat("2021-05-01 11:34:19")
        assert jrt.article.GetArticleUpdateTime("https://www.jianshu.com/p/2c2b76a1d0ae") >= datetime.fromisoformat("2018-11-30 11:34:12")
        assert jrt.article.GetArticleUpdateTime("https://www.jianshu.com/p/0589bd2ac952") >= datetime.fromisoformat("2021-05-29 08:29:44")
        with pytest.raises(ResourceError):
            jrt.article.GetArticleUpdateTime("https://www.jianshu.com/p/1b9ad61ade73")
    
    def test_GetArticlePaidStatus(self):
        assert isinstance(jrt.article.GetArticlePaidStatus("https://www.jianshu.com/p/52698676395f"), bool)
        assert jrt.article.GetArticlePaidStatus("https://www.jianshu.com/p/52698676395f") == False
        assert jrt.article.GetArticlePaidStatus("https://www.jianshu.com/p/2c2b76a1d0ae") == False
        assert jrt.article.GetArticlePaidStatus("https://www.jianshu.com/p/0589bd2ac952") == False
        assert jrt.article.GetArticlePaidStatus("https://www.jianshu.com/p/c653cf1b95ba") == True
        assert jrt.article.GetArticlePaidStatus("https://www.jianshu.com/p/e02dadb3269e") == True
        with pytest.raises(ResourceError):
            jrt.article.GetArticlePaidStatus("https://www.jianshu.com/p/1b9ad61ade73")
            
    def test_GetArticleReprintStatus(self):
        assert isinstance(jrt.article.GetArticleReprintStatus("https://www.jianshu.com/p/52698676395f"), bool)
        assert jrt.article.GetArticleReprintStatus("https://www.jianshu.com/p/52698676395f") == True
        assert jrt.article.GetArticleReprintStatus("https://www.jianshu.com/p/2c2b76a1d0ae") == True
        assert jrt.article.GetArticleReprintStatus("https://www.jianshu.com/p/0589bd2ac952") == True
        assert jrt.article.GetArticleReprintStatus("https://www.jianshu.com/p/8dee5fb8f570") == False
        assert jrt.article.GetArticleReprintStatus("https://www.jianshu.com/p/c653cf1b95ba") == False
        with pytest.raises(ResourceError):
            jrt.article.GetArticleReprintStatus("https://www.jianshu.com/p/1b9ad61ade73")
    
    def test_GetArticleCommentStatus(self):
        assert isinstance(jrt.article.GetArticleCommentStatus("https://www.jianshu.com/p/52698676395f"), bool)
        assert jrt.article.GetArticleCommentStatus("https://www.jianshu.com/p/52698676395f") == True
        assert jrt.article.GetArticleCommentStatus("https://www.jianshu.com/p/2c2b76a1d0ae") == False
        assert jrt.article.GetArticleCommentStatus("https://www.jianshu.com/p/0589bd2ac952") == True
        with pytest.raises(ResourceError):
            jrt.article.GetArticleCommentStatus("https://www.jianshu.com/p/1b9ad61ade73")
    
    def test_GetArticleHtml(self):
        assert isinstance(jrt.article.GetArticleHtml("https://www.jianshu.com/p/52698676395f"), str)
        assert jrt.article.GetArticleHtml("https://www.jianshu.com/p/52698676395f").find("<p>") != -1
        assert jrt.article.GetArticleHtml("https://www.jianshu.com/p/2c2b76a1d0ae").find("<p>") != -1
        assert jrt.article.GetArticleHtml("https://www.jianshu.com/p/0589bd2ac952").find("<p>") != -1
        with pytest.raises(ResourceError):
            jrt.article.GetArticleHtml("https://www.jianshu.com/p/1b9ad61ade73")
            
    def test_GetArticleText(self):
        assert isinstance(jrt.article.GetArticleText("https://www.jianshu.com/p/52698676395f"), str)
        assert jrt.article.GetArticleText("https://www.jianshu.com/p/52698676395f").find("<p>") == -1
        assert jrt.article.GetArticleText("https://www.jianshu.com/p/2c2b76a1d0ae").find("<p>") == -1
        assert jrt.article.GetArticleText("https://www.jianshu.com/p/0589bd2ac952").find("<p>") == -1
        with pytest.raises(ResourceError):
            jrt.article.GetArticleText("https://www.jianshu.com/p/1b9ad61ade73")


class TestAssertFuncsModule():
    def test_AssertString(self):
        assert AssertType("test", str) == None
        assert AssertType("1234567890", str) == None
        assert AssertType("52698676395f", str) == None
        with pytest.raises(TypeError):
            assert AssertType(1234567890, str) == None
        with pytest.raises(TypeError):
            assert AssertType(100.0, str) == None
            
    def test_AssertInt(self):
        assert AssertType(1234567890, int) == None
        assert AssertType(0, int) == None
        assert AssertType(-1, int) == None
        with pytest.raises(TypeError):
            assert AssertType("1234567890", int) == None
        with pytest.raises(TypeError):
            assert AssertType("test", int) == None
            
    def test_AssertFloat(self):
        assert AssertType(1234567890.0, float) == None
        assert AssertType(0.0, float) == None
        assert AssertType(-1.0, float) == None
        with pytest.raises(TypeError):
            assert AssertType("1234567890", float) == None
        with pytest.raises(TypeError):
            assert AssertType(1234567890, float) == None
    
    def test_AssertJianshuUrl(self):
        assert AssertJianshuUrl("https://www.jianshu.com") == None
        assert AssertJianshuUrl("https://www.jianshu.com/u/ea36c8d8aa30") == None
        assert AssertJianshuUrl("https://www.jianshu.com/p/52698676395f") == None
        assert AssertJianshuUrl("https://www.jianshu.com/nb/40458256") == None
        assert AssertJianshuUrl("https://www.jianshu.com/c/7ecac177f5a8") == None
        assert AssertJianshuUrl("https://www.jianshu.com/g/6187f99def472f5e") == None
        assert AssertJianshuUrl("https://www.jianshu.com/asimov/users/slug/ea36c8d8aa30") == None
        with pytest.raises(InputError):
            assert AssertJianshuUrl("https://www.baidu.com") == None
        with pytest.raises(InputError):
            assert AssertJianshuUrl("http://www.jianshu.com") == None
        with pytest.raises(InputError):
            assert AssertJianshuUrl("www.jianshu.com") == None
    
    def test_AssertUserUrl(self):
        assert AssertUserUrl("https://www.jianshu.com/u/ea36c8d8aa30") == None
        assert AssertUserUrl("https://www.jianshu.com/u/c5a2ce84f60b") == None
        with pytest.raises(InputError):
            assert AssertUserUrl("https://www.jianshu.com") == None
        with pytest.raises(InputError):
            assert AssertUserUrl("https://www.jianshu.com/p/52698676395f") == None
        with pytest.raises(InputError):
            assert AssertUserUrl("https://www.jianshu.com/nb/40458256") == None
        with pytest.raises(InputError):
            assert AssertUserUrl("https://www.jianshu.com/c/7ecac177f5a8") == None
        with pytest.raises(InputError):
            assert AssertUserUrl("https://www.jianshu.com/g/6187f99def472f5e") == None
    
    def test_AssertArticleUrl(self):
        assert AssertArticleUrl("https://www.jianshu.com/p/52698676395f") == None
        assert AssertArticleUrl("https://www.jianshu.com/p/2c2b76a1d0ae") == None
        with pytest.raises(InputError):
            assert AssertArticleUrl("https://www.jianshu.com") == None
        with pytest.raises(InputError):
            assert AssertArticleUrl("https://www.jianshu.com/u/ea36c8d8aa30") == None
        with pytest.raises(InputError):
            assert AssertArticleUrl("https://www.jianshu.com/nb/40458256") == None
        with pytest.raises(InputError):
            assert AssertArticleUrl("https://www.jianshu.com/c/7ecac177f5a8") == None
        with pytest.raises(InputError):
            assert AssertArticleUrl("https://www.jianshu.com/g/6187f99def472f5e") == None
    
    def test_AssertArticleStatusNormal(self):
        assert AssertArticleStatusNormal("https://www.jianshu.com/p/52698676395f") == None
        assert AssertArticleStatusNormal("https://www.jianshu.com/p/2c2b76a1d0ae") == None
        with pytest.raises(InputError):
            assert AssertArticleStatusNormal("https://www.jianshu.com") == None
        with pytest.raises(InputError):
            assert AssertArticleStatusNormal("https://www.jianshu.com/u/ea36c8d8aa30") == None
        with pytest.raises(InputError):
            assert AssertArticleStatusNormal("https://www.jianshu.com/nb/40458256") == None
        with pytest.raises(InputError):
            assert AssertArticleStatusNormal("https://www.jianshu.com/c/7ecac177f5a8") == None
        with pytest.raises(InputError):
            assert AssertArticleStatusNormal("https://www.jianshu.com/g/6187f99def472f5e") == None
        with pytest.raises(ResourceError):
            assert AssertArticleStatusNormal("https://www.jianshu.com/p/d3f393b2eddd") == None
    
    def test_AssertNotebookUrl(self):
        assert AssertNotebookUrl("https://www.jianshu.com/nb/40458256") == None
        assert AssertNotebookUrl("https://www.jianshu.com/nb/40899491") == None
        with pytest.raises(InputError):
            assert AssertNotebookUrl("https://www.jianshu.com") == None
        with pytest.raises(InputError):
            assert AssertNotebookUrl("https://www.jianshu.com/u/ea36c8d8aa30") == None
        with pytest.raises(InputError):
            assert AssertNotebookUrl("https://www.jianshu.com/c/c022c24c31a5") == None
        with pytest.raises(InputError):
            assert AssertNotebookUrl("https://www.jianshu.com/p/52698676395f") == None
        with pytest.raises(InputError):
            assert AssertNotebookUrl("https://www.jianshu.com/g/6187f99def472f5e") == None
    
    def test_AssertCollectionUrl(self):
        assert AssertCollectionUrl("https://www.jianshu.com/c/7ecac177f5a8") == None
        assert AssertCollectionUrl("https://www.jianshu.com/c/c022c24c31a5") == None
        with pytest.raises(InputError):
            assert AssertCollectionUrl("https://www.jianshu.com") == None
        with pytest.raises(InputError):
            assert AssertCollectionUrl("https://www.jianshu.com/u/ea36c8d8aa30") == None
        with pytest.raises(InputError):
            assert AssertCollectionUrl("https://www.jianshu.com/nb/40899491") == None
        with pytest.raises(InputError):
            assert AssertCollectionUrl("https://www.jianshu.com/p/52698676395f") == None
        with pytest.raises(InputError):
            assert AssertCollectionUrl("https://www.jianshu.com/g/6187f99def472f5e") == None
    
    def test_AssertIslandUrl(self):
        assert AssertIslandUrl("https://www.jianshu.com/g/6187f99def472f5e") == None
        assert AssertIslandUrl("https://www.jianshu.com/g/c921f9f70f1af261") == None
        with pytest.raises(InputError):
            assert AssertIslandUrl("https://www.jianshu.com") == None
        with pytest.raises(InputError):
            assert AssertIslandUrl("https://www.jianshu.com/u/ea36c8d8aa30") == None
        with pytest.raises(InputError):
            assert AssertIslandUrl("https://www.jianshu.com/nb/40899491") == None
        with pytest.raises(InputError):
            assert AssertIslandUrl("https://www.jianshu.com/p/52698676395f") == None
        with pytest.raises(InputError):
            assert AssertIslandUrl("https://www.jianshu.com/c/7ecac177f5a8") == None


class TestBeikeIslandModule():
    def test_GetBeikeIslandTotalTradeAmount(self):
        assert isinstance(jrt.beikeisland.GetBeikeIslandTotalTradeAmount(), int)
        assert 170000000 < jrt.beikeisland.GetBeikeIslandTotalTradeAmount() < 250000000
        
    def test_GetBeikeIslandTotalTradeCount(self):
        assert isinstance(jrt.beikeisland.GetBeikeIslandTotalTradeCount(), int)
        assert 40000 < jrt.beikeisland.GetBeikeIslandTotalTradeCount() < 80000
    
    def test_GetBeikeIslandTotalTradeRankData(self):
        assert isinstance(jrt.beikeisland.GetBeikeIslandTotalTradeRankData(), list)
        assert isinstance(jrt.beikeisland.GetBeikeIslandTotalTradeRankData(2), list)
        assert isinstance(jrt.beikeisland.GetBeikeIslandTotalTradeRankData(page=3), list)
        for item in jrt.beikeisland.GetBeikeIslandTotalTradeRankData():
            assert len(item) != 0
    
    def test_GetBeikeIslandBuyTradeRankData(self):
        assert isinstance(jrt.beikeisland.GetBeikeIslandBuyTradeRankData(), list)
        assert isinstance(jrt.beikeisland.GetBeikeIslandBuyTradeRankData(2), list)
        assert isinstance(jrt.beikeisland.GetBeikeIslandBuyTradeRankData(page=3), list)
        for item in jrt.beikeisland.GetBeikeIslandBuyTradeRankData():
            assert len(item) != 0
    
    def test_GetBeikeIslandSellTradeRankData(self):
        assert isinstance(jrt.beikeisland.GetBeikeIslandSellTradeRankData(), list)
        assert isinstance(jrt.beikeisland.GetBeikeIslandSellTradeRankData(2), list)
        assert isinstance(jrt.beikeisland.GetBeikeIslandSellTradeRankData(page=3), list)
        for item in jrt.beikeisland.GetBeikeIslandSellTradeRankData():
            assert len(item) != 0
    
    def test_GetBeikeIslandTradeOrderInfo(self):
        assert isinstance(jrt.beikeisland.GetBeikeIslandTradeOrderInfo(trade_type="buy"), list)
        assert isinstance(jrt.beikeisland.GetBeikeIslandTradeOrderInfo(trade_type="sell"), list)
        with pytest.raises(TypeError):
            jrt.beikeisland.GetBeikeIslandTradeOrderInfo()
        for item in jrt.beikeisland.GetBeikeIslandTradeOrderInfo(trade_type="buy"):
            assert len(item) != 0
        for item in jrt.beikeisland.GetBeikeIslandTradeOrderInfo(trade_type="sell"):
            assert len(item) != 0
    
    def test_GetBeikeIslandTradePrice(self):
        assert isinstance(jrt.beikeisland.GetBeikeIslandTradePrice(trade_type="buy"), float)
        assert isinstance(jrt.beikeisland.GetBeikeIslandTradePrice(trade_type="sell"), float)
        assert 0.03 < jrt.beikeisland.GetBeikeIslandTradePrice(trade_type="buy") < 1
        assert 0.03 < jrt.beikeisland.GetBeikeIslandTradePrice(trade_type="sell") < 1
        assert abs(jrt.beikeisland.GetBeikeIslandTradePrice(trade_type="buy") - \
                   jrt.beikeisland.GetBeikeIslandTradePrice(trade_type="sell")) < 0.3
        with pytest.raises(ResourceError):
            jrt.beikeisland.GetBeikeIslandTradePrice(trade_type="buy", rank=10000)
        with pytest.raises(ResourceError):
            jrt.beikeisland.GetBeikeIslandTradePrice(trade_type="sell", rank=10000)


class TestCollectionModule():
    def test_GetCollectionName(self):
        assert isinstance(jrt.collection.GetCollectionName("https://www.jianshu.com/c/7ecac177f5a8"), str)
        assert jrt.collection.GetCollectionName("https://www.jianshu.com/c/7ecac177f5a8")
        assert jrt.collection.GetCollectionName("https://www.jianshu.com/c/c022c24c31a5")
    
    def test_GetCollectionAvatarUrl(self):
        assert isinstance(jrt.collection.GetCollectionAvatarUrl("https://www.jianshu.com/c/7ecac177f5a8"), str)
        assert jrt.collection.GetCollectionAvatarUrl("https://www.jianshu.com/c/7ecac177f5a8") != ""
        assert jrt.collection.GetCollectionAvatarUrl("https://www.jianshu.com/c/c022c24c31a5") != ""
    
    def test_GetCollectionIntroductionText(self):
        assert isinstance(jrt.collection.GetCollectionIntroductionText("https://www.jianshu.com/c/7ecac177f5a8"), str)
        assert jrt.collection.GetCollectionIntroductionText("https://www.jianshu.com/c/7ecac177f5a8").find("<p>") == -1
        assert jrt.collection.GetCollectionIntroductionText("https://www.jianshu.com/c/c022c24c31a5").find("<p>") == -1
    
    def test_GetCollectionIntroductionHtml(self):
        assert isinstance(jrt.collection.GetCollectionIntroductionHtml("https://www.jianshu.com/c/7ecac177f5a8"), str)
        assert jrt.collection.GetCollectionIntroductionHtml("https://www.jianshu.com/c/7ecac177f5a8").find("<p>") != -1
        assert jrt.collection.GetCollectionIntroductionHtml("https://www.jianshu.com/c/c022c24c31a5").find("<p>") != -1
    
    def test_GetCollectionArticlesCount(self):
        assert isinstance(jrt.collection.GetCollectionArticlesCount("https://www.jianshu.com/c/7ecac177f5a8"), int)
        assert 1700000 > jrt.collection.GetCollectionArticlesCount("https://www.jianshu.com/c/7ecac177f5a8") > 1000000
        assert 5000 > jrt.collection.GetCollectionArticlesCount("https://www.jianshu.com/c/c022c24c31a5") > 50
    
    def test_GetCollectionSubscribersCount(self):
        assert isinstance(jrt.collection.GetCollectionSubscribersCount("https://www.jianshu.com/c/7ecac177f5a8"), int)
        assert 70000 > jrt.collection.GetCollectionSubscribersCount("https://www.jianshu.com/c/7ecac177f5a8") > 30000
        assert 5000 > jrt.collection.GetCollectionSubscribersCount("https://www.jianshu.com/c/c022c24c31a5") > 50
    
    def test_GetCollectionArticlesUpdateTime(self):
        assert jrt.collection.GetCollectionArticlesUpdateTime("https://www.jianshu.com/c/7ecac177f5a8") > datetime.fromisoformat("2021-06-20 00:00:00")
        assert jrt.collection.GetCollectionArticlesUpdateTime("https://www.jianshu.com/c/c022c24c31a5") > datetime.fromisoformat("2021-06-20 00:00:00")
    
    def test_GetCollectionInfoUpdateTime(self):
        assert jrt.collection.GetCollectionArticlesUpdateTime("https://www.jianshu.com/c/7ecac177f5a8") > datetime.fromisoformat("2019-09-10 00:00:00")
        assert jrt.collection.GetCollectionArticlesUpdateTime("https://www.jianshu.com/c/c022c24c31a5") > datetime.fromisoformat("2021-06-01 00:00:00")
    
    def test_GetCollectionOwnerInfo(self):
        assert isinstance(jrt.collection.GetCollectionOwnerInfo("https://www.jianshu.com/c/7ecac177f5a8"), dict)
        for item in jrt.collection.GetCollectionOwnerInfo("https://www.jianshu.com/c/7ecac177f5a8"):
            assert item != None
        for item in jrt.collection.GetCollectionOwnerInfo("https://www.jianshu.com/c/c022c24c31a5"):
            assert item != None
    
    def test_GetCollectionEditorsInfo(self):
        assert isinstance(jrt.collection.GetCollectionEditorsInfo(1686183), list)
        for item in jrt.collection.GetCollectionEditorsInfo(1686183):
            assert any(item.values()) == True
        for item in jrt.collection.GetCollectionEditorsInfo(1950955):
            assert any(item.values()) == True
        with pytest.raises(TypeError):
            jrt.collection.GetCollectionEditorsInfo()
    
    def test_GetCollectionRecommendedWritersInfo(self):
        assert isinstance(jrt.collection.GetCollectionRecommendedWritersInfo(1686183), list)
        for item in jrt.collection.GetCollectionRecommendedWritersInfo(1686183):
            assert any(item.values()) == True
        for item in jrt.collection.GetCollectionRecommendedWritersInfo(1950955):
            assert any(item.values()) == True
        with pytest.raises(TypeError):
            jrt.collection.GetCollectionRecommendedWritersInfo()
    
    def test_GetCollectionSubscribersInfo(self):
        assert isinstance(jrt.collection.GetCollectionSubscribersInfo(1686183), list)
        for item in jrt.collection.GetCollectionSubscribersInfo(1686183):
            assert any(item.values()) == True
        for item in jrt.collection.GetCollectionSubscribersInfo(1950955):
            assert any(item.values()) == True
        with pytest.raises(TypeError):
            jrt.collection.GetCollectionSubscribersInfo()
    
    def test_GetCollectionArticlesInfo(self):
        assert isinstance(jrt.collection.GetCollectionArticlesInfo("https://www.jianshu.com/c/7ecac177f5a8"), list)
        for item in jrt.collection.GetCollectionArticlesInfo("https://www.jianshu.com/c/7ecac177f5a8"):
            assert any(item.values()) == True
        for item in jrt.collection.GetCollectionArticlesInfo("https://www.jianshu.com/c/c022c24c31a5"):
            assert any(item.values()) == True
        with pytest.raises(TypeError):
            jrt.collection.GetCollectionArticlesInfo()


class TestConvertModule():
    def test_UserUrlToUserId(self):
        assert isinstance(UserUrlToUserId("https://www.jianshu.com/u/ea36c8d8aa30"), int)
        assert UserUrlToUserId("https://www.jianshu.com/u/ea36c8d8aa30") == 19867175
        assert UserUrlToUserId("https://www.jianshu.com/u/43c3a5c5aca3") == 17162710
        assert UserUrlToUserId("https://www.jianshu.com/u/c5a2ce84f60b") == 14715425
    
    def test_UserSlugToUserId(self):
        assert isinstance(UserSlugToUserId("ea36c8d8aa30"), int)
        assert UserSlugToUserId("ea36c8d8aa30") == 19867175
        assert UserSlugToUserId("43c3a5c5aca3") == 17162710
        assert UserSlugToUserId("c5a2ce84f60b") == 14715425

    def test_UserUrlToUserSlug(self):
        assert isinstance(UserUrlToUserSlug("https://www.jianshu.com/u/ea36c8d8aa30"), str)
        assert UserUrlToUserSlug("https://www.jianshu.com/u/ea36c8d8aa30") == "ea36c8d8aa30"
        assert UserUrlToUserSlug("https://www.jianshu.com/u/43c3a5c5aca3") == "43c3a5c5aca3"
        assert UserUrlToUserSlug("https://www.jianshu.com/u/c5a2ce84f60b") == "c5a2ce84f60b"
    
    def test_UserSlugToUserUrl(self):
        assert isinstance(UserSlugToUserUrl("https://www.jianshu.com/u/ea36c8d8aa30"), str)
        assert UserSlugToUserUrl("ea36c8d8aa30") == "https://www.jianshu.com/u/ea36c8d8aa30"
        assert UserSlugToUserUrl("43c3a5c5aca3") == "https://www.jianshu.com/u/43c3a5c5aca3"
        assert UserSlugToUserUrl("c5a2ce84f60b") == "https://www.jianshu.com/u/c5a2ce84f60b"
    
    
    def test_ArticleUrlToArticleSlug(self):
        assert isinstance(ArticleUrlToArticleSlug("https://www.jianshu.com/p/52698676395f"), str)
        assert ArticleUrlToArticleSlug("https://www.jianshu.com/p/52698676395f") == "52698676395f"
        assert ArticleUrlToArticleSlug("https://www.jianshu.com/p/2c2b76a1d0ae") == "2c2b76a1d0ae"
        assert ArticleUrlToArticleSlug("https://www.jianshu.com/p/0589bd2ac952") == "0589bd2ac952"
    
    def test_ArticleSlugToArticleUrl(self):
        assert isinstance(ArticleSlugToArticleUrl("52698676395f"), str)
        assert ArticleSlugToArticleUrl("52698676395f") == "https://www.jianshu.com/p/52698676395f"
        assert ArticleSlugToArticleUrl("2c2b76a1d0ae") == "https://www.jianshu.com/p/2c2b76a1d0ae"
        assert ArticleSlugToArticleUrl("0589bd2ac952") == "https://www.jianshu.com/p/0589bd2ac952"
    
    def test_ArticleSlugToArticleId(self):
        assert isinstance(ArticleSlugToArticleId("52698676395f"), int)
        assert ArticleSlugToArticleId("52698676395f") == 87256893
        assert ArticleSlugToArticleId("2c2b76a1d0ae") == 37330600
        assert ArticleSlugToArticleId("0589bd2ac952") == 54170136
        
    def test_NotebookUrlToNotebookId(self):
        assert isinstance(NotebookUrlToNotebookId("https://www.jianshu.com/nb/40458256"), int)
        assert NotebookUrlToNotebookId("https://www.jianshu.com/nb/40458256") == 40458256
        assert NotebookUrlToNotebookId("https://www.jianshu.com/nb/40899491") == 40899491
        
    def test_NotebookUrlToNotebookSlug(self):
        assert isinstance(NotebookUrlToNotebookSlug("https://www.jianshu.com/nb/40458256"), str)
        assert NotebookUrlToNotebookSlug("https://www.jianshu.com/nb/40458256") == "40458256"
        assert NotebookUrlToNotebookSlug("https://www.jianshu.com/nb/40899491") == "40899491"
    
    def test_NotebookSlugToNotebookUrl(self):
        assert isinstance(NotebookSlugToNotebookUrl("https://www.jianshu.com/nb/40458256"), str)
        assert NotebookSlugToNotebookUrl("40458256") == "https://www.jianshu.com/nb/40458256"
        assert NotebookSlugToNotebookUrl("40899491") == "https://www.jianshu.com/nb/40899491"
    
    def test_CollectionUrlToCollectionSlug(self):
        assert isinstance(CollectionUrlToCollectionSlug("https://www.jianshu.com/c/7ecac177f5a8"), str)
        assert CollectionUrlToCollectionSlug("https://www.jianshu.com/c/7ecac177f5a8") == "7ecac177f5a8"
        assert CollectionUrlToCollectionSlug("https://www.jianshu.com/c/c022c24c31a5") == "c022c24c31a5"
    
    def test_CollectionSlugToCollectionUrl(self):
        assert isinstance(CollectionSlugToCollectionUrl("https://www.jianshu.com/c/7ecac177f5a8"), str)
        assert CollectionSlugToCollectionUrl("7ecac177f5a8") == "https://www.jianshu.com/c/7ecac177f5a8"
        assert CollectionSlugToCollectionUrl("c022c24c31a5") == "https://www.jianshu.com/c/c022c24c31a5"

    def test_IslandUrlToIslandSlug(self):
        assert isinstance(IslandUrlToIslandSlug("https://www.jianshu.com/g/6187f99def472f5e"), str)
        assert IslandUrlToIslandSlug("https://www.jianshu.com/g/6187f99def472f5e") == "6187f99def472f5e"
        assert IslandUrlToIslandSlug("https://www.jianshu.com/g/c921f9f70f1af261") == "c921f9f70f1af261"
    
    def test_IslandSlugToIslandUrl(self):
        assert isinstance(IslandSlugToIslandUrl("https://www.jianshu.com/g/6187f99def472f5e"), str)
        assert IslandSlugToIslandUrl("6187f99def472f5e") == "https://www.jianshu.com/g/6187f99def472f5e"
        assert IslandSlugToIslandUrl("c921f9f70f1af261") == "https://www.jianshu.com/g/c921f9f70f1af261"
        
    # TODO: 完成关于 Url Scheme 的测试