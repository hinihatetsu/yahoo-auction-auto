import re
from datetime import datetime
from typing import Optional, Pattern

import requests_async as requests
import bs4

from yahoo_auction_auto.urls import YahooAuctionURL

class InfoSelling:
    aID: str
    title: str
    seller_name: str
    stack: int
    start_datetime: datetime
    end_datetime: datetime
    refundable: bool
    startprice: str
    timeleft: str
    count_bid: int
    count_access: int
    count_watch: int


    def __init__(self, aID: str) -> None:
        self.aID = aID

    
    async def update(self, cookies: dict[str, str], timeout: int=60) -> None:
        url: str = YahooAuctionURL.AUCTION(self.aID)
        response: requests.Response = await requests.get(url, cookies=cookies, timeout=timeout)
        response.raise_for_status()
        soup: bs4.BeautifulSoup = bs4.BeautifulSoup(response.content, 'lxml')

        self.title = _get_title(soup)
        self.seller_name = _get_seller_name(soup)
        self.stack = _get_stack(soup)
        self.start_datetime = _get_start_datetime(soup)
        self.end_datetime = _get_end_datetime(soup)
        self.refundable = _get_refundable(soup)
        self.startprice = _get_startprice(soup)
        self.timeleft = _get_timeleft(soup)
        self.count_bid = _get_count_bid(soup)
        self.count_access = _get_count_access(soup)
        self.count_watch = _get_count_watch(soup)



# scraping functions
# soup is from YahooAuctionURL.AUCTION()
def _get_title(soup: bs4.BeautifulSoup) -> str:
    """ Return product title from `soup`. 
    
    Parameters
    ----------
    soup : bs4.BeautifulSoup
        Soup of a Yahoo Auction page.

    Returns
    -------
    str
        Product title.

    """
    titles: bs4.element.ResultSet = soup.find_all('h1', {'class': 'ProductTitle__text'})
    if len(titles) > 0:
        return str(titles[0].text)
    else:
        return ''


def _get_seller_name(soup: bs4.BeautifulSoup) -> str:
    """ Return seller name from `soup`. 
    
    Parameters
    ----------
    soup : bs4.BeautifulSoup
        Soup of a Yahoo Auction page.

    Returns
    -------
    str
        Seller name.

    """
    pattern: Pattern[str] = re.compile(r'^rsec:seller;slk:slfinfo;')
    seller_names = soup.find_all('a', {'data-ylk': pattern})
    if len(seller_names) > 0:
        return str(seller_names[0].text)
    else:
        return ''


def _get_stack(soup: bs4.BeautifulSoup) -> int:
    """ Return stack count of product from  `soup`. 
    
    Parameters
    ----------
    soup : bs4.BeautifulSoup
        Soup of a Yahoo Auction page.

    Returns
    -------
    int
        Stack count.

    """
    tag: Optional[bs4.element.Tag] = soup.find('dt', text='個数'). \
        find_next_sibling('dd', {'class': 'ProductDetail__description'})
    return int(tag.text[1:]) if tag else 0


def _from_yahoo_datetime(datetimestr: str) -> datetime:
    """ From format `YYYY.MM.DD（d）HH:MM 
    
    Parameters
    ----------
    datetimestr : str
        String of datetime on a Yahoo Auction page.

    Returns
    -------
    datetime
    """
    year: int = int(datetimestr[:4])
    month: int = int(datetimestr[5:7])
    day: int = int(datetimestr[8:10])
    hour: int = int(datetimestr[13:15])
    min: int = int(datetimestr[16:18])
    return datetime(year, month, day, hour, min)


def _get_start_datetime(soup: bs4.BeautifulSoup) -> datetime:
    """ Return start datetime of the auction from `soup`. 
    
    Parameters
    ----------
    soup : bs4.BeautifulSoup
        Soup of a Yahoo Auction page.

    Returns
    -------
    datetime
        Start datetime.

    """
    tag: bs4.element.Tag = soup.find('dt', text='開始日時'). \
        find_next_sibling('dd', {'class': 'ProductDetail__description'})
    return _from_yahoo_datetime(tag.text[1:])


def _get_end_datetime(soup: bs4.BeautifulSoup) -> datetime:
    """ Return end datetime of the auction from `soup`. 
    
    Parameters
    ----------
    soup : bs4.BeautifulSoup
        Soup of a Yahoo Auction page.

    Returns
    -------
    datetime
        End datetime.

    """
    tag: bs4.element.Tag = soup.find('dt', text='終了日時'). \
        find_next_sibling('dd', {'class': 'ProductDetail__description'})
    return _from_yahoo_datetime(tag.text[1:])


def _get_refundable(soup: bs4.BeautifulSoup) -> bool:
    """ Return True if the product of `soup` is refundable. 
    
    Parameters
    ----------
    soup : bs4.BeautifulSoup
        Soup of a Yahoo Auction page.

    Returns
    -------
    bool
        Return True if the product of `soup` is refundable.

    """
    tag: bs4.element.Tag = soup.find('dt', text='返品'). \
        find_next_sibling('dd', {'class': 'ProductDetail__description'})
    return bool(tag.text[1:] != '返品不可')


def _get_startprice(soup: bs4.BeautifulSoup) -> str:
    """ Return start price from `soup`. 
    
    Parameters
    ----------
    soup : bs4.BeautifulSoup
        Soup of a Yahoo Auction page.

    Returns
    -------
    str
        Start price. e.g. 10,000 円（税 0 円）
    """
    tag: bs4.element.Tag = soup.find('dt', text='開始価格'). \
        find_next_sibling('dd', {'class': 'ProductDetail__description'})
    return str(tag.text[1:])


def _get_timeleft(soup: bs4.BeautifulSoup) -> str:
    """ Return timeleft from `soup`. 
    
    Parameters
    ----------
    soup : bs4.BeautifulSoup
        Soup of a Yahoo Auction page.

    Returns
    -------
    str
        String of timeleft.
    """
    tag: bs4.element.Tag = soup.find('dt', text='残り時間'). \
        find_next_sibling('dd', {'class': 'Count__number'})
    return str(tag.text.splitlines()[0])


def _get_count_bid(soup: bs4.BeautifulSoup) -> int:
    """ Return bidding count from `soup`. 
    
    Parameters
    ----------
    soup : bs4.BeautifulSoup
        Soup of a Yahoo Auction page.

    Returns
    -------
    int
        Count of total bidding.
    """
    tag: bs4.element.Tag = soup.find('dt', text='入札件数'). \
        find_next_sibling('dd', {'class': 'Count__number'})
    return int(tag.text[:-4])


def _get_count_access(soup: bs4.BeautifulSoup) -> int:
    """ Return access count from `soup`. 
    
    Parameters
    ----------
    soup : bs4.BeautifulSoup
        Soup of a Yahoo Auction page.

    Returns
    -------
    int
        Count of access.
    """
    tag: bs4.element.Tag = soup.find('span', {'class': 'StatisticsInfo__term--access'}). \
        find_next_sibling('span', {'class': 'StatisticsInfo__data'})
    return int(tag.text)


def _get_count_watch(soup: bs4.BeautifulSoup) -> int:
    """ Return watch count from `soup`. 
    
    Parameters
    ----------
    soup : bs4.BeautifulSoup
        Soup of a Yahoo Auction page.

    Returns
    -------
    int
        Count of watch.
    """
    tag: bs4.element.Tag = soup.find('span', {'class': 'StatisticsInfo__term--watch'}). \
        find_next_sibling('span', {'class': 'StatisticsInfo__data'})
    return int(tag.text)