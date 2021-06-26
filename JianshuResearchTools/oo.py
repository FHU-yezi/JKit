import hashlib
from datetime import datetime

import article
import beikeisland
import collection
import island
import user
from assert_funcs import *
from convert import *
from exceptions import InputError


def GetHash(*args: any) -> str:
    """获取任意数量参数的哈希值

    Returns:
        str: 哈希值前 6 位
    """
    data = "".join([str(item) for item in args])
    result = hashlib.md5(data.encode("utf-8")).hexdigest()
    result = result[0:7]  # 取前 6 位
    return result

def SimpleCache(cache_obj: any, getting_func: object, args: dict, disable_cache: bool =False):
    if cache_obj != None and disable_cache == False:
        return cache_obj
    else:
        result = getting_func(**args)
        cache_obj = result
        return result

def HashCache(cache_obj: any, getting_func: object, args: dict, disable_cache: bool =False):
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

        self._slug = None
        self._name = None
        self._followers_count = None
        self._fans_count = None
        self._articles_count = None
        self._words_count = None
        self._likes_count = None
        self._assets_count = None
        self._FP_count = None
        self._FTN_count = None
        self._badges = None
        self._introduction = None
        self._notebooks = None
        self._own_collections = None
        self._manageable_collections = None

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
    def slug(self, disable_cache: bool =False) -> str:
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
    def name(self, disable_cache:bool =False) -> str:
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
    def followers_count(self, disable_cache: bool =False) -> int:
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
    def fans_count(self, disable_cache: bool =False) -> int:
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
    def articles_count(self, disable_cache: bool =False) -> int:
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
    def words_count(self, disable_cache: bool =False) -> int:
        """获取用户总字数

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            int: 总字数
        """
        result = SimpleCache(self._words_count, user.GetUserWordsCount, 
                            {"user_url": self._url}, disable_cache)
        return result
    
    @property
    def likes_count(self, disable_cache: bool =False) -> int:
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
    def assets_count(self, disable_cache:bool =False) -> int:
        """获取用户资产量

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            int: 资产量
        """
        result = SimpleCache(self._assets_count, user.GetUserAssetsCount, 
                            {"usr_url": self._url}, disable_cache)
        return result
    
    @property
    def FP_count(self, disable_cache: bool =False) -> int:
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
    def FTN_count(self, disable_cache: bool =False) -> int:
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
    def badges(self, disable_cache: bool =False) -> list:
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
    def introduction(self, disable_cache: bool =False) -> str:
        """获取用户简介

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            str: 用户简介
        """
        result = SimpleCache(self._introduction, user.GetUserIntroduction, 
                            {"user_url": self._url}, disable_cache)
        return result
    
    @property
    def notebooks(self, disable_cache: bool =False) -> list:
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
    def manageable_collections(self, disable_cache: bool =False) -> list:
        """获取有管理权的专题信息

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            list: 有管理权的专题信息
        """
        result = SimpleCache(self._manageable_collections, user.GetUserManageableCollectionsInfo, 
                            {"user_url": self._url}, disable_cache)
        return result
    
    def articles_info(self, page: int =1, count: int =10, 
                        disable_cache: bool =False) -> list:
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

    def followers_info(self, page: int =1, disable_cache: bool =False) -> list:
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

    def fans_info(self, page: int =1, disable_cache: bool =False) -> list:
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
    
    def __eq__(self, other):
        """判断是否是同一个用户

        Args:
            other (object): 另一个对象
        """
        if isinstance(other, User) == False:
            return False  # 不是由用户类构建的均不相等
        if self.slug == other.slug:
            return True
        else:
            return False

    def __str__(self) -> str:
        """输出用户信息摘要

        Returns:
            str: 用户信息摘要
        """
        result = "用户名：{}\n关注数:{}\n粉丝数：{}\n文章数：{}\n总字数：{}\n被点赞数：{}\n总资产：{}".format(
            self.name, self.followers_count, self.fans_count, self.articles_count, \
            self.words_count, self.likes_count, self.assets_count
        )
        return result

class Article():
    """文章类
    """
    def __init__(self, source):
        try:
            AssertArticleUrl(source)
        except InputError:
            source = ArticleSlugToArticleUrl(source)
            AssertArticleUrl(source)
        self._url = source

        self._slug = None
        self._title = None
        self._likes_count = None
        self._comments_count = None
        self._most_valuable_comments_count = None
        self._total_FP_count = None
        self._desciption = None
        self._publish_time = None
        self._update_time = None
        self._paid_status = None
        self._reprint_status = None
        self._comment_status = None
        self._html = None
        self._text = None
    
    @property
    def url(self) -> str:
        return self._url
    
    @property
    def slug(self, disable_cache: bool =False) -> str:
        result = SimpleCache(self._slug, ArticleUrlToArticleSlug, 
                            {"user_url": self._slug})
        return result
    
    @property
    def title(self, disable_cache: bool =False) -> str:
        result = SimpleCache(self._title, article.GetArticleTitle, 
                            {"article_url": self._url}, disable_cache)
        return result
    
    @property
    def likes_count(self, disable_cache: bool =False) -> int:
        result = SimpleCache(self._likes_count, article.GetArticleLikesCount, 
                            {"article_url": self._url}, disable_cache)
        return result
    
    @property
    def comments_count(self, disable_cache: bool =False) -> int:
        result = SimpleCache(self._comments_count, article.GetArticleCommentsCount, 
                            {"article_url": self._url}, disable_cache)
        return result
    
    @property
    def most_valuable_comments_count(self, disable_cache: bool =False) -> int:
        result = SimpleCache(self._most_valuable_comments_count, 
                            article.GetArticleMostValuableCommentsCount, 
                            {"article_url": self._url}, disable_cache)
        return result
    
    @property
    def total_FP_count(self, disable_cache: bool =False) -> int:
        result = SimpleCache(self._total_FP_count, article.GetArticleTotalFPCount, 
                            {"article_url": self._total_FP_count}, disable_cache)
        return result

    @property
    def description(self, disable_cache: bool =False) -> str:
        result = SimpleCache(self._desciption, article.GetArticleDescription, 
                            {"article_url": self._url}, disable_cache)
        return result
    
    @property
    def publish_time(self, disable_cache: bool =False) -> datetime:
        result = SimpleCache(self._publish_time, article.GetArticlePublishTime, 
                            {"article_url": self._url}, disable_cache)
        return result
    
    @property
    def update_time(self, disable_cache: bool =False) -> datetime:
        result = SimpleCache(self._update_time, article.GetArticleUpdateTime, 
                            {"article_url": self._url}, disable_cache)
        return result
