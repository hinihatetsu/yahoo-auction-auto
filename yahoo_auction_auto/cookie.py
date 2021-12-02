import time
from typing import Any
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from .chrome import chrome
from .urls import YahooAuctionURL

def get_cookies() -> list[dict[str, Any]]:
    _, cookies = get_username_and_cookies()
    return cookies
    


def get_username_and_cookies() -> tuple[str, list[dict[str, Any]]]:
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])

    with chrome(options) as driver:
        driver.get(YahooAuctionURL.MYPAGE)
        while True:
            if driver.current_url == YahooAuctionURL.MYPAGE:
                break
            time.sleep(1)
        username = driver. \
            find_element_by_class_name('yjmthloginarea'). \
            find_element(By.TAG_NAME, 'strong'). \
            text
        cookies = driver.get_cookies()
    return username, cookies




