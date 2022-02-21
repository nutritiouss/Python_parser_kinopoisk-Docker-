import time
from bs4 import BeautifulSoup
from helper import parse_films,kinopoisk_request
from configparser import ConfigParser
import os
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(name)s: %(message)s',
    level=logging.INFO
)

config = ConfigParser()
config.read(f'{os.path.dirname(__file__)}/config/config.ini')
X_API = config["main_param"]["X_API"]

logger.info(f"loading X-API key")
print(X_API)

if __name__ == '__main__':
    for page_number in range(1,6):
        response = kinopoisk_request(X_API,page_number)
        soup = BeautifulSoup(response,'lxml')
        parse_films(page_number,soup)
        time.sleep(8)
        logger.info('Данные со страницы {0} сохранены'.format(page_number))

