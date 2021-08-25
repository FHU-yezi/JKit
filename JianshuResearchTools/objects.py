from datetime import datetime
from hashlib import md5

from . import article, beikeisland, collection, island, notebook, user
from .assert_funcs import (AssertArticleUrl, AssertCollectionUrl,
                           AssertIslandUrl, AssertNotebookUrl, AssertUserUrl)
from .convert import (ArticleSlugToArticleUrl, ArticleUrlToArticleSlug,
                      CollectionSlugToCollectionUrl,
                      CollectionUrlToCollectionSlug, IslandSlugToIslandUrl,
                      IslandUrlToIslandSlug, NotebookSlugToNotebookUrl,
                      NotebookUrlToNotebookId, NotebookUrlToNotebookSlug,
                      UserSlugToUserUrl, UserUrlToUserSlug)
from .exceptions import InputError


def GetHash(*args: any) -> str:
    """获取任意数量参数的哈希值

    Returns:
        str: 哈希值前 6 位
    """
    data = "".join([str(item) for item in args])
    result = md5(data.encode("utf-8")).hexdigest()
    result = result[0:7]  # 取前 6 位
    return result

def SimpleCache(cache_obj: list, getting_func: object, args: dict, disable_cache: bool = False) -> any:
    """基本缓存

    Args:
        cache_obj (list): 缓存信息储存对象
        getting_func (object): 信息获取函数
        args (dict): 信息获取函数的参数
        disable_cache (bool, optional): 禁用缓存. Defaults to False.

    Returns:
        any: 信息获取函数的返回值
    """
    if cache_obj != [] and disable_cache == False:
        return cache_obj[0]
    else:
        result = getting_func(**args)
        cache_obj.append(result)
        return result

def HashCache(cache_obj: dict, getting_func: object, args: dict, disable_cache: bool = False) -> any:
    """基于哈希值的缓存

    Args:
        cache_obj (dict): 缓存信息储存对象
        getting_func (object): 信息获取函数
        args (dict): 信息获取函数的参数
        disable_cache (bool, optional): 禁用缓存. Defaults to False.

    Returns:
        any: 信息获取函数的返回值
    """
    hash = GetHash(*list(args.values()))
    cache = cache_obj.get(hash)
    if cache != None and disable_cache == False:
        return cache
    else:
        result = getting_func(**args)
        cache_obj[hash] = result
        return result

