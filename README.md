# JKit

[![许可证](https://img.shields.io/github/license/FHU-yezi/JKit?style=flat-square&label=%E8%AE%B8%E5%8F%AF%E8%AF%81)](https://github.com/FHU-yezi/JKit/blob/v3/LICENSE)
[![PyPI 版本](https://img.shields.io/pypi/v/jkit?style=flat-square&label=PyPI)
](https://pypi.python.org/pypi/jkit)
[![支持的 Python 版本](https://img.shields.io/pypi/pyversions/jkit?style=flat-square&label=%E6%94%AF%E6%8C%81%E7%9A%84%20Python%20%E7%89%88%E6%9C%AC)](https://endoflife.date/python)

[![静态分析 Ruff](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fastral-sh%2Fruff%2Fmain%2Fassets%2Fbadge%2Fv2.json&style=flat-square&label=%E9%9D%99%E6%80%81%E5%88%86%E6%9E%90)](https://github.com/astral-sh/ruff)
[![类型检查](https://img.shields.io/badge/%E7%B1%BB%E5%9E%8B%E6%A3%80%E6%9F%A5-Pyright-blue?style=flat-square)](https://github.com/microsoft/pyright)
[![代码风格 Ruff](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fastral-sh%2Fruff%2Fmain%2Fassets%2Fbadge%2Fv2.json&style=flat-square&label=%E4%BB%A3%E7%A0%81%E9%A3%8E%E6%A0%BC)](https://github.com/astral-sh/ruff)


<p align="center">
  <b>创造可能性。</b>
</p>

> [!WARNING]
> JKit v3 正在 Beta 测试中，可能随时进行重大变更。

> [!WARNING]
> JKit 为非官方 SDK，可能因相关 API 变动导致功能异常。

# 功能

- 简书文章 / 用户 / 专题 / 文集标识符（ID / Slug / URL）校验与转换
- 获取简书文章、用户、专题、文集数据
- 获取简书资产数据、钻贝变动记录、持钻奖励数据、收益加成卡数据
- 获取简书会员分销链接
- 钻贝互转
- 获取简书积分兑换平台贝市场订单数据
- 获取贝交易平台贝市场订单数据

（部分功能需要鉴权凭证）

# 安装

JKit 需要 Python 3.9 及以上版本。

PyPy 等其它 Python 实现可能运行，但不受支持。

```bash
pip install jkit
```

# 快速上手

JKit 仅支持异步操作。

```python
import asyncio

from jkit.user import User


async def main() -> None:
    user = User.from_slug("ea36c8d8aa30")

    info = await user.info

    print("ID:", info.id)
    print("URL:", user.url)
    print("昵称:", info.name)


asyncio.run(main())
```

```
ID: 19867175
URL: https://www.jianshu.com/u/ea36c8d8aa30
昵称: 初心不变_叶子
```

# 获取凭证

## 简书

**目前仅支持从电脑端获取凭证。**

在浏览器中登录简书账号。

打开开发者工具（DevTools）- 存储（Storages）选项卡- Cookie，`remember_user_token` 对应的值即为凭证。

使用示例：

```python
import asyncio

from jkit.credentials import JianshuCredential
from jkit.private.assets_wallet import AssetsWallet

TOKEN = "<YOUR_TOKEN>"


async def main() -> None:
    credential = JianshuCredential.from_remember_user_token(TOKEN)
    assets_wallet = AssetsWallet(credential=credential)

    print(await assets_wallet.assets_info)


asyncio.run(main())
```

```
AssetsInfoData(
    fp_amount=Decimal('88987.0378258294950'),
    ftn_amount=Decimal('7860.19387826272668'),
    assets_amount=Decimal('96847.2317040922062'),
    converting_fp_amount=Decimal('8.46199999999999974')
)
```

## 贝交易平台

在浏览器中登录贝交易平台账号。

打开开发者工具（DevTools）- 控制台（Console）选项卡，执行以下代码：

```javascript
JSON.parse(window.localStorage.app_user_token).token
```

输出内容即为凭证。（不包含引号）

使用示例：

```python
import asyncio

from jkit.beijiaoyi.ftn_macket import FtnMacket
from jkit.credentials import BeijiaoyiCredential

TOKEN = "<YOUR_TOKEN>"


async def main() -> None:
    credential = BeijiaoyiCredential.from_bearer_token(TOKEN)
    ftn_macket = FtnMacket(credential=credential)

    async for item in ftn_macket.iter_orders(type="BUY"):
        print(item)
        return


asyncio.run(main())
```

```
OrderData(
    id=1893596965401399296,
    price=0.046,
    total_amount=10000,
    traded_amount=0,
    tradable_amount=10000,
    minimum_trade_amount=1000,
    maximum_trade_amount=None,
    completed_trades_count=0,
    publish_time=datetime.datetime(2025, 2, 23, 17, 41, 12),
    supported_payment_channels=('WECHAT_PAY', 'ALIPAY'),
    publisher_info=_PublisherInfoField(
        id=3513,
        name='eQn8ME9fnt',
        avatar_url='https://testapi.beijiaoyi.com/Upload/headimg/13.png'
    )
)
```