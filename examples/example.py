from yahoo_auction import YahooAuction
import asyncio
import json
from pprint import pprint


async def main():
    with open('cookies.json') as f:
        cookies = json.load(f)

    ya = YahooAuction(cookies=cookies)
    aIDs: list[str] = await ya.get_urls_selling() # 出品中のaIDを全て取得する
    pprint(aIDs)

    for aID in aIDs[:3]:
        info = await ya.get_info_selling(aID) # 出品中の情報を取得する。
        pprint(info.__dict__)


if __name__ == '__main__':
    asyncio.run(main())