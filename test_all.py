from datetime import datetime
from typing import Any, List, Union

import pytest
from yaml import FullLoader
from yaml import load as yaml_load

import JianshuResearchTools as jrt
from JianshuResearchTools.convert import (ArticleSlugToArticleId,
                                          ArticleSlugToArticleUrl,
                                          ArticleUrlToArticleId,
                                          ArticleUrlToArticleSlug,
                                          CollectionSlugToCollectionUrl,
                                          CollectionUrlToCollectionId,
                                          CollectionUrlToCollectionSlug,
                                          IslandSlugToIslandUrl,
                                          IslandUrlToIslandSlug,
                                          NotebookSlugToNotebookUrl,
                                          NotebookUrlToNotebookSlug,
                                          UserSlugToUserId, UserSlugToUserUrl,
                                          UserUrlToUserId, UserUrlToUserSlug)
from JianshuResearchTools.exceptions import APIError, InputError, ResourceError

error_text_to_obj = {
    "InputError": InputError,
    "APIError": APIError,
    "ResourceError": ResourceError
}


class NumberNotInRangeError(Exception):
    """内容不在数值范围内时抛出此异常"""
    pass


def AssertNormalCase(value: Any, case: Any) -> None:
    assert type(value) == type(case)
    assert value == case


def AssertDatetimeCase(value: datetime, case: float) -> None:
    assert value.timestamp() >= case


def AssertRangeCase(value: Union[int, float], case: List[Union[int, float]]) -> None:
    if not case[0] <= value <= case[1]:
        raise NumberNotInRangeError(f"{value} 不在范围 {case} 中")


def AssertListCase(value: List[Any], case: List[Any]):
    assert set(case).issubset(set(value))


with open("test_cases.yaml", "r", encoding="utf-8") as f:
    test_cases = yaml_load(f, Loader=FullLoader)


class TestEggs():  # 测试彩蛋内容
    def TestFuture(self):
        jrt.future()


class TestConvertModule():
    def test_UserUrlToUserId(self):
        for case in test_cases["convert_cases"]["user_convert_cases"]:
            AssertNormalCase(UserUrlToUserId(case["url"]), case["uid"])

    def test_UserSlugToUserId(self):
        for case in test_cases["convert_cases"]["user_convert_cases"]:
            AssertNormalCase(UserSlugToUserId(case["uslug"]), case["uid"])

    def test_UserUrlToUserSlug(self):
        for case in test_cases["convert_cases"]["user_convert_cases"]:
            AssertNormalCase(UserUrlToUserSlug(case["url"]), case["uslug"])

    def test_UserSlugToUserUrl(self):
        for case in test_cases["convert_cases"]["user_convert_cases"]:
            AssertNormalCase(UserSlugToUserUrl(case["uslug"]), case["url"])

    def test_ArticleUrlToArticleSlug(self):
        for case in test_cases["convert_cases"]["article_convert_cases"]:
            AssertNormalCase(ArticleUrlToArticleSlug(case["url"]), case["aslug"])

    def test_ArticleSlugToArticleUrl(self):
        for case in test_cases["convert_cases"]["article_convert_cases"]:
            AssertNormalCase(ArticleSlugToArticleUrl(case["aslug"]), case["url"])

    def test_ArticleSlugToArticleId(self):
        for case in test_cases["convert_cases"]["article_convert_cases"]:
            AssertNormalCase(ArticleSlugToArticleId(case["aslug"]), case["aid"])

    def test_ArticleUrlToArticleId(self):
        for case in test_cases["article_cases"]["success_cases"]:
            AssertNormalCase(ArticleUrlToArticleId(case["url"]), case["aid"])

    def test_NotebookUrlToNotebookSlug(self):
        for case in test_cases["convert_cases"]["notebook_convert_cases"]:
            AssertNormalCase(NotebookUrlToNotebookSlug(case["url"]), case["nslug"])

    def test_NotebookSlugToNotebookUrl(self):
        for case in test_cases["convert_cases"]["notebook_convert_cases"]:
            AssertNormalCase(NotebookSlugToNotebookUrl(case["nslug"]), case["url"])

    def test_CollectionUrlToCollectionSlug(self):
        for case in test_cases["convert_cases"]["collection_convert_cases"]:
            AssertNormalCase(CollectionUrlToCollectionSlug(case["url"]), case["cslug"])

    def test_CollectionSlugToCollectionUrl(self):
        for case in test_cases["convert_cases"]["collection_convert_cases"]:
            AssertNormalCase(CollectionSlugToCollectionUrl(case["cslug"]), case["url"])

    def test_CollectionUrlToCollectionId(self):
        for case in test_cases["convert_cases"]["collection_convert_cases"]:
            AssertNormalCase(CollectionUrlToCollectionId(case["url"]), case["cid"])

    def test_IslandUrlToIslandSlug(self):
        for case in test_cases["convert_cases"]["island_convert_cases"]:
            AssertNormalCase(IslandUrlToIslandSlug(case["url"]), case["islug"])

    def test_IslandSlugToIslandUrl(self):
        for case in test_cases["convert_cases"]["island_convert_cases"]:
            AssertNormalCase(IslandSlugToIslandUrl(case["islug"]), case["url"])


