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
    
if __name__ == "__main__":
    unittest.main(verbosity = 2)