import unittest
from time import sleep

import JianshuResearchTools as jrt

class TestBasic(unittest.TestCase):
    def testUA(self):
        self.assertTrue(jrt.UA['User-Agent'])
    def testMobileUA(self):
        self.assertTrue(jrt.Mobile_UA["User-Agent"])
    def testRequestUA(self):
        self.assertTrue(jrt.request_UA["User-Agent"])
        self.assertTrue(jrt.request_UA["X-INFINITESCROLL"])
        self.assertTrue(jrt.request_UA["X-Requested-With"])
    def testBeiKeIslandHeaders(self):
        self.assertTrue(jrt.BeiKeIslandHeaders["Host"])
        self.assertTrue(jrt.BeiKeIslandHeaders["User-Agent"])
        self.assertTrue(jrt.BeiKeIslandHeaders["Content-Type"])
        self.assertTrue(jrt.BeiKeIslandHeaders["Version"])
        self.assertEqual(jrt.BeiKeIslandHeaders["Host"],"www.beikeisland.com")
        self.assertEqual(jrt.BeiKeIslandHeaders["Content-Type"],"application/json")
        self.assertEqual(jrt.BeiKeIslandHeaders["Version"],"v2.0")
    def testParser(self):
        self.assertEqual(jrt.parser,"html.parser")
    def testAssertUserURL(self):
        self.assertTrue(jrt.AssertUserURL("https://www.jianshu.com/u/ea36c8d8aa30"))
        self.assertTrue(jrt.AssertUserURL("https://www.jianshu.com/u/0f438ff0a55f?utm_source=desktop&utm_medium=index-users"))
        self.assertFalse(jrt.AssertUserURL("https://www.jianshu.com/"))
        self.assertFalse(jrt.AssertUserURL("https://www.baidu.com/"))
        self.assertFalse(jrt.AssertUserURL("https://www.jianshu.com/p/06d33efe8b35"))
    def testAssertArticleUrl(self):
        self.assertTrue(jrt.AssertArticleURL("https://www.jianshu.com/p/06d33efe8b35"))
        self.assertTrue(jrt.AssertArticleURL("https://www.jianshu.com/p/b3cd0fee6325"))
        self.assertFalse(jrt.AssertArticleURL("https://www.jianshu.com/u/ea36c8d8aa30"))
        self.assertFalse(jrt.AssertArticleURL("https://www.jianshu.com/"))
        self.assertFalse(jrt.AssertArticleURL("https://www.baidu.com/"))
    def testStrToDatetime(self):
        result = jrt.StrToDatetime("2021-03-07T08:53:54.000+08:00")
        self.assertEqual(result.year,2021)
        self.assertEqual(result.month,3)
        self.assertEqual(result.day,7)
        self.assertEqual(result.hour,8)
        self.assertEqual(result.minute,53)
        self.assertEqual(result.second,54)
        self.assertEqual(result.microsecond,0)
        
