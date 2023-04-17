__version__ = "2.11.0"

from . import article, collection, island, notebook, objects, rank, user

__all__ = ["article", "collection", "island", "notebook", "objects", "rank", "user"]


def future() -> None:
    """彩蛋

    在 JRT 2.0 版本中加入
    """
    print("回望洪荒，历史苍茫；\n只身向前，重铸星光。\n赴梦万里，道阻且长；\n今日萤火，明日华章。")
