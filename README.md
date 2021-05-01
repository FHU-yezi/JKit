> 科技赋能创作星辰。

Jianshu-Research-Tools（简书研究工具）是一个数据获取与分析库。我们将底层的数据获取过程抽象成接口，供有 Python 数据分析能力的用户快速调用，通过数据分析驱动社区成长。

# 功能一览

- 获取用户 ID、昵称、徽章、关注数、粉丝数等基础数据
- 获取用户关注与粉丝列表
- 获取用户文章列表
- 获取用户总资产、简书钻、简书贝等资产数据
- 获取贝壳小岛买卖挂单列表和最新价格数据
- 获取资产排行榜和日更排行榜信息
- 获取专题基础信息
- 获取文章基础信息
- 更多......

# 即将实现

- 获取用户的简书周年纪念日期

# 快速上手

## 自动安装

执行以下命令：

```
pip install JianshuResearchTools
```

全部依赖库将被自动安装。

## 手动安装

JRT 的依赖库如下：

- bs4：用于 HTML 解析与提取
- Requests：用于发起网络请求。

如果您没有安装依赖库，使用 JRT 时会出现异常。您可以执行以下代码自动安装依赖库：

```
pip install bs4
pip install requests
```

请从[版本页面](https://github.com/FHU-yezi/JianshuResearchTools/releases)下载最新版本的 JRT，并将其解压后放置到您的项目根目录。不要更改文件名，否则将造成导入失败。

之后，您可以通过以下几行代码获取一位用户的昵称，并将其显示出来。

```python
import JianshuResearchTools as jrt

result = jrt.GetUserName("https://www.jianshu.com/u/ea36c8d8aa30")

print(result)
```

如果一切顺利，输出结果应是“初心不变_叶子“。

感谢您使用 JRT。