class User():
    """用户类
    """
    def __init__(self, source: str):
        """构建新的用户对象

        Args:
            source (str): 用户个人主页 Url 或用户 Slug
        """
        try:
            AssertUserUrl(source)
        except InputError:
            # TODO: 这里还有点问题
            source = UserSlugToUserUrl(source)
            AssertUserUrl(source)
        self._url = source

        self._slug = []
        self._name = []
        self._gender = []
        self._followers_count = []
        self._fans_count = []
        self._articles_count = []
        self._wordage = []
        self._likes_count = []
        self._assets_count = []
        self._FP_count = []
        self._FTN_count = []
        self._badges = []
        self._last_update_time = []
        self._VIP_info = []
        self._introduction_text = []
        self._introduction_html = []
        self._notebooks = []
        self._own_collections = []
        self._manageable_collections = []

        self._articles_info = {}
        self._followers_info = {}
        self._fans_info = {}
    
    @property
    def url(self) -> str:
        """获取用户主页 Url

        Returns:
            str: 用户主页 Url
        """
        return self._url
    
    @property
    def slug(self, disable_cache: bool = False) -> str:
        """获取用户 Slug

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            str: 用户 Slug
        """
        result = SimpleCache(self._slug, UserUrlToUserSlug, 
                            {"user_url": self._url})
        return result
    
    @property
    def name(self, disable_cache:bool = False) -> str:
        """获取用户昵称

        Args:
            disable_cache (bool, optional): 禁用缓存，强制请求新结果. Defaults to False.

        Returns:
            str: 用户昵称
        """
        result = SimpleCache(self._name, user.GetUserName, 
                            {"user_url": self._url}, disable_cache)
        return result

    @property
    def gender(self, disable_cache: bool = False) -> int:
        """获取用户性别

        Args:
            disable_cache (bool, optional): 禁用缓存，强制请求新结果. Defaults to False.

        Returns:
            int: 用户性别，0 为未知，1 为男，2 为女
        """
        result = SimpleCache(self._gender, user.GetUserGender, 
                             {"user_url": self._url}, disable_cache)
        return result
    
    @property
    def followers_count(self, disable_cache: bool = False) -> int:
        """获取用户关注数

        Args:
            disable_cache (bool, optional): 禁用缓存，强制请求结果. Defaults to False.

        Returns:
            int: 关注数
        """
        result = SimpleCache(self._followers_count, user.GetUserFollowersCount, 
                            {"user_url": self._url}, disable_cache)
        return result
    
    @property
    def fans_count(self, disable_cache: bool = False) -> int:
        """获取用户粉丝数

        Args:
            disable_cache (bool, optional): 禁用缓存，强制请求结果. Defaults to False.

        Returns:
            int: 粉丝数
        """
        result = SimpleCache(self._fans_count, user.GetUserFansCount, 
                            {"user_url": self._url}, disable_cache)
        return result
    
    @property
    def articles_count(self, disable_cache: bool = False) -> int:
        """获取用户文章数

        Args:
            disable_cache (bool, optional): 禁用缓存，强制请求结果. Defaults to False.

        Returns:
            int: 文章数
        """
        result = SimpleCache(self._articles_count, user.GetUserArticlesCount, 
                            {"user_url": self._url}, disable_cache)
        return result
    
    @property
    def wordage(self, disable_cache: bool = False) -> int:
        """获取用户总字数

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            int: 总字数
        """
        result = SimpleCache(self._wordage, user.GetUserWordage, 
                            {"user_url": self._url}, disable_cache)
        return result
    
    @property
    def likes_count(self, disable_cache: bool = False) -> int:
        """获取用户被点赞数

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            int: 被点赞数
        """
        result = SimpleCache(self._likes_count, user.GetUserLikesCount, 
                            {"user_url": self._url}, disable_cache)
        return result

    @property
    def assets_count(self, disable_cache:bool = False) -> int:
        """获取用户资产量

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            int: 资产量
        """
        result = SimpleCache(self._assets_count, user.GetUserAssetsCount, 
                            {"user_url": self._url}, disable_cache)
        return result
    
    @property
    def FP_count(self, disable_cache: bool = False) -> int:
        """获取用户简书钻数量

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            int: 简书钻数量
        """
        result = SimpleCache(self._FP_count, user.GetUserFPCount, 
                            {"user_url": self._url}, disable_cache)
        return result
    
    @property
    def FTN_count(self, disable_cache: bool = False) -> int:
        """获取用户简书贝数量

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            int: 简书贝数量
        """
        result = SimpleCache(self._FTN_count, user.GetUserFTNCount, 
                            {"user_url": self._url}, disable_cache)
        return result
    
    @property
    def badges(self, disable_cache: bool = False) -> list:
        """获取徽章列表

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            list: 徽章列表
        """
        result = SimpleCache(self._badges, user.GetUserBadgesList, 
                            {"user_url": self._url}, disable_cache)
        return result
    
    @property
    def last_update_time(self, disable_cache: bool = False) -> datetime:
        """获取最近更新时间

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            datetime: 最近更新时间
        """
        result = SimpleCache(self._last_update_time, user.GetUserLastUpdateTime, 
                             {"user_url": self._url}, disable_cache)
        return result
    
    @property
    def VIP_info(self, disable_cache: bool = False) -> dict:
        """获取用户会员信息

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            dict: 会员信息
        """
        result = SimpleCache(self._VIP_info, user.GetUserVIPInfo, 
                             {"user_url": self._url}, disable_cache)
        return result
    
    @property
    def introduction_text(self, disable_cache: bool = False) -> str:
        """获取纯文本格式的用户简介

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            str:纯文本格式的用户简介
        """
        result = SimpleCache(self._introduction_text, user.GetUserIntroductionText, 
                             {"user_url", self._url}, disable_cache)
        return result
    
    @property
    def introduction_html(self, disable_cache: bool = False) -> str:
        """获取 Html 格式的用户简介

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            str: Html 格式的用户简介
        """
        result = SimpleCache(self._introduction_html, user.GetUserIntroductionHtml, 
                            {"user_url": self._url}, disable_cache)
        return result
    
    @property
    def notebooks(self, disable_cache: bool = False) -> list:
        """获取用户文集信息

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            list: 文集信息
        """
        result = SimpleCache(self._notebooks, user.GetUserNotebooksInfo, 
                            {"user_url": self._url}, disable_cache)
        return result
    
    @property
    def own_collections(self, disable_cache: bool = False) -> list:
        """获取自己创建的专题信息

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            list: 自己创建的专题信息
        """
        result = SimpleCache(self._own_collections, user.GetUserOwnCollectionsInfo, 
                            {"user_url": self._url}, disable_cache)
        return result
    
    @property
    def manageable_collections(self, disable_cache: bool = False) -> list:
        """获取有管理权的专题信息

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            list: 有管理权的专题信息
        """
        result = SimpleCache(self._manageable_collections, user.GetUserManageableCollectionsInfo, 
                            {"user_url": self._url}, disable_cache)
        return result
    
    def articles_info(self, page: int = 1, count: int = 10, 
                        disable_cache: bool = False) -> list:
        """获取文章信息

        Args:
            page (int, optional): 页码. Defaults to 1.
            count (int, optional): 每次获取的文章信息数量. Defaults to 10.
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            list: 文章信息
        """
        result = HashCache(self._articles_info, user.GetUserArticlesInfo, 
                            {"user_url": self._url, "page": page, "count": count}, 
                            disable_cache)
        return result

    def followers_info(self, page: int = 1, disable_cache: bool = False) -> list:
        """获取关注者信息

        Args:
            page (int, optional): 页码. Defaults to 1.
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            list: 关注者信息
        """
        result = HashCache(self._followers_info, user.GetUserFollowersInfo, 
                            {"user_url": self._url, "page": page}, disable_cache)
        return result

    def fans_info(self, page: int = 1, disable_cache: bool = False) -> list:
        """获取粉丝信息

        Args:
            page (int, optional): 页码. Defaults to 1.
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            list: 粉丝信息
        """
        result = HashCache(self._fans_info, user.GetUserFansInfo, 
                            {"user_url": self._url, "page": page}, disable_cache)
        return result
    
    def __eq__(self, other: object) -> bool:
        """判断是否是同一个用户

        Args:
            other (object): 另一个对象

        Returns:
            bool: 判断结果
        """
        if isinstance(other, User) == False:
            return False  # 不是由用户类构建的必定不相等
        if self._slug == other._slug:
            return True
        else:
            return False

    def __str__(self) -> str:
        """输出用户信息摘要

        Returns:
            str: 用户信息摘要
        """
        result = "用户信息摘要：\n用户名：{}\n性别：{}\n关注数：{}\n粉丝数：{}\n文章数：{}\n总字数：{}\n被点赞数：{}\n总资产：{}\n简书钻：{}\n简书贝：{}\n会员等级：{}\n会员过期时间：{}".format(
            self.name, {0: "未知", 1: "男", 2: "女"}[self.gender], self.followers_count, 
            self.fans_count, self.articles_count, self.wordage, self.likes_count, self.assets_count, 
            self.FP_count, self.FTN_count, self.VIP_info["vip_type"], self.VIP_info["expire_date"]
        )
        return result

