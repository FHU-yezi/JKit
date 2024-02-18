import asyncio

from jkit.notebook import Notebook


async def main() -> None:
    notebook = Notebook.from_id(40458256)

    async for item in notebook.iter_articles(
        start_page=2, order_by="last_comment_time"
    ):
        print(item.id, end="\t")


asyncio.run(main())
