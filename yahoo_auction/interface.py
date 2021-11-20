import re
import logging
from typing import Optional, Any, Pattern

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
import requests_async as requests 
import bs4

from yahoo_auction.chrome import chrome
from yahoo_auction.urls import YahooAuctionURL
from yahoo_auction.info.selling import InfoSelling
from yahoo_auction.info.closed_with_winner import InfoClosedWithWinner
from yahoo_auction.info.closed_without_winner import InfoClosedWithoutWinner

logger = logging.getLogger(__name__)

class YahooAuction:

    def __init__(
        self, 
        cookies: list[dict[str, Any]],
        headless: bool = True
    ) -> None:
        """ 
        Parameters
        ----------
        cookies : dict[str, str]
            Cookies to get session.
        """
        self.cookies: list[dict[str, Any]] = cookies
        self._cookies: dict[str, str] = {cookie['name']: cookie['value'] for cookie in cookies} # for requests module
        self._chrome_options: Options = Options()
        self._chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        if headless:
            self._chrome_options.add_argument('--headless')

    
    async def check_login(self) -> bool:
        """ Return True if logined. 
        
        Returns
        -------
        bool
            Return True if logined.
        """
        url: str = YahooAuctionURL.MYPAGE
        try:
            response: requests.Response = await requests.get(url, cookies=self._cookies, timeout=60)
            response.raise_for_status()
        except Exception:
            return False
        
        return bool(response.url == url)


    def submit(self) -> None:
        """ Submit product on Yahoo Auction page. 

        Not Impremented yet.
        """
        raise NotImplementedError()



    def cancel(self, aID: str) -> None:
        """ Cancel selling. 
        
        Parameters
        ----------
        aID
            Auction ID of Yahoo Auction.
        """
        with chrome(self._chrome_options) as driver:
            driver.get(YahooAuctionURL.HOME)
            for cookie in self.cookies:
                driver.add_cookie(cookie)
            driver.get(YahooAuctionURL.CANCEL(aID))
            cancel_element: WebElement = driver.find_element_by_name('confirm')
            cancel_element.click()
            
            
    def cancel_items(self, aIDs: list[str]) -> list[str]:
        canceled: list[str] = []
        with chrome(self._chrome_options) as driver:
            driver.get(YahooAuctionURL.HOME)
            for cookie in self.cookies:
                driver.add_cookie(cookie)
            for aID in aIDs:
                try:
                    logger.debug(f'canceling {aID}')
                    driver.get(YahooAuctionURL.CANCEL(aID))
                    cancel_element: WebElement = driver.find_element_by_name('confirm')
                    cancel_element.click()
                    canceled.append(aID)
                except Exception as e:
                    logger.error(e)
        return canceled


    def resubmit(self, aID: str) -> None:
        """ Resubmit product. 
        
        Not Inpremented yet
        """
        raise NotImplementedError()
                 
        
    async def get_aIDs_selling(self) -> list[str]:
        """ Get aIDs currently selling on Yahoo Auction page. 
        
        Returns
        -------
        list[str]
            List of aIDs.
        """
        urls: list[str] = await self.get_urls_selling()
        aIDs: list[str] = []
        for url in urls:
            match = re.search(r'(?<=/)\w+$', url)
            if match:
                aIDs.append(url[match.start():match.end()])
        return aIDs


    async def get_urls_selling(self) -> list[str]:
        """ Get URLs currently selling on Yahoo Auction page. 
        
        Returns
        -------
        list[str]
            List of URLs.
        """
        pattern: Pattern[str] = re.compile(r'^rsec:itm;slk:tc;')
        return await _get_urls(self._cookies, YahooAuctionURL.SELLING, pattern)


    async def get_info_selling(self, aID: str) -> InfoSelling:
        """ Get product information of `aID`. 
        
        Parameters
        ----------
        aID : str
            Auction ID.

        Returns
        -------
        InfoSelling
            selling information.

        """
        
        info: InfoSelling = InfoSelling(aID)
        await info.update(self._cookies)    
        return info


    async def get_aIDs_closed_with_winner(self) -> list[str]:
        """ Get aIDs closed with winner on Yahoo Auction page. 
        
        Returns
        -------
        list[str]
            List of aIDs.
        """
        urls: list[str] = await self.get_urls_closed_with_winner()
        aIDs: list[str] = []
        for url in urls:
            match = re.search(r'(?<=/)\w+$', url)
            if match:
                aIDs.append(url[match.start():match.end()])
        return aIDs


    async def get_urls_closed_with_winner(self) -> list[str]:
        """ Get URLs closed with winner on Yahoo Auction page. 
        
        Returns
        -------
        list[str]
            List of URLs.
        """
        pattern: Pattern[str] = re.compile(r'^rsec:itm;slk:ttlc;')
        return await _get_urls(self._cookies, YahooAuctionURL.CLOSED_WITH_WINNER, pattern)


    async def get_info_closed_with_winner(self) -> InfoClosedWithWinner:
        raise NotImplementedError()


    async def get_aIDs_closed_without_winner(self) -> list[str]:
        """ Get aIDs closed with no winner on Yahoo Auction page. 
        
        Returns
        -------
        list[str]
            List of aIDs.
        """
        urls: list[str] = await self.get_urls_closed_without_winner()
        aIDs: list[str] = []
        for url in urls:
            match = re.search(r'(?<=/)\w+$', url)
            if match:
                aIDs.append(url[match.start():match.end()])
        return aIDs


    async def get_urls_closed_without_winner(self) -> list[str]:
        """ Get URLs closed with no winner on Yahoo Auction page. 
        
        Returns
        -------
        list[str]
            List of URLs.
        """
        pattern: Pattern[str] = re.compile(r'^rsec:itm;slk:ttlc;')
        return await _get_urls(self._cookies, YahooAuctionURL.CLOSED_WITHOUT_WINNER, pattern)


    async def get_info_closed_without_winner(self) -> InfoClosedWithoutWinner:
        raise NotImplementedError()



    def reflesh_cookies(self) -> None:
        """ Reflesh cookies. 
        
        Not Impremented yet.
        """
        raise NotImplementedError()





async def _get_urls(cookies: dict[str, str], src_url: str, pattern: Pattern[str]) ->list[str]:
    """ Get product urls from `src_url`. 
    
    Recursive.
    """    
    response: requests.Response = await requests.get(src_url, cookies=cookies)
    response.raise_for_status()

    soup = bs4.BeautifulSoup(response.content, 'lxml')
    urls: list[str] = []
    url_tags: list[bs4.element.Tag] = [tag for tag in soup.find_all('a', attrs={'data-ylk': pattern})]
    for tag in url_tags:
        try:
            urls.append(tag.get('href'))
        except Exception as e:
            pass
    next_page: Optional[str] = _get_next_page(soup)

    
    if next_page:
        urls.extend(await _get_urls(cookies, next_page, pattern))

    return urls



def _get_next_page(soup: bs4.BeautifulSoup) -> Optional[str]:
    """ Return next page url from `soup`. 
    
    Parameters
    ----------
    soup : bs4.BeautifulSoup
        Soup of a Yahoo Auction page.

    Returns
    -------
    str | None
        URL of next page if exists, else None.

    """
    pattern: Pattern[str] = re.compile(r'^rsec:pagination;slk:next;')
    next_page_tags: list[bs4.element.Tag] = [tag for tag in soup.find_all('a', attrs={'data-ylk': pattern})]
    if len(next_page_tags) > 0:
        try:
            return str(next_page_tags[0].get('href'))
        except:
            return None
    else:
        return None