class Article():
    """文章类
    """
    def __init__(self, source: str):
        """构建新的文章对象

        Args:
            source (str): 文章 Url 或文章 Slug
        """
        try:
            AssertArticleUrl(source)
        except InputError:
            source = ArticleSlugToArticleUrl(source)
            AssertArticleUrl(source)
        self._url = source

        self._slug = []
        self._title = []
        self._author = []
        self._wordage = []
        self._reads_count = []
        self._likes_count = []
        self._comments_count = []
        self._most_valuable_comments_count = []
        self._total_FP_count = []
        self._description = []
        self._publish_time = []
        self._update_time = []
        self._paid_status = []
        self._reprint_status = []
        self._comment_status = []
        self._html = []
        self._text = []
    
    @property
    def url(self) -> str:
        """获取文章 Url

        Returns:
            str: 文章 Url
        """
        return self._url
    
    @property
    def slug(self, disable_cache: bool = False) -> str:
        """获取文章 Slug

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            str: 文章 Slug
        """
        result = SimpleCache(self._slug, ArticleUrlToArticleSlug, 
                            {"user_url": self._slug}, disable_cache)
        return result
    
    @property
    def title(self, disable_cache: bool = False) -> str:
        """获取文章标题

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            str: 标题
        """
        result = SimpleCache(self._title, article.GetArticleTitle, 
                            {"article_url": self._url}, disable_cache)
        return result
    
    @property
    def author_name(self, disable_cache: bool = False) -> str:
        """获取文章作者名

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            str: 作者名
        """
        result = SimpleCache(self._author, article.GetArticleAuthorName, 
                            {"article_url": self._url}, disable_cache)
        return result
    
    @property
    def wordage(self, disable_cache: bool = False) -> int:
        """获取文章总字数

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            int: 总字数
        """
        result = SimpleCache(self._wordage, article.GetArticleWordage, 
                            {"article_url": self._url}, disable_cache)
        return result
    
    @property
    def reads_count(self, disable_cache: bool = False) -> int:
        """获取文章阅读量

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            int: 阅读量
        """
        result = SimpleCache(self._reads_count, article.GetArticleReadsCount, 
                            {"article_url": self._url}, disable_cache)
        return result
    
    @property
    def likes_count(self, disable_cache: bool = False) -> int:
        """获取文章点赞量

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            int: 文章点赞量
        """
        result = SimpleCache(self._likes_count, article.GetArticleLikesCount, 
                            {"article_url": self._url}, disable_cache)
        return result
    
    @property
    def comments_count(self, disable_cache: bool = False) -> int:
        """获取文章评论量

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            int: 文章评论量
        """
        result = SimpleCache(self._comments_count, article.GetArticleCommentsCount, 
                            {"article_url": self._url}, disable_cache)
        return result
    
    @property
    def most_valuable_comments_count(self, disable_cache: bool = False) -> int:
        """获取文章精选评论量

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            int: 文章精选评论量
        """
        result = SimpleCache(self._most_valuable_comments_count, 
                            article.GetArticleMostValuableCommentsCount, 
                            {"article_url": self._url}, disable_cache)
        return result
    
    @property
    def total_FP_count(self, disable_cache: bool = False) -> int:
        """获取文章总获钻量

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            int: 文章总获钻量
        """
        result = SimpleCache(self._total_FP_count, article.GetArticleTotalFPCount, 
                            {"article_url": self._url}, disable_cache)
        return result

    @property
    def description(self, disable_cache: bool = False) -> str:
        """获取文章摘要

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            str: 文章摘要
        """
        result = SimpleCache(self._description, article.GetArticleDescription, 
                            {"article_url": self._url}, disable_cache)
        return result
    
    @property
    def publish_time(self, disable_cache: bool = False) -> datetime:
        """获取文章发布时间

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            datetime: 文章发布时间
        """
        result = SimpleCache(self._publish_time, article.GetArticlePublishTime, 
                            {"article_url": self._url}, disable_cache)
        return result
    
    @property
    def update_time(self, disable_cache: bool = False) -> datetime:
        """获取文章更新时间

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            datetime: 文章更新时间
        """
        result = SimpleCache(self._update_time, article.GetArticleUpdateTime, 
                            {"article_url": self._url}, disable_cache)
        return result

    @property
    def paid_status(self, disable_cache: bool = False) -> bool:
        """获取文章付费状态

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            bool: 文章付费状态
        """
        result = SimpleCache(self._paid_status, article.GetArticlePaidStatus, 
                            {"article_url": self._url}, disable_cache)
        return result

    @property
    def reprint_status(self, disable_cache: bool = False) -> bool:
        """获取文章转载状态

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            bool: 文章转载状态
        """
        result = SimpleCache(self._reprint_status, article.GetArticleReprintStatus, 
                            {"article_url": self._url}, disable_cache)
        return result
    
    @property
    def comment_status(self, disable_cache: bool = False) -> bool:
        """获取文章评论状态

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            bool: 文章评论状态
        """
        result = SimpleCache(self._comment_status, article.GetArticleCommentStatus, 
                            {"article_url": self._url}, disable_cache)
        return result
    
    @property
    def html(self, disable_cache: bool = False) -> str:
        """获取 Html 格式的文章内容

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            str: Html 格式的文章内容
        """
        result = SimpleCache(self._html, article.GetArticleHtml, 
                            {"article_url": self._url}, disable_cache)
        return result
    
    @property
    def text(self, disable_cache: bool = False) -> str:
        """获取纯文本格式的文章内容

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            str: 纯文本格式的文章内容
        """
        result = SimpleCache(self._text, article.GetArticleText, 
                            {"article_url": self._url}, disable_cache)
        return result
    
    def __eq__(self, other: object) -> bool:
        """判断是否是同一篇文章

        Args:
            other (object): 另一个对象

        Returns:
            bool: 判断结果
        """
        if isinstance(other, Article) == False:
            return False  # 不是由文章类构建的必定不相等
        if self._slug == other._slug:
            return True
        else:
            return False
    
    def __str__(self) -> str:
        result = "文章信息摘要：\n标题：{}\n作者：{}\n获钻量：{}\n发布时间：{}\n更新时间：{}\n字数：{}\n阅读量：{}\n点赞量：{}\n评论量：{}".format(
            self.title, self.author_name, self.total_FP_count, self.publish_time, \
            self.update_time, self.wordage, self.reads_count, self.likes_count, self.comments_count
        )
        return result

