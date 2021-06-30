# 贡献指南

## Issue

### 上报 Bug

一个良好的 Bug Report Issue 应该包括以下部分：

**运行环境**（操作系统、Python 版本、JRT 版本、依赖库版本）。

以下是一个示例：

- 操作系统：Windows 10 专业版 内部版本号 2004
- Python ：Python 3.8.10 64-bit
- JRT：v2.0.0
- 依赖库：
    - requests 2.25.1
    - lxml 4.6.3

**您执行的代码**

这段代码应是最小可运行的、可以反映出问题的示例，请去除无关的逻辑部分。

如果复现这个问题需要引入其它库，请说明这些库的版本。

示例：

```python
import JianshuResearchTools as jrt

print(jrt.user.GetUserName("https://www.jianshu.com/u/ea36c8d8aa30/"))
```

**输出结果**

示例：

```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "D:\Python\lib\site-packages\JianshuResearchTools\main.py", line 56, in GetUserName
    html = requests.get(user_url, headers=UA)
  File "D:\Python\lib\site-packages\requests\api.py", line 76, in get
    return request('get', url, params=params, **kwargs)
  File "D:\Python\lib\site-packages\requests\api.py", line 61, in request
    return session.request(method=method, url=url, **kwargs)
  File "D:\Python\lib\site-packages\requests\sessions.py", line 542, in request
    resp = self.send(prep, **send_kwargs)
  File "D:\Python\lib\site-packages\requests\sessions.py", line 655, in send
    r = adapter.send(request, **kwargs)
  File "D:\Python\lib\site-packages\requests\adapters.py", line 439, in send
    resp = conn.urlopen(
  File "D:\Python\lib\site-packages\urllib3\connectionpool.py", line 696, in urlopen
    self._prepare_proxy(conn)
  File "D:\Python\lib\site-packages\urllib3\connectionpool.py", line 964, in _prepare_proxy
    conn.connect()
  File "D:\Python\lib\site-packages\urllib3\connection.py", line 359, in connect
    conn = self._connect_tls_proxy(hostname, conn)
  File "D:\Python\lib\site-packages\urllib3\connection.py", line 500, in _connect_tls_proxy
    return ssl_wrap_socket(
  File "D:\Python\lib\site-packages\urllib3\util\ssl_.py", line 432, in ssl_wrap_socket
    ssl_sock = _ssl_wrap_socket_impl(sock, context, tls_in_tls)
  File "D:\Python\lib\site-packages\urllib3\util\ssl_.py", line 474, in _ssl_wrap_socket_impl
    return ssl_context.wrap_socket(sock)
  File "D:\Python\lib\ssl.py", line 500, in wrap_socket
    return self.sslsocket_class._create(
  File "D:\Python\lib\ssl.py", line 997, in _create
    raise ValueError("check_hostname requires server_hostname")
ValueError: check_hostname requires server_hostname
```

**您认为正确的输出**

示例：

```
'初心不变_叶子'
```

**该 Bug 的分类**

可选的分类如下：

- 报错、无法运行
- 数据错误
- 输出类型错误
- 速度异常
- 影响其它库 / 系统的正常使用

示例：

```markdown
- [x] 报错、无法运行
- [ ] 数据错误
- [ ] 输出类型错误
- [ ] 速度异常
- [ ] 影响其它库 / 系统的正常使用
```

**该问题是否紧急**

如果该问题紧急，请勾选”是“，该问题将被标记为高优先级，并得到更快的处理。

**请注意，我们并不对处理速度做出保证。** 但我们会尽全力处理您的问题，尽量不让您的使用受到影响。

**滥用紧急问题将被禁止添加 Issue。**

**联系方式**

可选的联系方式如下：

- 邮箱
- 微信
- QQ

如果您不预留联系方式，问题有新的进展时将在 Issue 中评论告知您，请注意保持该 Issue 处于 Watch 状态。

### 功能建议

**功能建议类别**

- 增加新功能
- 优化速度
- 优化返回数据
- 与其它库对接
- 提升用户体验

示例：

```markdown
- [x] 增加新功能
- [ ] 优化速度
- [ ] 优化返回数据
- [ ] 与其它库对接
- [ ] 提升用户体验
```

**简要描述该功能**

示例：

增加获取贝壳小岛挂单信息的函数

**提出该建议的原因**（可选）

示例：

助力对简书资产交易的分析

**实现思路**（可选）

如果您已经有较为成熟的技术思路，请在此简要叙述，如果有代码也请一并留下，以备参考。

如果有接口可以使用，请说明以下信息：

- 接口链接
- 请求方式
- 参数
- 返回值

示例：

思路：通过解析接口返回的 Json 数据实现。

接口：https://www.beikeisland.com/api/Trade/getTradeList

请求方式：POST

参数：

- pageIndex：整数，页码
- retype：整数，1 为卖单，2 为买单

返回值：

（略）

**联系方式**

可选的联系方式如下：

- 邮箱
- 微信
- QQ

如果您不预留联系方式，问题有新的进展时将在 Issue 中评论告知您，请注意保持该 Issue 处于 Watch 状态。

## Pull Request

### 我们接收何种类型的 PR

- 对新功能的实现
- 对已有功能的改进
- 对 Bug 的修复

### 开发指南

请从 [FHU-yezi/JianshuResearchTools](https://github.com/FHU-yezi/JianshuResearchTools) Fork 存储库，然后将您 Fork 的库 clone 到本地。

存储库下载到本地后，请执行 `git switch dev` 切换到开发分支，在主分支上进行开发的 PR 将被拒绝。

开发时请注意遵守代码规范。本项目基本遵循 PEP8 规范，对单行字符数的限制除外。

请书写与现有注释格式一致的函数注释。如果您使用 VS Code 进行开发，建议下载 Python Docstring Generator 扩展。

进行提交时，请遵循项目原有的提交信息书写规范，在每条提交信息前加入分类：

- feat - 新功能 feature
- fix - 修复 bug
- docs - 文档注释
- style - 代码格式(不影响代码运行的变动)
- refactor - 重构、优化(既不增加新功能，也不是修复bug)
- perf - 性能优化
- test - 增加测试
- chore - 构建过程或辅助工具的变动
- revert - 回退
- build - 打包

分类和提交信息间用一个中文冒号进行分隔，两边不加空格。

您可自行决定是否将您开发过程中的提交合并到一个提交。

完成开发后，**不要**将 dev 分支 merge 到 main。

之后，请运行单元测试，确保所有测试用例通过。

将全部本地代码 Push 到您 Fork 的存储库，之后提交 Pull Request。

### Pull Request 规范

Pull Request 应包含以下内容：

**分类**

- 对新功能的实现
- 对已有功能的改进
- 对 Bug 的修复

**简述此次更改**

每个 Pull Request 应只围绕一个主题展开。

**具体更改**

例如：重写了某个函数、增加了某个函数
