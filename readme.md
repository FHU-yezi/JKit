# 项目简介

![许可证 Badge](https://img.shields.io/github/license/fhu-yezi/JianshuResearchTools?color=%234263eb&label=%E8%AE%B8%E5%8F%AF%E8%AF%81)

![代码库大小 Badge](https://img.shields.io/github/repo-size/fhu-yezi/JianshuResearchTools?color=%2352c41a&label=%E4%BB%A3%E7%A0%81%E5%BA%93%E5%A4%A7%E5%B0%8F)

![GitHub 最新版本 Badge](https://img.shields.io/github/v/release/fhu-yezi/JianshuResearchTools?color=%233339af0&label=GitHub%20%E6%9C%80%E6%96%B0%E7%89%88%E6%9C%AC)

![PyPI 最新版本 Badge](https://img.shields.io/pypi/v/JianshuResearchTools?color=%233339af0&label=PyPI%20%E6%9C%80%E6%96%B0%E7%89%88%E6%9C%AC)

![Github Release 总下载量 Badge](https://img.shields.io/github/downloads/fhu-yezi/JianshuResearchTools/total?color=%23c41d7f&label=GitHub%20%E6%80%BB%E4%B8%8B%E8%BD%BD%E9%87%8F)

![PyPI 月下载量 Badge](https://img.shields.io/pypi/dm/JianshuResearchTools?color=%23597ef7&label=PyPI%20%E6%9C%88%E4%B8%8B%E8%BD%BD%E9%87%8F)

![打开的 Issues 数量 Badge](https://img.shields.io/github/issues-raw/fhu-yezi/JianshuResearchTools?color=%23339af0&label=%E6%89%93%E5%BC%80%E7%9A%84%20Issues%20%E6%95%B0%E9%87%8F)

> 科技赋能创作星辰。

JRT 是一个简书数据获取与分析库，致力于用更简单的方式，帮助有编程基础的用户快速进行数据分析，助力社区成长。

该库基于简书官方接口。

# 安装

## 自动安装

JRT 已上传到 PyPI，可使用以下命令自动安装：

```
pip install JianshuResearchTools
```

## 手动安装

您亦可以手动下载项目源代码，使用 `setup.py` 将其安装到您的设备上。

同时，您还需要运行以下命令，下载 JRT 的依赖库：

```
pip install requests lxml
```

您可运行以下代码示例，确认 JRT 已在您的设备上正常安装：

```python
import JianshuResearchTools as jrt
print(jrt.__version__)
```

如果一切正常，您会看到 JRT 的版本号。

# 快速上手

## 函数调用

示例一，获取用户昵称：

```python
>>> import JianshuResearchTools as jrt
>>> jrt.user.GetUserName("https://www.jianshu.com/u/ea36c8d8aa30")
'初心不变_叶子'
```

示例二，获取文章标题：

```python
>>> import JianshuResearchTools as jrt
>>> jrt.article.GetArticleTitle("https://www.jianshu.com/p/2c2b76a1d0ae")
'你好，简书贝'
```

## 面向对象

示例一，获取用户昵称：

```python
>>> import JianshuResearchTools as jrt
>>> user = jrt.objects.User("https://www.jianshu.com/u/ea36c8d8aa30") 
>>> user.name
'初心不变_叶子'
```

示例二，获取用户信息摘要：
```python
>>> import JianshuResearchTools as jrt
>>> user = jrt.objects.User("https://www.jianshu.com/u/ea36c8d8aa30")            
>>> print(user)
用户信息摘要：
用户名：初心不变_叶子
性别：男
关注数：325
粉丝数：822
文章数：120
总字数：245295
被点赞数：4030
总资产：18000.0
简书钻：10156.544
简书贝：7843.456
会员等级：None
会员过期时间：None
```

# 依赖库

## 必须依赖

- httpx：用于实现网络请求
- lxml：用于实现基于 Xpath 的 HTML 解析

## 可选依赖

- ujson：安装后在大量数据获取场景将获得一定性能提升
- tomd：安装后可以使用`jrt.article.GetArticleMarkdown()`函数获取 Markdown 格式的文章内容

# 贡献

详见贡献指南文件。（CONTRIBUTING.md）