class Notebook():
    """文集类
    """
    def __init__(self, source: str):
        """构建新的文集对象

        Args:
            source (str): 文集 Url 或文集 Slug
        """
        try:
            AssertNotebookUrl(source)
        except InputError:
            source = NotebookSlugToNotebookUrl(source)
            AssertNotebookUrl(source)
        self._url = source

        self._id = []
        self._slug = []
        self._name = []
        self._articles_count = []
        self._author_name = []
        self._author_info = []
        self._wordage = []
        self._subscribers_count = []
        self._update_time = []
        self._articles_info = {}
        
    @property
    def url(self) -> str:
        """获取文集 Url

        Returns:
            str: 文集 Url
        """
        return self._url
    
    @property
    def id(self, disable_cache: bool = False) -> int:
        """获取文集 ID

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            int: 文集 ID
        """
        result = SimpleCache(self._id, NotebookUrlToNotebookId, 
                             {"notebook_url": self._url}, disable_cache)
        return result
    
    @property
    def slug(self, disable_cache: bool = False) -> str:
        """获取文集 Slug

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            str: 文集 Slug
        """
        result = SimpleCache(self._slug, NotebookUrlToNotebookSlug, 
                             {"notebook_url": self._url}, disable_cache)
        return result

    @property
    def name(self, disable_cache: bool = False) -> str:
        """获取文集名称

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            str: 文集名称
        """
        result = SimpleCache(self._name, notebook.GetNotebookName, 
                             {"notebook_url": self._url}, disable_cache)
        return result
    
    @property
    def articles_count(self, disable_cache: bool = False) -> int:
        """获取文集中的文章总数

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            int: 文章总数
        """
        result = SimpleCache(self._articles_count, notebook.GetNotebookArticlesCount, 
                             {"notebook_url": self._url}, disable_cache)
        return result

    @property
    def author_name(self, disable_cache: bool = False) -> str:
        """获取文集的作者名

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            str: 作者名
        """
        result = SimpleCache(self._author_name, notebook.GetNotebookAuthorName, 
                             {"notebook_url": self._url}, disable_cache)
        return result
    
    @property
    def author_info(self, disable_cache: bool = False) -> dict:
        """获取文集的作者信息

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            dict: 作者信息
        """
        result = SimpleCache(self._author_info, notebook.GetNotebookAuthorInfo, 
                             {"notebook_url": self._url}, disable_cache)
        return result
    
    @property
    def wordage(self, disable_cache: bool = False) -> int:
        """获取文集中所有文章的总字数

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            int: 文集总字数
        """
        result = SimpleCache(self._wordage, notebook.GetNotebookWordage, 
                             {"notebook_url": self._url}, disable_cache)
        return result
    
    @property
    def subscribers_count(self, disable_cache: bool = False) -> int:
        """获取文集的关注者数量

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            int: 关注者数量
        """
        result = SimpleCache(self._subscribers_count, notebook.GetNotebookSubscribersCount, 
                             {"notebook_url": self._url}, disable_cache)
        return result
    
    @property
    def update_time(self, disable_cache: bool = False) -> datetime:
        """获取文集的更新时间

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            datetime: 更新时间
        """
        result = SimpleCache(self._update_time, notebook.GetNotebookUpdateTime, 
                             {"notebook_url": self._url}, disable_cache)
        return result
    
    def articles_info(self, page: int = 1, count: int = 10, sorting_method: str = "time", disable_cache: bool = False) -> list:
        """获取文集中的文章信息

        Args:
            page (int, optional): 页码. Defaults to 1.
            count (int, optional): 每次返回的数据数量. Defaults to 10.
            sorting_method (str, optional): 排序方法，time 为按照发布时间排序，
        comment_time 为按照最近评论时间排序，hot 为按照热度排序. Defaults to "time".
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            list: 文章信息
        """
        result = HashCache(self._articles_info, notebook.GetNotebookArticlesInfo, 
                           {"notebook_url": self._url, "page": page, "count": count, 
                            "sorting_method": sorting_method}, disable_cache)
        return result

    def __eq__(self, other: object) -> bool:
        """判断是否是同一个文集

        Args:
            other (object): 另一个对象

        Returns:
            bool: 判断结果
        """
        if isinstance(other, Notebook) == False:
            return False  # 不是由文集类构建的必定不相等
        if self.slug == other.slug:
            return True
        else:
            return False
        
    def __str__(self) -> str:
        """输出文集信息摘要

        Returns:
            str: 文集信息摘要
        """
        result = "文具信息摘要：\n名称：{}\n作者：{}\n文章数：{}\n总字数：{}\n关注者数量：{}\n更新时间：{}".format(
            self.name, self.author_name, self.articles_count, self.wordage, 
            self.subscribers_count, self.update_time
        )
        return result
    
