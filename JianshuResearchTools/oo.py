import hashlib

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
    def slug(self) -> str:
        """获取用户 slug

        Returns:
            str: 用户 slug
        """
        if self._slug != None:
            return self._slug
        else:
            result = UserUrlToUserSlug(self._url)
            self._slug = result
            return result
    
    @property
    def name(self, disable_cache:bool =False) -> str:
        """获取用户昵称

        Args:
            disable_cache (bool, optional): 禁用缓存，强制请求新结果. Defaults to False.

        Returns:
            str: 用户昵称
        """
        if self._name != None and disable_cache == False:
            return self._name
        else:
            result = user.GetUserName(self._url)
            self._name = result
            return result

    @property
    def followers_count(self, disable_cache: bool =False) -> int:
        """获取用户关注数

        Args:
            disable_cache (bool, optional): 禁用缓存，强制请求结果. Defaults to False.

        Returns:
            int: 关注数
        """
        if self._followers_count != None and disable_cache == False:
            return self._followers_count
        else:
            result = user.GetUserFollowersCount(self._url)
            self._followers_count = result
            return result
    
    @property
    def fans_count(self, disable_cache: bool =False) -> int:
        """获取用户粉丝数

        Args:
            disable_cache (bool, optional): 禁用缓存，强制请求结果. Defaults to False.

        Returns:
            int: 粉丝数
        """
        if self._fans_count != None and disable_cache == False:
            return self._fans_count
        else:
            result = user.GetUserFansCount(self._url)
            self._fans_count = result
            return result
    
    @property
    def articles_count(self, disable_cache: bool =False) -> int:
        """获取用户文章数

        Args:
            disable_cache (bool, optional): 禁用缓存，强制请求结果. Defaults to False.

        Returns:
            int: 文章数
        """
        if self._articles_count != None and disable_cache == False:
            return self._articles_count
        else:
            result = user.GetUserArticlesCount(self._url)
            self._articles_count = result
            return result
    
    @property
    def words_count(self, disable_cache: bool =False) -> int:
        """获取用户总字数

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            int: 总字数
        """
        if self._words_count != None and disable_cache == False:
            return self._words_count
        else:
            result = user.GetUserWordsCount(self._url)
            self._words_count = result
            return result
    
    @property
    def likes_count(self, disable_cache: bool =False) -> int:
        """获取用户被点赞数

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            int: 被点赞数
        """
        if self._likes_count != None and disable_cache == False:
            return self._likes_count
        else:
            result = user.GetUserLikesCount(self._url)
            self._likes_count = result
            return result

    @property
    def assets_count(self, disable_cache:bool =False) -> int:
        """获取用户资产量

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            int: 资产量
        """
        if self._assets_count != None and disable_cache == False:
            return self._assets_count
        else:
            result = user.GetUserAssetsCount(self._url)
            self._assets_count = result
            return result
    
    @property
    def FP_count(self, disable_cache: bool =False) -> int:
        """获取用户简书钻数量

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            int: 简书钻数量
        """
        if self._FP_count != None and disable_cache == False:
            return self._FP_count
        else:
            result = user.GetUserFPCount(self._url)
            self._FP_count = result
            return result
    
    @property
    def FTN_count(self, disable_cache: bool =False) -> int:
        """获取用户简书贝数量

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            int: 简书贝数量
        """
        if self._FTN_count != None and disable_cache == False:
            return self._FTN_count
        else:
            result = user.GetUserFTNCount(self._url)
            self._FTN_count = result
            return result
    
    @property
    def badges(self, disable_cache: bool =False) -> list:
        """获取徽章列表

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            list: 徽章列表
        """
        if self._badges != None and disable_cache == False:
            return self._badges
        else:
            result = user.GetUserBadgesList(self._url)
            self._badges = result
            return result
    
    @property
    def introduction(self, disable_cache: bool =False) -> str:
        """获取用户简介

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            str: 用户简介
        """
        if self._introduction != None and disable_cache == False:
            return self._introduction
        else:
            result = user.GetUserIntroduction(self._url)
            self._introduction = result
            return result
    
    @property
    def notebooks(self, disable_cache: bool =False) -> list:
        """获取用户文集信息

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            list: 文集信息
        """
        if self._notebooks != None and disable_cache == False:
            return self._notebooks
        else:
            result = user.GetUserNotebooksInfo(self._url)
            self._notebooks = result
            return result
    
    @property
    def own_collections(self, force_refresh: bool = False) -> list:
        """获取自己创建的专题信息

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            list: 自己创建的专题信息
        """
        if self._own_collections != None and disable_cache == False:
            return self._own_collections
        else:
            result = user.GetUserOwnCollectionsInfo(self._url)
            self._own_collections = result
            return result
    
    @property
    def manageable_collections(self, disable_cache: bool =False) -> list:
        """获取有管理权的专题信息

        Args:
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            list: 有管理权的专题信息
        """
        if self._manageable_collections != None and disable_cache == False:
            return self._manageable_collections
        else:
            result = user.GetUserManageableCollectionsInfo(self._url)
            self._manageable_collections = result
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
        hash = GetHash(page, count)
        cache = self._articles_info.get(hash)
        if cache != None and disable_cache == False:
            return cache
        else:
            result = user.GetUserArticlesInfo(self._url, page, count)
            hash = GetHash(page, count)
            self._articles_info[hash] = result
            return result

    def followers_info(self, page: int =1, disable_cache: bool =False) -> list:
        """获取关注者信息

        Args:
            page (int, optional): 页码. Defaults to 1.
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            list: 关注者信息
        """
        hash = GetHash(page)
        cache = self._followers_info.get(hash)
        if cache != None and disable_cache == False:
            return cache
        else:
            result = user.GetUserFollowersInfo(self._url, page)
            hash = GetHash(page)
            self._followers_info[hash] = result
            return result

    def fans_info(self, page: int =1, disable_cache: bool =False) -> list:
        """获取粉丝信息

        Args:
            page (int, optional): 页码. Defaults to 1.
            disable_cache (bool, optional): 禁用缓存. Defaults to False.

        Returns:
            list: 粉丝信息
        """
        hash = GetHash(page)
        cache = self._fans_info.get(hash)
        if cache != None and disable_cache == False:
            return cache
        else:
            result = user.GetUserFansInfo(self._url, page)
            hash = GetHash(page)
            self._fans_info[hash] = result
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
    def slug(self) -> str:
        if self._slug != None:
            return self._slug
        else:
            result = ArticleUrlToArticleSlug(self._url)
            self._slug = result
            return result
    
    @property
    def title(self) -> str:
        if self._title != None:
            return self._title
        else:
            result = article.GetArticleTitle(self._url)
            self._title = result
            return result
    
    @property
    def likes_count(self) -> int:
        if self._likes_count != None:
            return self._likes_count
        else:
            result = article.GetArticleLikesCount(self._url)
            self._likes_count = result
            return result
    
    @property
    def comments_count(self) -> int:
        if self._comments_count != None:
            return self.comments_count
        else:
            result = article.GetArticleCommentsCount(self._url)
            self._comments_count = result
            return result