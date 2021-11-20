from contextlib import contextmanager
from typing import Iterator
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import chromedriver_binary


@contextmanager
def chrome(options: Options) -> Iterator[Chrome]:
    driver: Chrome = Chrome(options=options)
    driver.implicitly_wait(30)
    try:
        yield driver
    finally:
        driver.close()
        driver.quit()