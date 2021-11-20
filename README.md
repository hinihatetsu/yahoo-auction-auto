# ヤフオク！のタスクを自動化

## 必要条件

- Python3.9以上
- Google Chrome or Chromium

## インストール
```
pip install yahoo-auction-auto
```

## 使用例
このパッケージでは廃止された公式APIの代わりにcookieを使ってセッションを取得する。
そのために、初めにcookieをファイルに書き出す。

```python
from yahoo_auction.cookie import get_cookies
import json

cookies = get_cookies()

with open('cookies.json', 'w') as f:
    json.dump(cookies, f)
```

書き出したcookieを使用して、出品情報を取得する。

```python
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
```

## API



## LICESE
MIT LICENSE