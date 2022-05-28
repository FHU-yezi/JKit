__all__ = ["PC_header", "jianshu_request_header", "BeikeIsland_request_header", "mobile_header"]


PC_header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
}

jianshu_request_header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57",
                          "X-INFINITESCROLL": "true",
                          "X-Requested-With": "XMLHttpRequest"
                          }

BeikeIsland_request_header = {"Host": "www.beikeisland.com",
                              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57",
                              "Content-Type": "application/json",
                              "Version": "v2.0"
                              }

mobile_header = {"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.134 Mobile Safari/537.36"}
