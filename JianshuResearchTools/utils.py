from typing import Any, Dict, Tuple, Callable

__all__ = ["NameValueMappingToString", "CallWithoutCheck"]


def NameValueMappingToString(mapping: Dict[str, Tuple[Any, bool]], title: str = "") -> str:
    """将字典转换成特定格式的字符串

    Args:
        mapping (Dict[str, Tuple[Any, bool]]): 键为属性名，值为 (属性值, 是否换行) 的字典
        title (str, optional): 标题. Defaults to "".

    Returns:
        str: 供 __str__ 方法返回的字符串
    """
    result_lst = []
    for key, (value, new_line) in mapping.items():
        # 如果需要换行，则在字符串前添加换行符
        value = "\n" + value if new_line else value
        result_lst.append(f"{key}: {value}")

    # 如果有标题，则拼接标题并在后面加入一个换行符，然后拼接属性字符串
    return "\n".join((f"{title}：", *result_lst)) if title else "\n".join(result_lst)


def CallWithoutCheck(func: Callable, *args: Any, **kwargs: Any) -> Any:
    """调用函数，并自动禁用函数的参数检查。

    通过向参数列表注入关键字参数 disable_check=True 实现
    如果函数不支持禁用参数检查，会抛出 AttributeError 异常

    Args:
        func (Callable): 待调用的函数

    Returns:
        Any: 函数返回值
    """
    return func(*args, **kwargs, disable_check=True)
