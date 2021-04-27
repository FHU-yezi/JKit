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
        
    
if __name__ == "__main__":
    unittest.main(verbosity = 2)