class TestBeikeIslandMethods(unittest.TestCase):
    def testGetBeiKeIslandTotalTradeAmount(self):
        result = jrt.GetBeiKeIslandTotalTradeAmount()
        self.assertFalse(result == 0)
        self.assertTrue(result >= 20000000)
    def testGetBeiKeIslandTotalTradeCount(self):
        result = jrt.GetBeiKeIslandTotalTradeCount()
        self.assertFalse(result == 0)
        self.assertTrue(result >= 30000)
    def testGetBeikeIslandTradeRanking(self):
        for page in [1,2]:
            result = jrt.GetBeikeIslandTradeRanking(page)
            for item in result:
                self.assertFalse(item["bkuid"] == 0)
                self.assertFalse(item["jianshuname"] == "")
                self.assertFalse(item["amount"] == 0)
                self.assertFalse(item["times"] == 0)
            self.assertEqual(len(result),10)
            sleep(0.3)
    def testGetBeiKeIslandTradeList(self):
        buy_result = jrt.GetBeiKeIslandTradeList("buy")
        sell_result = jrt.GetBeiKeIslandTradeList("sell")
        with self.assertRaises(TypeError):
            jrt.GetBeiKeIslandTradeList()
        with self.assertRaises(ValueError):
            jrt.GetBeiKeIslandTradeList("3")
        for item in buy_result:
            self.assertFalse(item["JianshuName"] == "")
            self.assertFalse(item["BeiKeIslandName"] == "")
            self.assertFalse(item["Total"] == 0)
            self.assertFalse(item["Remaining"] == 0)
            self.assertFalse(item["Total"] < item["Remaining"])
            self.assertFalse(item["TradeLimit"] > item["Total"])
            self.assertFalse(item["TradeLimit"] > item["Remaining"])
            self.assertTrue(0 < item["Price"] < 3)
            self.assertIn(item["UserLevel"],["普通用户","普通会员","银牌会员","金牌会员"])
        for item in sell_result:
            self.assertFalse(item["JianshuName"] == "")
            self.assertFalse(item["BeiKeIslandName"] == "")
            self.assertFalse(item["Total"] == 0)
            self.assertFalse(item["Remaining"] == 0)
            self.assertFalse(item["Total"] < item["Remaining"])
            self.assertFalse(item["TradeLimit"] > item["Total"])
            self.assertFalse(item["TradeLimit"] > item["Remaining"])
            self.assertTrue(0 < item["Price"] < 3)
            self.assertIn(item["UserLevel"],["普通用户","普通会员","银牌会员","金牌会员"])
    def testGetBeiKeIslandTradePrice(self):
        self.assertTrue(0 <jrt.GetBeiKeIslandTradePrice("buy") < 3)
        self.assertTrue(0 <jrt.GetBeiKeIslandTradePrice("sell") < 3)

