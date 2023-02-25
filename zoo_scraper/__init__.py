import json
from datetime import datetime

from dotenv import load_dotenv

from .scraper import PageScraper
from .zooshop_handler import ZooshopHandler
from .utils import write_log, write_error


if not load_dotenv():
    raise Exception('Failed to load environment')


def read_urls(config_path):
    with open(config_path) as f:
        config = json.load(f)
    
    # checkin for "/" in the base_url
    if config['base_url'][-1] == '/':
        base_url = config['base_url'][:-1]
    else:
        base_url = config['base_url']
    
    # base page/1/ not working for some reason. so if requested - change to url without /1/.
    urls = []
    if config['start_page'] == 1:
        urls.append(f'{base_url}/')
        start_idx = 2
    else:
        start_idx = config['start_page']
    
    for i in range(start_idx, config['end_page'] + 1):
        urls.append(f'{base_url}/{i}/')

    return sorted(urls, reverse=True)


class ZooshopScraper:
    '''Scrapes data from zooshop and stores it into a database'''
    def __init__(self):
        zooshop_handler_ = ZooshopHandler()
        self.page_scraper = PageScraper(zooshop_handler_)

    
    def run(self):
        write_log('start run')
        urls = read_urls('zooshop_scraping_config.json')        


        results_file = f'loadouts/out_{datetime.now().strftime("D%Y_%m_%d_T%H_%M_%S")}.csv'
        self.page_scraper.scrape_pages(urls, results_file)
        print('run done')
        write_log('run done')

        

