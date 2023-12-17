# JKit

[![许可证](https://img.shields.io/github/license/FHU-yezi/JKit?style=flat-square&label=%E8%AE%B8%E5%8F%AF%E8%AF%81)](https://github.com/FHU-yezi/JKit/blob/v3/LICENSE)
[![简书主页](https://img.shields.io/badge/%E7%AE%80%E4%B9%A6-%E5%88%9D%E5%BF%83%E4%B8%8D%E5%8F%98__%E5%8F%B6%E5%AD%90-black?style=flat-square&color=EA6F5A)](https://www.jianshu.com/u/ea36c8d8aa30)

[![PyPI 最新版](https://img.shields.io/pypi/v/jkit?style=flat-square&label=PyPI)
](https://pypi.python.org/pypi/jkit)
[![支持的 Python 版本](https://img.shields.io/pypi/pyversions/jkit.svg?style=flat-square&label=Python%20%E7%89%88%E6%9C%AC)](https://pypi.python.org/pypi/jkit)

[![Ruff](https://img.shields.io/badge/%E9%9D%99%E6%80%81%E6%A3%80%E6%9F%A5-Ruff-purple?style=flat-square)
](https://github.com/astral-sh/ruff)
[![Pyright](https://img.shields.io/badge/%E7%B1%BB%E5%9E%8B%E6%A3%80%E6%9F%A5-Pyright-blue?style=flat-square)
](https://github.com/microsoft/pyright)
[![Black](https://img.shields.io/badge/%E4%BB%A3%E7%A0%81%E9%A3%8E%E6%A0%BC-Black-black?style=flat-square)
](https://github.com/psf/black)


<p align="center">
  <b>创造可能性。</b>
</p>

> [!WARNING]
> JKit v3 正在 Alpha 测试中，可能随时进行重大变更。

# 快速上手

```bash
pip install jkit --pre
```

```python
from asyncio import run as asyncio_run

from jkit import User


async def main() -> None:
    user = User.from_url("https://www.jianshu.com/u/622a3993108c")
    print(f"用户昵称：{await user.name}")  # == (await user.info).name

    info = await user.info
    print(
        f"性别：{info.gender.value}，会员等级：{info.membership_info.type.value}\n"
        f"会员过期时间：{info.membership_info.expired_at}"
    )


asyncio_run(main())

```

```
用户昵称：任真
性别：女，会员等级：白金会员
会员过期时间：2024-04-12 14:24:24
```

# 亮点

- [x] 完全异步操作
- [x] 基于 [msgspec](https://github.com/jcrist/msgspec) 的数据模型和自动校验