class TestUserMethods(unittest.TestCase):
    def testGetUID(self):
        self.assertEqual(jrt.GetUID("https://www.jianshu.com/u/ea36c8d8aa30"),"ea36c8d8aa30")
    def testGetUserName(self):
        self.assertEqual(jrt.GetUserName("https://www.jianshu.com/u/ea36c8d8aa30"),"初心不变_叶子")
    def testGetUserFollowersCount(self):
        self.assertTrue(0 < jrt.GetUserFollowersCount("https://www.jianshu.com/u/ea36c8d8aa30"))
    def testGetUserFansCount(self):
        self.assertTrue(0 < jrt.GetUserFansCount("https://www.jianshu.com/u/ea36c8d8aa30"))
    def testGetUserArticlesCount(self):
        self.assertTrue(0 < jrt.GetUserArticlesCount( "https://www.jianshu.com/u/ea36c8d8aa30"))
    def testGetUsersWordsCount(self):
        self.assertTrue(0 < jrt.GetUserWordsCount("https://www.jianshu.com/u/ea36c8d8aa30"))
    def testGetUserLikesCount(self):
        self.assertTrue(0 < jrt.GetUserLikesCount("https://www.jianshu.com/u/ea36c8d8aa30"))
    def testUsersAssetsCount(self):
        self.assertTrue(0 < jrt.GetUserAssetsCount("https://www.jianshu.com/u/ea36c8d8aa30"))
    def testGetUserBasicInformation(self):
        result = jrt.GetUserBasicInformation("https://www.jianshu.com/u/ea36c8d8aa30")
        self.assertTrue(result["name"] == jrt.GetUserName("https://www.jianshu.com/u/ea36c8d8aa30"))
        self.assertTrue(result["followers"] == jrt.GetUserFollowersCount("https://www.jianshu.com/u/ea36c8d8aa30"))
        self.assertTrue(result["fans"] == jrt.GetUserFansCount("https://www.jianshu.com/u/ea36c8d8aa30"))
        self.assertTrue(result["articles"] == jrt.GetUserArticlesCount("https://www.jianshu.com/u/ea36c8d8aa30"))
        self.assertTrue(result["words"] == jrt.GetUserWordsCount("https://www.jianshu.com/u/ea36c8d8aa30"))
        self.assertTrue(result["likes"] == jrt.GetUserLikesCount("https://www.jianshu.com/u/ea36c8d8aa30"))
        self.assertTrue(result["total_assets"] == jrt.GetUserAssetsCount("https://www.jianshu.com/u/ea36c8d8aa30"))
    def testGetUserBadgesCount(self):
        self.assertTrue(0 < len(jrt.GetUserBadgesList("https://www.jianshu.com/u/ea36c8d8aa30")) < 30)
    def testGetUserIntroduction(self):
        self.assertTrue(0 <= len(jrt.GetUserIntroduction("https://www.jianshu.com/u/43c3a5c5aca3")) < 1000)
    def testGetUserNotebookInfo(self):
        result = jrt.GetUserNotebookInfo("https://www.jianshu.com/u/ea36c8d8aa30")
        for item in result:
            self.assertTrue(item["nid"] != 0)
            self.assertTrue(item["name"] != "")
            if item["is_book"] == True:
                item["paid_book"] # 如果是连载，检查是否有付费连载状态字段
    def testGetUserManageableCollectionInfo(self):
        result = jrt.GetUserManageableCollectionInfo("https://www.jianshu.com/u/ea36c8d8aa30")
        for item in result:
            self.assertTrue(item["cid"] != 0)
            self.assertTrue(item["name"] != "")
    def testGetUserOwnCollectionInfo(self):
        result = jrt.GetUserOwnCollectionInfo("https://www.jianshu.com/u/ea36c8d8aa30")
        for item in result:
            self.assertTrue(item["cid"] != 0)
            self.assertTrue(item["name"] != "")
    def testUserAssetMethods(self):
        fp = jrt.GetUserFP("https://www.jianshu.com/u/ea36c8d8aa30")
        ftn = jrt.GetUserFTN("https://www.jianshu.com/u/ea36c8d8aa30")
        total = jrt.GetUserAssetsCount("https://www.jianshu.com/u/ea36c8d8aa30")
        self.assertEqual(round(fp + ftn,2),total)
    def testGetUserArticlesTitleList(self):
        for page in [1,2]:
            result = jrt.GetUserArticlesTitleList("https://www.jianshu.com/u/ea36c8d8aa30",page)
            for item in result:
                self.assertTrue(item != "")
    def testGetUserFollowersList(self):
        for page in [1,2]:
            result = jrt.GetUserFollowersList("https://www.jianshu.com/u/ea36c8d8aa30",page)
            for item in result:
                self.assertTrue(item != "")
    def testGetUserFansList(self):
        for page in [1,2]:
            result = jrt.GetUserFansList("https://www.jianshu.com/u/ea36c8d8aa30",page)
            for item in result:
                self.assertTrue(item != "")
                
class TestArticleMethods(unittest.TestCase):
    def testGetArticleTitle(self):
        self.assertTrue(jrt.GetArticleTitle("https://www.jianshu.com/p/06d33efe8b35") != "")
    def testGetArticleID(self):
        self.assertTrue(jrt.GetArticleID("https://www.jianshu.com/p/06d33efe8b35") != 0)
    def testGetArticleLikeCount(self):
        self.assertTrue(jrt.GetArticleLikeCount("https://www.jianshu.com/p/06d33efe8b35") >= 0)
    def testGetArticleCommentCount(self):
        self.assertTrue(jrt.GetArticleCommentCount("https://www.jianshu.com/p/06d33efe8b35") >= 0)
    def testGetArticleFPCount(self):
        self.assertTrue(jrt.GetArticleFPCount("https://www.jianshu.com/p/06d33efe8b35") >= 0)
    def testGetArticlePublishTime(self):
        result = jrt.GetArticlePublishTime("https://www.jianshu.com/p/06d33efe8b35")
        # TODO: 补全测试方法

if __name__ == "__main__":
    unittest.main(verbosity = 2)