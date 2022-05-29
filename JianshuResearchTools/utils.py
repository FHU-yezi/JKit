from typing import Any, Dict, Tuple


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
