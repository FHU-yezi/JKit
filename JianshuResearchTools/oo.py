import article
import beikeisland
import collection
import island
import user
from assert_funcs import *
from convert import *


class User():
    """用户类
    """
    def __init__(self, url: str =None, slug: str = None):
        if url != None:
            AssertUserUrl(url)
            self._url = url
        elif slug != None:
            url = UserSlugToUserUrl(slug)
            AssertUserUrl(url)
            self._url = url
        else:
            raise AttributeError("url 与 slug 不能同时为空")

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
        self._articles_info = None
        self._followers_info = None
        self._fans_info = None
    
    @property
    def url(self):
        return self._url
    
    @property
    def slug(self):
        if self._slug != None:
            return self._slug
        else:
            result = UserUrlToUserSlug(self._url)
            self._slug = result
            return result
    
    @property
    def name(self, force_refresh:bool =False):
        if self._name != None and force_refresh == False:
            return self._name
        else:
            result = user.GetUserName(self._url)
            self._name = result
            return result

    @property
    def followers_count(self, force_refresh: bool =False):
        if self._followers_count != None and force_refresh == False:
            return self._followers_count
        else:
            result = user.GetUserFollowersCount(self._url)
            self._followers_count = result
            return result
    
    @property
    def fans_count(self, force_refresh: bool =False):
        if self._fans_count != None and force_refresh == False:
            return self._fans_count
        else:
            result = user.GetUserFansCount(self._url)
            self._fans_count = result
            return result
    
    @property
    def articles_count(self, force_refresh: bool =False):
        if self._articles_count != None and force_refresh == False:
            return self._articles_count
        else:
            result = user.GetUserArticlesCount(self._url)
            self._articles_count = result
            return result
    
    @property
    def words_count(self, force_refresh: bool =False):
        if self._words_count != None and force_refresh == False:
            return self._words_count
        else:
            result = user.GetUserWordsCount(self._url)
            self._words_count = result
            return result
    
    @property
    def likes_count(self, force_refresh: bool =False):
        if self._likes_count != None and force_refresh == False:
            return self._likes_count
        else:
            result = user.GetUserLikesCount(self._url)
            self._likes_count = result
            return result

    @property
    def assets_count(self, force_refresh:bool =False):
        if self._assets_count != None and force_refresh == False:
            return self._assets_count
        else:
            result = user.GetUserAssetsCount(self._url)
            self._assets_count = result
            return result
    
    @property
    def FP_count(self, force_refresh: bool =False):
        if self._FP_count != None and force_refresh == False:
            return self._FP_count
        else:
            result = user.GetUserFPCount(self._url)
            self._FP_count = result
            return result
    
    @property
    def FTN_count(self, force_refresh: bool =False):
        if self._FTN_count != None and force_refresh == False:
            return self._FTN_count
        else:
            result = user.GetUserFTNCount(self._url)
            self._FTN_count = result
            return result
    
    @property
    def badges(self, force_refresh: bool =False):
        if self._badges != None and force_refresh == False:
            return self._badges
        else:
            result = user.GetUserBadgesList(self._url)
            self._badges = result
            return result
    
    @property
    def introduction(self, force_refresh: bool =False):
        if self._introduction != None and force_refresh == False:
            return self._introduction
        else:
            result = user.GetUserIntroduction(self._url)
            self._introduction = result
            return result