class TestArticleModule():
    def test_GetArticleTitle(self):
        for case in test_cases["article_cases"]["success_cases"]:
            AssertNormalCase(jrt.article.GetArticleTitle(case["url"]), case["title"])

        for case in test_cases["article_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.article.GetArticleTitle(case["url"])

    def test_GetArticleAuthorName(self):
        for case in test_cases["article_cases"]["success_cases"]:
            AssertNormalCase(jrt.article.GetArticleAuthorName(case["url"]), case["author_name"])

        for case in test_cases["article_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.article.GetArticleAuthorName(case["url"])

    def test_GetArticleReadsCount(self):
        for case in test_cases["article_cases"]["success_cases"]:
            AssertRangeCase(jrt.article.GetArticleReadsCount(case["url"]), case["reads_count"])

        for case in test_cases["article_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.article.GetArticleReadsCount(case["url"])

    def test_GetArticleWordage(self):
        for case in test_cases["article_cases"]["success_cases"]:
            AssertNormalCase(jrt.article.GetArticleWordage(case["url"]), case["wordage"])

        for case in test_cases["article_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.article.GetArticleWordage(case["url"])

    def test_GetArticleLikesCount(self):
        for case in test_cases["article_cases"]["success_cases"]:
            AssertRangeCase(jrt.article.GetArticleLikesCount(case["url"]), case["likes_count"])

        for case in test_cases["article_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.article.GetArticleLikesCount(case["url"])

    def test_GetArticleCommentsCount(self):
        for case in test_cases["article_cases"]["success_cases"]:
            AssertRangeCase(jrt.article.GetArticleCommentsCount(case["url"]), case["comments_count"])

        for case in test_cases["article_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.article.GetArticleCommentsCount(case["url"])

    def test_GetArticleMostValuableCommentsCount(self):
        for case in test_cases["article_cases"]["success_cases"]:
            AssertRangeCase(jrt.article.GetArticleMostValuableCommentsCount(case["url"]), case["most_valuable_comments_count"])

        for case in test_cases["article_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.article.GetArticleMostValuableCommentsCount(case["url"])

    def test_GetArticleTotalFPCount(self):
        for case in test_cases["article_cases"]["success_cases"]:
            AssertRangeCase(jrt.article.GetArticleTotalFPCount(case["url"]), case["total_FP_count"])

        for case in test_cases["article_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.article.GetArticleTotalFPCount(case["url"])

    def test_GetArticleDescription(self):
        for case in test_cases["article_cases"]["success_cases"]:
            AssertNormalCase(jrt.article.GetArticleDescription(case["url"]), case["description"])

        for case in test_cases["article_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.article.GetArticleDescription(case["url"])

    def test_GetArticlePublishTime(self):
        for case in test_cases["article_cases"]["success_cases"]:
            AssertDatetimeCase(jrt.article.GetArticlePublishTime(case["url"]), case["publish_time"])

        for case in test_cases["article_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.article.GetArticlePublishTime(case["url"])

    def test_GetArticleUpdateTime(self):
        for case in test_cases["article_cases"]["success_cases"]:
            AssertDatetimeCase(jrt.article.GetArticleUpdateTime(case["url"]), case["update_time"])

        for case in test_cases["article_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.article.GetArticleUpdateTime(case["url"])

    def test_GetArticlePaidStatus(self):
        for case in test_cases["article_cases"]["success_cases"]:
            AssertNormalCase(jrt.article.GetArticlePaidStatus(case["url"]), case["paid_status"])

        for case in test_cases["article_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.article.GetArticlePaidStatus(case["url"])

    def test_GetArticleReprintStatus(self):
        for case in test_cases["article_cases"]["success_cases"]:
            AssertNormalCase(jrt.article.GetArticleReprintStatus(case["url"]), case["reprint_status"])

        for case in test_cases["article_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.article.GetArticleReprintStatus(case["url"])

    def test_GetArticleCommentStatus(self):
        for case in test_cases["article_cases"]["success_cases"]:
            AssertNormalCase(jrt.article.GetArticleCommentStatus(case["url"]), case["comment_status"])

        for case in test_cases["article_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.article.GetArticleCommentStatus(case["url"])


class TestUserModule():
    def test_GetUserName(self):
        for case in test_cases["user_cases"]["success_cases"]:
            AssertNormalCase(jrt.user.GetUserName(case["url"]), case["name"])

        for case in test_cases["user_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.user.GetUserName(case["url"])

    def test_GetUserGender(self):
        for case in test_cases["user_cases"]["success_cases"]:
            AssertNormalCase(jrt.user.GetUserGender(case["url"]), case["gender"])

        for case in test_cases["user_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.user.GetUserGender(case["url"])

    def test_GetUserFollowersCount(self):
        for case in test_cases["user_cases"]["success_cases"]:
            AssertRangeCase(jrt.user.GetUserFollowersCount(case["url"]), case["followers_count"])

        for case in test_cases["user_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.user.GetUserFollowersCount(case["url"])

    def test_GetUserFansCount(self):
        for case in test_cases["user_cases"]["success_cases"]:
            AssertRangeCase(jrt.user.GetUserFansCount(case["url"]), case["fans_count"])

        for case in test_cases["user_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.user.GetUserFansCount(case["url"])

    def test_GetUserArticlesCount(self):
        for case in test_cases["user_cases"]["success_cases"]:
            AssertRangeCase(jrt.user.GetUserArticlesCount(case["url"]), case["articles_count"])

        for case in test_cases["user_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.user.GetUserArticlesCount(case["url"])

    def test_GetUserWordage(self):
        for case in test_cases["user_cases"]["success_cases"]:
            AssertRangeCase(jrt.user.GetUserWordage(case["url"]), case["wordage"])

        for case in test_cases["user_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.user.GetUserWordage(case["url"])

    def test_GetUserLikesCount(self):
        for case in test_cases["user_cases"]["success_cases"]:
            AssertRangeCase(jrt.user.GetUserLikesCount(case["url"]), case["likes_count"])

        for case in test_cases["user_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.user.GetUserLikesCount(case["url"])

    def test_GetUserAssetsCount(self):
        for case in test_cases["user_cases"]["success_cases"]:
            AssertRangeCase(jrt.user.GetUserAssetsCount(case["url"]), case["assets_count"])

        for case in test_cases["user_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.user.GetUserAssetsCount(case["url"])

    def test_GetUserFPCount(self):
        for case in test_cases["user_cases"]["success_cases"]:
            AssertRangeCase(jrt.user.GetUserFPCount(case["url"]), case["FP_count"])

        for case in test_cases["user_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.user.GetUserFPCount(case["url"])

    def test_GetUserFTNCount(self):
        for case in test_cases["user_cases"]["success_cases"]:
            AssertRangeCase(jrt.user.GetUserFTNCount(case["url"]), case["FTN_count"])

        for case in test_cases["user_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.user.GetUserFTNCount(case["url"])

    def test_GetUserBadgesList(self):
        for case in test_cases["user_cases"]["success_cases"]:
            AssertListCase(jrt.user.GetUserBadgesList(case["url"]), case["badges_list"])

        for case in test_cases["user_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.user.GetUserBadgesList(case["url"])

    def test_GetUserLastUpdateTime(self):
        for case in test_cases["user_cases"]["success_cases"]:
            AssertDatetimeCase(jrt.user.GetUserLastUpdateTime(case["url"]), case["last_update_time"])

        for case in test_cases["user_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.user.GetUserLastUpdateTime(case["url"])

    def test_GetUserNextAnniversaryDay(self):
        for case in test_cases["user_cases"]["success_cases"]:
            AssertDatetimeCase(jrt.user.GetUserNextAnniversaryDay(case["url"]), case["next_anniversary_day"])

        for case in test_cases["user_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.user.GetUserNextAnniversaryDay(case["url"])


class TestCollectionModule():
    def test_GetCollectionAvatarUrl(self):
        for case in test_cases["collection_cases"]["success_cases"]:
            AssertNormalCase(jrt.collection.GetCollectionAvatarUrl(case["url"]), case["avatar_url"])

        for case in test_cases["collection_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.collection.GetCollectionAvatarUrl(case["url"])

    def test_GetCollectionArticlesCount(self):
        for case in test_cases["collection_cases"]["success_cases"]:
            AssertRangeCase(jrt.collection.GetCollectionArticlesCount(case["url"]), case["articles_count"])

        for case in test_cases["collection_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.collection.GetCollectionArticlesCount(case["url"])

    def test_GetCollectionSubscribersCount(self):
        for case in test_cases["collection_cases"]["success_cases"]:
            AssertRangeCase(jrt.collection.GetCollectionSubscribersCount(case["url"]), case["subscribers_count"])

        for case in test_cases["collection_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.collection.GetCollectionSubscribersCount(case["url"])

    def test_GetCollectionArticlesUpdateTime(self):
        for case in test_cases["collection_cases"]["success_cases"]:
            AssertDatetimeCase(jrt.collection.GetCollectionArticlesUpdateTime(case["url"]), case["articles_update_time"])

        for case in test_cases["collection_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.collection.GetCollectionArticlesUpdateTime(case["url"])

    def test_GetCollectionInformationUpdateTime(self):
        for case in test_cases["collection_cases"]["success_cases"]:
            AssertDatetimeCase(jrt.collection.GetCollectionInformationUpdateTime(case["url"]), case["information_update_time"])

        for case in test_cases["collection_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.collection.GetCollectionInformationUpdateTime(case["url"])


class TestIslandModule():
    def test_GetArticleName(self):
        for case in test_cases["island_cases"]["success_cases"]:
            AssertNormalCase(jrt.island.GetIslandName(case["url"]), case["name"])

        for case in test_cases["island_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.island.GetIslandName(case["url"])

    def test_GetIslandAvatarUrl(self):
        for case in test_cases["island_cases"]["success_cases"]:
            AssertNormalCase(jrt.island.GetIslandAvatarUrl(case["url"]), case["avatar_url"])

        for case in test_cases["island_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.island.GetIslandAvatarUrl(case["url"])

    def test_GetIslandMembersCount(self):
        for case in test_cases["island_cases"]["success_cases"]:
            AssertRangeCase(jrt.island.GetIslandMembersCount(case["url"]), case["members_count"])

        for case in test_cases["island_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.island.GetIslandMembersCount(case["url"])

    def test_GetIslandPostsCount(self):
        for case in test_cases["island_cases"]["success_cases"]:
            AssertRangeCase(jrt.island.GetIslandPostsCount(case["url"]), case["posts_count"])

        for case in test_cases["island_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.island.GetIslandPostsCount(case["url"])

    def test_GetIslandCategory(self):
        for case in test_cases["island_cases"]["success_cases"]:
            AssertNormalCase(jrt.island.GetIslandCategory(case["url"]), case["category"])

        for case in test_cases["island_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.island.GetIslandCategory(case["url"])


class TestNotebookModule():
    def test_GetNotebookName(self):
        for case in test_cases["notebook_cases"]["success_cases"]:
            AssertNormalCase(jrt.notebook.GetNotebookName(case["url"]), case["name"])

        for case in test_cases["notebook_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.notebook.GetNotebookName(case["url"])

    def test_GetNotebookArticlesCount(self):
        for case in test_cases["notebook_cases"]["success_cases"]:
            AssertRangeCase(jrt.notebook.GetNotebookArticlesCount(case["url"]), case["articles_count"])

        for case in test_cases["notebook_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.notebook.GetNotebookArticlesCount(case["url"])

    def test_GetNotebookAuthorName(self):
        for case in test_cases["notebook_cases"]["success_cases"]:
            AssertNormalCase(jrt.notebook.GetNotebookAuthorInfo(case["url"])["name"], case["author_name"])

        for case in test_cases["notebook_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.notebook.GetNotebookAuthorInfo(case["url"])["name"]

    def test_GetNotebookAuthorAvatarUrl(self):
        for case in test_cases["notebook_cases"]["success_cases"]:
            AssertNormalCase(jrt.notebook.GetNotebookAuthorInfo(case["url"])["avatar_url"], case["author_avatar_url"])

        for case in test_cases["notebook_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.notebook.GetNotebookAuthorInfo(case["url"])["author_avatar_url"]

    def test_GetNotebookWordage(self):
        for case in test_cases["notebook_cases"]["success_cases"]:
            AssertRangeCase(jrt.notebook.GetNotebookWordage(case["url"]), case["wordage"])

        for case in test_cases["notebook_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.notebook.GetNotebookWordage(case["url"])

    def test_GetNotebookSubscribersCount(self):
        for case in test_cases["notebook_cases"]["success_cases"]:
            AssertRangeCase(jrt.notebook.GetNotebookSubscribersCount(case["url"]), case["subscribers_count"])

        for case in test_cases["notebook_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.notebook.GetNotebookSubscribersCount(case["url"])

    def test_GetNotebookUpdateTime(self):
        for case in test_cases["notebook_cases"]["success_cases"]:
            AssertDatetimeCase(jrt.notebook.GetNotebookUpdateTime(case["url"]), case["update_time"])

        for case in test_cases["notebook_cases"]["fail_cases"]:
            with pytest.raises(error_text_to_obj[case["exception_name"]]):
                jrt.notebook.GetNotebookUpdateTime(case["url"])


if __name__ == "__main__":
    pytest.main(args=["-n 4"])  # 运行测试
