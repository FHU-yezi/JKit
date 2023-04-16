from httpx import Client

client = Client(http2=True, timeout=5)
