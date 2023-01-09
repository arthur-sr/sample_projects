import requests
import time

from .parsers import Zoopage
from .zooshop_handler import ZooshopHandler

HEADERS =  {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1"
}


class PageScraper:
    def __init__(self, zooshop_handler: ZooshopHandler):
        self.zooshop_handler = zooshop_handler
        
    def get_page(self, url):
        response = requests.get(url, headers=HEADERS)
        shops = Zoopage(response.text).get_shops()
        self.zooshop_handler.add_shops(shops, url)

    
    def scrape_pages(self, urls: list[str], results_filepath):
        scraped_urls = urls.copy()

        while scraped_urls:
            url = scraped_urls.pop()
            try:
                print(f'getting {url}')
                self.get_page(url)
                print(f'got {url}')
            except:
                print(f'failed to get {url}')                
            finally:    
                time.sleep(1) # not to ddos their servers; also reason not to parrallel / async

        self.zooshop_handler.load_out_csv(results_filepath)



