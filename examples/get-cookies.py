from yahoo_auction_auto.cookie import get_cookies
import json

cookies: dict[str, str] = get_cookies()

with open('cookies.json', 'w') as f:
    json.dump(cookies, f)