import json

import requests

from basic import beikeisland_request_header


def GetBeiKeIslandTotalTradeAmount() -> int:
    # TODO: 注释优化
    """该函数返回贝壳小岛的总交易额。

    Returns:
        int: 总交易额
    """
    data = {}  # 不传送数据也能正常获取，节省时间和带宽
    source = requests.post("https://www.beikeisland.com/api/Trade/getTradeRankList", 
                            headers=beikeisland_request_header, json=data)
    json_obj = json.loads(source.content)
    result = json_obj["data"]["totalcount"]
    return result

def GetBeiKeIslandTotalTradeCount() -> int:
    # TODO: 注释优化
    """该函数返回贝壳小岛的总交易次数。

    Returns:
        int: 总交易次数
    """
    data = {}  # 不传送数据也能正常获取，节省时间和带宽
    source = requests.post("https://www.beikeisland.com/api/Trade/getTradeRankList", 
                            headers=beikeisland_request_header, json=data)
    json_obj = json.loads(source.content)
    result = json_obj["data"]["totaltime"]
    return result