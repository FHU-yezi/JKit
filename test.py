import unittest

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
    
      
if __name__ == "__main__":
    unittest.main(verbosity = 2)