class Collection():
    """专题类
    """
    def __init__(self, source: str, id: int = None):
        """构建新的文集对象

        Args:
            source (str): 文集 Url 或文集 Slug
            id (int): 专题 ID，如不传入将无法获取编辑、推荐作者和关注者信息
        """
        try:
            AssertCollectionUrl(source)
        except InputError:
            source = CollectionSlugToCollectionUrl(source)
            AssertCollectionUrl(source)
        self._url = source
        self._id = id
        
        self._slug = []
        self._name = []
        self._avatar_url = []
        self._introduction_text = []
        self._introduction_html = []
        self._articles_update_time = []
        self._info_update_time = []
        self._articles_count = []
        self._subscribers_count = []
        self._owner_info = []
        
        self._editors_info = {}
        self._recommended_writers_info = {}
        self._subscribers_info = {}
        self._articles_info = {}
        
    @property
    def url(self) -> str:
        """获取专题 Url

        Returns:
            str: 专题 Url
        """
        return self._url
    
    @property
    def slug(self, disable_cache: bool = False) -> str:
        """获取专题 Slug

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            str: 专题 Slug
        """
        result = SimpleCache(self._slug, CollectionUrlToCollectionSlug, 
                            {"user_url": self._slug}, disable_cache)
        return result
    
    @property
    def name(self, disable_cache: bool = False) -> str:
        """获取专题名称

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            str: 专题名称
        """
        result = SimpleCache(self._name, collection.GetCollectionName, 
                             {"collection_url": self._url}, disable_cache)
        return result
    
    @property
    def avatar_url(self, disable_cache: bool = False) -> str:
        """获取专题头像

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            str: 专题头像
        """
        result = SimpleCache(self._name, collection.GetCollectionAvatarUrl, 
                             {"collection_url": self._url}, disable_cache)
        return result
    
    @property
    def introduction_text(self, disable_cache: bool = False) -> str:
        """获取纯文本格式的专题简介

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            str: 纯文本格式的专题简介
        """
        result = SimpleCache(self._introduction_text, collection.GetCollectionIntroductionText, 
                             {"collection_url": self._url}, disable_cache)
        return result
    
    @property
    def introduction_html(self, disable_cache: bool = False) -> str:
        """获取 Html 格式的专题简介

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            str:  Html 格式的专题简介
        """
        result = SimpleCache(self._introduction_html, collection.GetCollectionIntroductionHtml, 
                             {"collection_url": self._url}, disable_cache)
        return result
    
    @property
    def articles_update_time(self, disable_cache: bool = False) -> datetime:
        """获取专题文章更新时间

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            datetime: 专题文章更新时间
        """
        result = SimpleCache(self._articles_update_time, collection.GetCollectionArticlesUpdateTime, 
                             {"collection_url": self._url}, disable_cache)
        return result

    @property
    def info_update_time(self, disable_cache: bool = False) -> datetime:
        """获取专题信息更新时间

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            datetime: 专题信息更新时间
        """
        result = SimpleCache(self._info_update_time, collection.GetCollectionInfoUpdateTime, 
                             {"collection_url": self._url}, disable_cache)
        return result
    
    @property
    def owner_info(self, disable_cache: bool = False) -> dict:
        """获取专题的所有者信息

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            dict: 用户信息
        """
        result = SimpleCache(self._owner_info, collection.GetCollectionOwnerInfo, 
                             {"collection_url": self._url}, disable_cache)
        return result
    
    @property
    def articles_count(self, disable_cache: bool = False) -> int:
        """获取专题文章数

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            int: 专题文章数
        """
        result = SimpleCache(self._articles_count, collection.GetCollectionArticlesCount, 
                             {"collection_url": self._url}, disable_cache)
        return result
    
    @property
    def subscribers_count(self, disable_cache: bool = False) -> int:
        """获取专题关注者数

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            int: 专题关注者数
        """
        result = SimpleCache(self._subscribers_count, collection.GetCollectionSubscribersCount, 
                             {"collection_url": self._url}, disable_cache)
        return result
    
    def editors_info(self, page: int = 1, disable_cache: bool = False) -> list:
        """获取专题编辑信息

        Args:
            page (int, optional): 页码. Defaults to 1.
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Raises:
            InputError: 因缺少 ID 参数而无法获取结果时抛出此异常

        Returns:
            list: 编辑信息
        """
        if self._id == None:
            raise InputError("实例化该专题对象时未传入 ID 参数，无法获取编辑信息")
        result = HashCache(self._editors_info, collection.GetCollectionEditorsInfo, 
                           {"collection_id": self._id, "page": page}, disable_cache)
        return result

    def recommended_writers_info(self, page: int = False, disable_cache: bool = False) -> list:
        """获取专题推荐作者信息

        Args:
            page (int, optional): 页码. Defaults to False.
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Raises:
            InputError: 因缺少 ID 参数而无法获取结果时抛出此异常

        Returns:
            list: 推荐作者信息
        """
        if self._id == None:
            raise InputError("实例化该专题对象时未传入 ID 参数，无法获取推荐作者信息")
        result = HashCache(self._recommended_writers_info, collection.GetCollectionRecommendedWritersInfo, 
                           {"collection_id": self._id}, disable_cache)
        return result
    
    def subscribers_info(self, start_sort_id: int, disable_cache: bool = False) -> list:
        """获取专题关注者信息

        Args:
            start_sort_id (int): 起始序号，等于上一条数据的序号
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Raises:
            InputError: 因缺少 ID 参数而无法获取结果时抛出此异常

        Returns:
            list: 关注者信息
        """
        if self._id == None:
            raise InputError("实例化该专题对象时未传入 ID 参数，无法获取关注者信息")
        result = HashCache(self._subscribers_info, collection.GetCollectionSubscribersInfo, 
                           {"collection_id": self._id, "start_sort_id": start_sort_id}, disable_cache)
        return result
    
    def articles_info(self, page: int = 1, count: int = 10, 
                      sorting_method: str = "time", disable_cache: bool = False) -> list:
        """获取专题文章信息

        Args:
            page (int, optional): 页码. Defaults to 1.
            count (int, optional): 每次返回的数据数量. Defaults to 10.
            sorting_method (str, optional): 排序方法，time 为按照发布时间排序，
        comment_time 为按照最近评论时间排序，hot 为按照热度排序. Defaults to "time".
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            list: 文章信息
        """
        result = HashCache(self._articles_info, collection.GetCollectionArticlesInfo, 
                           {"collection_url": self._url, "page": page, "count": count, 
                            "sorting_method": sorting_method}, disable_cache)
        return result
    
    def __eq__(self, other: object) -> bool:
        """判断是否是同一个专题

        Args:
            other (object): 另一个对象

        Returns:
            bool: 判断结果
        """
        if isinstance(other, Collection) == False:
            return False  # 不是由专题类构建的必定不相等
        if self._slug == other._slug:
            return True
        else:
            return False
    
    def __str__(self) -> str:
        """输出专题信息摘要

        Returns:
            str: 专题信息摘要
        """
        result = "专题信息摘要：\n名称：{}\n文章更新时间：{}\n信息更新时间：{}\n所有者：{}\n收录文章数：{}\n关注者数：{}".format(
            self.name, self.articles_update_time, self.info_update_time, 
            self.owner_info["name"], self.articles_count, self.subscribers_count
        )
        return result

