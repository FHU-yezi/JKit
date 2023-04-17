from datetime import datetime

from yaml import dump as yaml_dump

test_cases = {
    # "type_cases": [
    #     {
    #         "type": "<class 'str'>",
    #         "value": "string"
    #     },
    #     {
    #         "type": "<class 'str'>",
    #         "value": "123"
    #     },
    #     {
    #         "type": "<class 'int'>",
    #         "value": 0
    #     },
    #     {
    #         "type": "<class 'int'>",
    #         "value": -1
    #     },
    #     {
    #         "type": "<class 'float'>",
    #         "value": 0.0
    #     },
    #     {
    #         "type": "<class 'float'>",
    #         "value": 1.0
    #     },
    #     {
    #         "type": "<class 'float'>",
    #         "value": -1.0
    #     },
    # ],
    "convert_cases": {
        "article_convert_cases": [
            {
                "aid": 87256893,
                "url": "https://www.jianshu.com/p/52698676395f",
                "aslug": "52698676395f",
            },
            {
                "aid": 89748991,
                "url": "https://www.jianshu.com/p/11dfce54cd7c",
                "aslug": "11dfce54cd7c",
            },
        ],
        "user_convert_cases": [
            {
                "uid": 19867175,
                "url": "https://www.jianshu.com/u/ea36c8d8aa30",
                "uslug": "ea36c8d8aa30",
            },
            {
                "uid": 19302450,
                "url": "https://www.jianshu.com/u/f8c2072f9afe",
                "uslug": "f8c2072f9afe",
            },
            {
                "uid": 14715425,
                "url": "https://www.jianshu.com/u/c5a2ce84f60b",
                "uslug": "c5a2ce84f60b",
            },
        ],
        "collection_convert_cases": [
            {
                "cid": 95,
                "url": "https://www.jianshu.com/c/fcd7a62be697",
                "cslug": "fcd7a62be697",
            },
            {
                "cid": 14,
                "url": "https://www.jianshu.com/c/V2CqjW",
                "cslug": "V2CqjW",
            },
            {
                "cid": 1938174,
                "url": "https://www.jianshu.com/c/a335661c66d9",
                "cslug": "a335661c66d9",
            },
        ],
        "island_convert_cases": [
            {
                "url": "https://www.jianshu.com/g/6187f99def472f5e",
                "islug": "6187f99def472f5e",
            }
        ],
        "notebook_convert_cases": [
            {
                "url": "https://www.jianshu.com/nb/36960761",
                "nslug": "36960761",
            },
            {
                "url": "https://www.jianshu.com/nb/36131833",
                "nslug": "36131833",
            },
        ],
    },
    "article_cases": {
        "success_cases": [
            {
                "aid": 87256893,
                "url": "https://www.jianshu.com/p/52698676395f",
                "aslug": "52698676395f",
                "title": "科技赋能创作星辰，简书分析工具集 JRT 发布",
                "author_name": "初心不变_叶子",
                "reads_count": (1000, 3000),
                "wordage": 1068,
                "likes_count": (40, 100),
                "comments_count": (15, 30),
                "most_valuable_comments_count": (0, 3),
                "total_FP_count": (80, 120),
                "description": "我们一直在想，当简书的一切都可以数据化，晦涩难懂的术语变为一张张图表，展现着创作背后的法则...... 当复杂的数据获取过程简化成一个函数调用，一行代码，一百毫秒.........",
                "publish_time": datetime(2021, 5, 1, 11, 34, 19).timestamp(),
                "update_time": datetime(2021, 5, 1, 11, 34, 19).timestamp(),
                "paid_status": False,
                "reprint_status": True,
                "comment_status": True,
            },
            {
                "aid": 89748991,
                "url": "https://www.jianshu.com/p/11dfce54cd7c",
                "aslug": "11dfce54cd7c",
                "title": "JRT 2.0，星辰赋能，创作未来",
                "author_name": "初心不变_叶子",
                "reads_count": (1600, 3000),
                "wordage": 1093,
                "likes_count": (85, 120),
                "comments_count": (15, 30),
                "most_valuable_comments_count": (2, 5),
                "total_FP_count": (100, 150),
                "description": "两个月前，我们发布了 JRT 的第一个正式版本。 自此，这一工具在社区的专业领域有了一定知名度，在 PyPI 上获得了 307 的月下载量。同时，我们也收到了来自不同行业用户...",
                "publish_time": datetime(2021, 7, 1, 11, 0).timestamp(),
                "update_time": datetime(2021, 7, 2, 14, 35, 36).timestamp(),
                "paid_status": False,
                "reprint_status": True,
                "comment_status": True,
            },
            {
                "aid": 78722940,
                "url": "https://www.jianshu.com/p/09c5bf171574",
                "aslug": "09c5bf171574",
                "title": "简书社区守护者徽章奖励公告",
                "author_name": "简书钻首席小管家",
                "reads_count": (7000, 12000),
                "wordage": 185,
                "likes_count": (65, 120),
                "comments_count": (0, 0),
                "most_valuable_comments_count": (0, 0),
                "total_FP_count": (65, 100),
                "description": "在过去的一段时间，简书社区对全站内容进行了全面审核，三位热心用户参与其中，帮助简书尽快完成审核工作。感谢各位热心用户的辛勤付出。 社区守护者徽章颁奖如下：任真[https:/...",
                "publish_time": datetime(2020, 10, 19, 17, 22, 6).timestamp(),
                "update_time": datetime(2020, 12, 24, 12, 38, 30).timestamp(),
                "paid_status": False,
                "reprint_status": True,
                "comment_status": False,
            },
        ],
        "fail_cases": [
            {
                "exception_name": "ResourceError",
                "url": "https://www.jianshu.com/p/abc1234qwert",
                "aslug": "abc1234qwert",
            }
        ],
    },
    "user_cases": {
        "success_cases": [
            {
                "uid": 19867175,
                "url": "https://www.jianshu.com/u/ea36c8d8aa30",
                "uslug": "ea36c8d8aa30",
                "name": "初心不变_叶子",
                "gender": 1,
                "followers_count": (200, 500),
                "fans_count": (1000, 3000),
                "articles_count": (150, 270),
                "wordage": (270000, 800000),
                "likes_count": (4000, 7000),
                "assets_count": (50000, 120000),
                "FP_count": (30000, 100000),
                "FTN_count": (1000, 50000),
                "badges_list": ["简书创作者", "岛主", "社区守护者"],
                "last_update_time": datetime(2021, 7, 31, 23, 6, 16).timestamp(),
                "VIP_info": {"vip_type": None, "expire_date": None},
                "next_anniversary_day": datetime(2022, 10, 21, 0, 0).timestamp(),
            },
            {
                "uid": 19302450,
                "url": "https://www.jianshu.com/u/f8c2072f9afe",
                "uslug": "f8c2072f9afe",
                "name": "小岛管理局局长",
                "gender": 0,
                "followers_count": (80, 120),
                "fans_count": (8000, 12000),
                "articles_count": (35, 60),
                "wordage": (18000, 30000),
                "likes_count": (9500, 13000),
                "assets_count": (500000, 700000),
                "FP_count": (150000, 200000),
                "FTN_count": (380000, 500000),
                "badges_list": ["简书员工", "鼠年大吉", "锦鲤", "幸运四叶草", "怦然心动", "岛主"],
                "last_update_time": datetime(2021, 3, 19, 11, 56, 14).timestamp(),
                "VIP_info": {
                    "vip_type": "铜牌",
                    "expire_date": datetime(2022, 3, 26, 11, 56, 14).timestamp(),
                },
                "next_anniversary_day": datetime(2022, 8, 19, 0, 0).timestamp(),
            },
            {
                "uid": 14715425,
                "url": "https://www.jianshu.com/u/c5a2ce84f60b",
                "uslug": "c5a2ce84f60b",
                "name": "简书钻首席小管家",
                "gender": 0,
                "followers_count": (10, 30),
                "fans_count": (160000, 200000),
                "articles_count": (450, 600),
                "wordage": (450000, 600000),
                "likes_count": (110000, 150000),
                "assets_count": (0, 5000),
                "FP_count": (0, 3000),
                "FTN_count": (0, 3000),
                "badges_list": ["简书创作者", "鼠年大吉", "二〇一九新春快乐~", "简书员工"],
                "last_update_time": datetime(2020, 10, 9, 18, 38, 36).timestamp(),
                "VIP_info": {"vip_type": None, "expire_date": None},
                "next_anniversary_day": datetime(2022, 10, 29, 0, 0).timestamp(),
            },
        ],
        "fail_cases": [
            {
                "exception_name": "ResourceError",
                "url": "https://www.jianshu.com/u/ea36c8d8aa31",
                "uslug": "ea36c8d8aa31",
            }
        ],
    },
    "collection_cases": {
        "success_cases": [
            {
                "cid": 95,
                "url": "https://www.jianshu.com/c/fcd7a62be697",
                "cslug": "fcd7a62be697",
                "avatar_url": "https://upload.jianshu.io/collections/images/95/1.jpg",
                "articles_count": (320000, 380000),
                "subscribers_count": (2300000, 2800000),
                "articles_update_time": datetime(2021, 12, 3, 0, 15, 49).timestamp(),
                "information_update_time": datetime(2021, 10, 21, 0, 21, 8).timestamp(),
            },
            {
                "cid": 14,
                "url": "https://www.jianshu.com/c/V2CqjW",
                "cslug": "V2CqjW",
                "avatar_url": "https://upload.jianshu.io/collections/images/14/6249340_194140034135_2.jpg",
                "articles_count": (35000, 45000),
                "subscribers_count": (2500000, 3000000),
                "articles_update_time": datetime(2021, 12, 1, 22, 40, 15).timestamp(),
                "information_update_time": datetime(
                    2021, 3, 12, 17, 46, 57
                ).timestamp(),
            },
            {
                "cid": 1938174,
                "url": "https://www.jianshu.com/c/a335661c66d9",
                "cslug": "a335661c66d9",
                "avatar_url": "https://upload.jianshu.io/collections/images/1938174/crop1611215330383.jpg",
                "articles_count": (2000, 5000),
                "subscribers_count": (1000, 3000),
                "articles_update_time": datetime(2021, 12, 3, 6, 2, 22).timestamp(),
                "information_update_time": datetime(
                    2021, 1, 28, 15, 40, 42
                ).timestamp(),
            },
        ],
        "fail_cases": [
            {
                "exception_name": "ResourceError",
                "url": "https://www.jianshu.com/c/a335661c66d0",
                "uslug": "a335661c66d0",
            }
        ],
    },
    "island_cases": {
        "success_cases": [
            {
                "url": "https://www.jianshu.com/g/6187f99def472f5e",
                "slug": "6187f99def472f5e",
                "name": "简友动态广场",
                "avatar_url": "https://upload.jianshu.io/group_image/18454410/6b6138a6-685a-4f12-80a7-5e731b5fc935",
                "members_count": (80000, 120000),
                "posts_count": (160000, 240000),
                "category": "生活",
            }
        ],
        "fail_cases": [
            {
                "exception_name": "ResourceError",
                "url": "https://www.jianshu.com/g/6187f99def472f5f",
                "uslug": "6187f99def472f5e",
            }
        ],
    },
    "notebook_cases": {
        "success_cases": [
            {
                "url": "https://www.jianshu.com/nb/36131833",
                "slug": "36131833",
                "name": "公告",
                "articles_count": (25, 40),
                "author_name": "简书",
                "author_uslug": "yZq3ZV",
                "author_avatar_url": "https://upload.jianshu.io/users/upload_avatars/259/5210859b-fc54-4cf8-908f-830f0237926a.png",
                "wordage": (9000, 20000),
                "subscribers_count": (0, 50),
                "update_time": datetime(2019, 4, 15, 16, 47, 50).timestamp(),
            }
        ],
        "fail_cases": [
            {
                "exception_name": "ResourceError",
                "url": "https://www.jianshu.com/nb/12345678",
                "uslug": "12345678",
            }
        ],
    },
}

with open("test_cases.yaml", "w", encoding="utf-8") as f:
    yaml_dump(test_cases, f, indent=4, allow_unicode=True)

print("测试用例生成成功！")
