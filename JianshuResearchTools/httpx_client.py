from httpx import Client

from JianshuResearchTools.headers import API_HEADER, MOBILE_HEADER, PC_HEADER

JIANSHU_API_CLIENT = Client(
    http2=True,
    timeout=5,
    base_url="https://www.jianshu.com",
    headers=API_HEADER,
)
JIANSHU_PC_CLIENT = Client(
    http2=True,
    timeout=5,
    base_url="https://www.jianshu.com",
    headers=PC_HEADER,
)
JIANSHU_MOBILE_CLIENT = Client(
    http2=True,
    timeout=5,
    base_url="https://www.jianshu.com",
    headers=MOBILE_HEADER,
)
