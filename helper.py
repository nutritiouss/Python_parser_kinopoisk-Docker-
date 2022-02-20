import requests
import os
import pandas as pd
import pickle
from glob import glob
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(name)s: %(message)s',
    level=logging.INFO
)


def kinopoisk_request(X_API, page_number):
    """input:Получает на вход ключ от Прокси(zyte-proxy) и номер страницы
       output: html текст страницы"""
    logger.info(f"kinopoisk_request start for page {page_number}")
    url = f"https://www.kinopoisk.ru/lists/movies/series-top250/?page={page_number}"
    response = requests.get(
        url,
        proxies={
            "http": f"http://{X_API}:@proxy.crawlera.com:8011/",
            "https": f"http://{X_API}:@proxy.crawlera.com:8011/",
        },
        verify=f"{os.path.dirname(__file__)}/zyte-proxy-ca.crt"
    )
    logger.info(f"kinopoisk_request finish for page {page_number}")
    return response.text


def parse_films(page_number, soup):
    """input: номер страницы, обьект Beautiful(одна строница в 50 фильмов) soup
       output: Dataframe с фильмами с одной страницы
       Происходит обработка html разметки и создается DF(50 строк)
        со структурой 'link','film_name','genre'
       """
    data_films = []
    list_films = soup.findAll('div', class_='styles_root__3a8vf')
    logger.info(f"parse_films start for page {page_number}")
    for idx, film in enumerate(list_films):
        try:
            url = "https://www.kinopoisk.ru" + film.find('a', class_='base-movie-main-info_link__3BnCh').get('href')
            name_film = film.find('a', class_='base-movie-main-info_link__3BnCh'). \
                find('span', class_='styles_mainTitle__3Bgao styles_activeMovieTittle__1yPIb'). \
                text
            genre = film.find('div', class_='desktop-list-main-info_additionalInfo__3bH2Z'). \
                find('span', class_='desktop-list-main-info_truncatedText__2Q88H'). \
                text.split('•')[1].split('\xa0')[0]
            data_films.append([url, name_film, genre])
        except  Exception as ex:
            print (ex.args)
            data_films.append(['null'] * 3)
            print(f'Ошибка парсинга в фильме c номером {(page_number - 1) * 50 + idx}')
    data_films = pd.DataFrame(data_films)

    # Store data (serialize), check if file exist
    if not os.path.isfile(f'data/{page_number}_page.pickle'):
        with open(f'data/{page_number}_page.pickle', 'wb') as handle:
            pickle.dump(data_films, handle, protocol=pickle.HIGHEST_PROTOCOL)
        logger.info(f"parse_films finish for page {page_number}")
    return data_films


def concat_dataframes():
    """"Соединение всех датафрэймов в один для последующей обработки"""
    list_file = glob('data/*_page.pickle')
    with open(list_file[0], "rb", buffering=30) as file:
        df = pd.read_pickle(file)
    for table in list_file[1:]:
        with open(table, "rb", buffering=30) as file:
            table_df = pd.read_pickle(file)
            file.close()
        df = pd.concat([df, table_df])
    df.columns = ['link', 'film_name', 'genre']
    return df