class Island():
    """小岛类
    """
    def __init__(self, source):
        """构建新的小岛对象

        Args:
            source (str): 小岛 Url 或小岛 Slug
        """
        try:
            AssertIslandUrl(source)
        except InputError:
            source = IslandSlugToIslandUrl(source)
            AssertIslandUrl(source)
        self._url = source
        
        self._slug = []
        self._name = []
        self._avatar_url = []
        self._introduction = []
        self._members_count = []
        self._posts_count = []
        self._category = []
        
        self._posts = {}
    
    @property
    def url(self) -> str:
        """获取小岛 Url

        Returns:
            str: 小岛 Url
        """
        return self._url
    
    @property
    def slug(self, disable_cache: bool = False) -> str:
        """获取小岛 Slug

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            str: 小岛 Slug
        """
        result = SimpleCache(self._slug, IslandUrlToIslandSlug, 
                            {"user_url": self._slug}, disable_cache)
        return result
    
    @property
    def name(self, disable_cache: bool = False) -> str:
        """获取小岛名称

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            str: 小岛名称
        """
        result = SimpleCache(self._name, island.GetIslandName, 
                             {"island_url": self._url}, disable_cache)
        return result
    
    @property
    def avatar_url(self, disable_cache: bool = False) -> str:
        result = SimpleCache(self._avatar_url, island.GetIslandAvatarUrl, 
                             {"island_url":self._url}, disable_cache)
        return result
    
    @property
    def introduction(self, disable_cache: bool = False) -> str:
        """获取小岛简介

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            str: 小岛简介
        """
        result = SimpleCache(self._introduction, island.GetIslandIntroduction, 
                             {"island_url": self._url}, disable_cache)
        return result
    
    @property
    def members_count(self, disable_cache: bool = False) -> int:
        """获取小岛成员数量

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            int: 成员数量
        """
        result = SimpleCache(self._members_count, island.GetIslandMembersCount, 
                             {"island_url": self._url}, disable_cache)
        return result
    
    @property
    def posts_count(self, disable_cache: bool = False) -> int:
        """获取小岛帖子数量

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            int: 帖子数量
        """
        result = SimpleCache(self._posts_count, island.GetIslandPostsCount, 
                             {"island_url": self._url}, disable_cache)
        return result
    
    @property
    def category(self, disable_cache: bool = False) -> str:
        """获取小岛分类

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            str: 分类
        """
        result = SimpleCache(self._category, island.GetIslandCategory, 
                             {"island_url": self._url}, disable_cache)
        return result
    
    def posts(self, start_sort_id: int = None, count: int = 10, 
              topic_id: int = None, sorting_method: str = "time", disable_cache: bool = False) -> list:
        """获取小岛帖子信息

        Args:
            start_sort_id (int, optional): 起始序号，等于上一条数据的序号. Defaults to None.
            count (int, optional): 每次返回的数据数量. Defaults to 10.
            topic_id (int, optional): 话题 ID. Defaults to None.
            sorting_method (str, optional): 排序方法，time 为按照发布时间排序，
        comment_time 为按照最近评论时间排序，hot 为按照热度排序. Defaults to "time".
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            list: 帖子信息
        """
        result = HashCache(self._posts, island.GetIslandPosts, 
                           {"island_url": self._url, "start_sort_id": start_sort_id, 
                            "count": count, "topic_id": topic_id, "sorting_method": sorting_method}, disable_cache)
        return result
    
    def __eq__(self, other: object) -> bool:
        """判断是否是同一个小岛

        Args:
            other (object): 另一个对象

        Returns:
            bool: 判断结果
        """
        if isinstance(other, Collection) == False:
            return False  # 不是由小岛类构建的必定不相等
        if self._slug == other._slug:
            return True
        else:
            return False
    
    def __str__(self) -> str:
        """输出小岛信息摘要

        Returns:
            str: 小岛信息摘要
        """
        result = "小岛信息摘要：\n名称：{}\n成员数量：{}\n帖子数量：{}\n分类：{}".format(
            self.name, self.members_count, self.posts_count,self.category
        )
        return result
