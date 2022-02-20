# Кинопоиск ТОП-250 сериалов гистограмма

Необходимый  предоставить программу на python которая будет парсить список
сериалов https://www.kinopoisk.ru/lists/series-top250/ и выдавать необходимый анализ.
Перед 


## Загрузка

- **clone repository**

    ```shell
    git clone https://github.com/vavasya/Pet_projects.git
    cd Pet_projects
    ```
- **prepare config file**

  copy template config:

    ```shell
    cp ./config_template.ini ./config.ini
    ```

  fill template config:

    ```shell
    vim ./configs/config.ini
    ```

- **build & run**

    ```shell
    docker build -t top_250 .
    docker run -d -p 8050:8050 --rm -v "$PWD/config.ini:/usr/project/config.ini" -v "$PWD/data/:/usr/project/data/" --name top_250_run top_250
    ```

  ##  Парсинг Кинопоиска (ТОП-250 сериалов)
  В репозитории уже лежат дампы с собраными данными. Для успешного парсинга необходим API  ключ от прокси zyte. Так же можно легко адапатировать код под другой прокси.

    ```shell
    rm -r data/*
    docker exec -it top_250_run bash
    cd /usr/project/  
    python main.py
    ```

    reading logs:
    ```shell
    docker logs -f top_250_run
    ```

    stopping:
    ```shell
    docker stop top_250_run
    ```