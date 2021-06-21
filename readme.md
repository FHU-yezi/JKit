# 项目简介

> 科技赋能创作星辰。

JRT 是一个简书数据获取与分析库，致力于用更简单的方式，帮助有编程基础的用户快速进行数据分析，助力社区成长。

同时，它提供了一系列的接口，可以与其它数据科学库实现对接，亦可用来快速构建数据可视化应用。

该项目基于简书网页官方接口。

# 安装与使用

JRT 已上传到 PyPi，可使用以下命令一键安装：

```
pip install JianshuResearchTools
```

您可运行以下代码示例，确保 JRT 在您的设备上安装成功：

```python
import JianshuResearchTools as jrt
print(jrt.GetUserName("https://www.jianshu.com/u/ea36c8d8aa30"))
```

如果一切正常，您会看到输出“初心不变_叶子”。

# 依赖库

## 必须依赖

- requests：用于实现网络请求
- lxml：用于实现基于 Xpath 的 HTML 解析

## 可选依赖

括号中内容为依赖此库的模块名，如您不需要用到它们，可不下载这些依赖库。

- (data_output) pandas：用于将数据导出到 Pandas DataFrame
- (prediction) scikit-learn：用于进行数据预测
- (plot) matplotlib：用于绘制图表

# 贡献

详见贡献指南文件。（CONTRIBUTING.md）