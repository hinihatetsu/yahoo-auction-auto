from unittest import TestCase
from datetime import datetime

import bs4

from yahoo_auction_auto.info import selling

class TestInfoSelling(TestCase):

    def setUp(self) -> None:
        with open('tests/info/test_selling.html', encoding='utf-8') as f:
            self.soup = bs4.BeautifulSoup(f.read(), 'lxml')
    

    def test_get_title(self) -> None:
        title = selling._get_title(self.soup)
        self.assertEqual(title, 'title')

    
    def test_get_sellername(self) -> None:
        sellername = selling._get_seller_name(self.soup)
        self.assertEqual(sellername, 'seller_name')


    def test_get_detail_stack(self) -> None:
        stack: int = selling._get_stack(self.soup)
        self.assertEqual(stack, 1)


    def test_get_detail_start_datetime(self) -> None:
        dt: datetime = selling._get_start_datetime(self.soup)
        self.assertEqual(dt, datetime(2021, 10, 12, 19, 54))


    def test_get_detail_end_datetime(self) -> None:
        dt: datetime = selling._get_end_datetime(self.soup)
        self.assertEqual(dt, datetime(2021, 10, 15, 19, 54))


    def test_get_detail_refundable(self) -> None:
        self.assertFalse(selling._get_refundable(self.soup))


    def test_get_detail_startprice(self) -> None:
        startprice: str = selling._get_startprice(self.soup)
        self.assertEqual(startprice, '10,000 円（税 0 円）')


    def test_get_count_bid(self) -> None:
        count_bid: int = selling._get_count_bid(self.soup)
        self.assertEqual(count_bid, 0)

    
    def test_get_count_timeleft(self) -> None:
        timeleft: str = selling._get_timeleft(self.soup)
        self.assertEqual(timeleft, '19時間')


    def test_get_count_access(self) -> None:
        count_access: int = selling._get_count_access(self.soup)
        self.assertEqual(count_access, 0)

    
    def test_get_count_watch(self) -> None:
        count_watch: int = selling._get_count_watch(self.soup)
        self.assertEqual(count_watch, 0)