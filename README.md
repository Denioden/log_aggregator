# Django Aggregator Apache Access Logs

## Задание

    Используя django/flask(на выбор), реализовать приложение, которое является агрегатором данных из access логов apache с сохранением в БД.
    Разбор файлов должен выполняться по cron'у.

    В приложении реализовать такие функции:
    - авторизация (пользователи в БД)
    - просмотр данных сохраненных в БД (группировка по IP, по дате, выборка по промежутку дат)
    - API для получения данных в виде JSON (смысл тот же: получение данных по временному промежутку, возможность группировать/фильтровать по IP)
    - конфигурация через файл настроек (где лежат логи, маска файлов, и все, что Вам потребуется для настройки приложения)

    СУБД: postgresql

## Установка

Клонировать репозиторий и перейти в него в командной строке:

```
$ git clone https://github.com/Denioden/log_aggregator.git
```

Создать и активировать виртуальное окружение:

```
$ python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    $ source env/bin/activate
    ```

* Если у вас windows

    ```
    $ venv\Scripts\activate.bat
    ```

```
(venv) $ python3 -m pip install --upgrade pip
```

Перейти в директорию log_agregator

```
(venv) $ cd  log_aggregator/
```
Установить зависимости из файла requirements.txt:

```
(venv) $ pip install -r requirements.txt
```
Настроить базу данных postgresql. Описано ниже. 

Выполнить миграции:
```
(venv) $ python3 manage.py makemigarations
(venv) $ python3 manage.py migration
```

### Создаём базу данных:

- Вызовите утилиту psql.
```
(venv) $ sudo -u postgres psql
```
- Теперь через psql создайте базу данных, например log_list
```
postgres=# CREATE DATABASE log_list;
```
- Создайте пользователя например log_user и придумайте пароль.
```
postgres=#CREATE USER log_user WITH ENCRYPTED PASSWORD 'log_password';
``` 
- Дайте пользователю log_user все права при работе с базой log_list. 
```
- postgres=#GRANT ALL PRIVILEGES ON DATABASE log_list TO log_user;
```
- Выйдите из psql.
``` 
postgres=#\q
```
     
Создайте .env файл. Директория_проекта/log_agregator/log_agregator/.env
Добавьте в файл настройки подключения к базе данных:

- Укажите, что используете postgresql.
    DB_ENGINE=django.db.backends.postgresql

- Укажите имя созданной базы данных.
    DB_NAME=log_list

- Укажите имя пользователя.
    POSTGRES_USER=log_user

- Укажите пароль для пользователя.
    POSTGRES_PASSWORD=log_password

- Укажите localhost.
    DB_HOST=127.0.0.1

- Укажите порт, для подключения к базе.
    DB_PORT=5432 


## Внимание:

    Если у файла новое имя, сиcтема распознаёт его как новый файл, запишет данные 
    и сообщит "Данные файла {file_name} записываются".

    Если у файла имя которое уже записано в базу, но новые данные (новая первая строка), система 
    обновит данные о файле, запишет новые данные и сообщит - "Запись файла {file_name} обновлена"

    Если в ранее записанный файл добавить новые строки система распознает это, обновит данные о файле, 
    запишет новые данные и сообщит - "Запись файла {file_name} обновлена"

    Если начать записывать файл, который был записан ранее, без изменения данных,
    система сообщит - "Данные файла {file_name} уже были записаны" 


## Настройка setting.py
 __PARSER_LOG_PATH__ - укажите путь и маску ваших логов например: "home/user/logs/*".
  - __По умолчанию:__ указывает на "log_aggregator/test_logs/*".

__CRONJOBS__ - настройки параметров планового запуска скрипта, по умолчанию запуск скрипта раз в 5 минут.


## Запуск проекта

- Проверить что виртуальное окружение активировано.
- Переходим в директорию, где находится файл manage.py
- Запускаем парсер логов:

    ```
    (venv) $ python manage.py shell
        >>> from log_access_apache.utils import parser
        >>> parser_log()
        >>> exit()
    ```
     
- Создаём суперпользователя:
    ```
    (venv) $ python manage.py createsuperuser

    ```
- вводим имя, пароль, повтор пароля:
    ```
    (venv) $ Username: admin
    (venv) $ Email addres: ivanov@yandex.ru
    (venv) $ Password: admin
    (venv) $ Password (again): admin
    ```

- Активируем локальный сервер.
    ```
    python3 manage.py runserver
    ```

## Команды для работы с cron
- Активируем cron.
   ```
   python manage.py crontab add
   ```

- Показать текущие активные задания.
   ```
   python manage.py crontab show
   ```

- Удаление всех заданий.
   ```
   python manage.py crontab remove
   ```

# Тестирование API
## Авторизация, просмотр данных и фильтрация (Django REST Api)
## Переходим в приложение для тестирования, при разработке, тестирование проводилось в приложение Potsman
## Документация API находится по ссылке: http://127.0.0.1:8000/api/docs/

### Получить токен
Отправляем POST-запрос на адрес ```/api/api-token-auth/``` и передаем 2 поля в `data`.

#### Request
    http http://127.0.0.1:8000/api/api-token-auth/ 

#### Response
    "token": "6b4bee3aad939a0957651a015116a18db60947d4"
  
Вводим данный суперпользователя.
1. `username` - указываем имя пользователя.
2. `password` - указываем пароль пользователя.

## Посмотреть все логи

Отправляем GET-запрос на адрес ```/api/logs/```, указывая полученный токен.

#### Request
    http http://127.0.0.1:8000/api/logs/  
    Authorization: Token 6b4bee3aad939a0957651a015116a18db60947d4
#### Response
    Выдаст все записанные логи в базе

Можно вывести определённое количество записей указав limit
#### Request
    http://127.0.0.1:8000/api/logs/?limit=1
    Authorization: Token 6b4bee3aad939a0957651a015116a18db60947d4
#### Response
    {
        "count": 10000,
        "next": "http://127.0.0.1:8000/api/logs/?limit=1&offset=1",
        "previous": null,
        "results": [
            {
                "id": 48,
                "remote_host": "66.249.73.185",
                "remote_logname": null,
                "remote_user": null,
                "request_time": "2015-05-17T10:05:00",
                "request_line": "GET /reset.css HTTP/1.1",
                "final_status": 200,
                "bytes_sent": 1015,
                "referer": null,
                "user_agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
            }
        ]
    }


### Фильтрация логов 

- Доступные фильтры (С примерами):
  - Host (IP)
    - remote_host=68.180.224.225
  - Диапазон времени:
    - request_time_after=2015-05-18 07:00:00
    - request_time_before=2015-05-19 07:05:40
 

    #### Request

        http://127.0.0.1:8000/api/logs/?remote_host=68.180.224.225&request_time_after=2015-05-18 07:00:00&request_time_before=2015-05-18 07:05:40
        Authorization: Token 6b4bee3aad939a0957651a015116a18db60947d4

    #### Response

        {
            "id": 2474,
            "remote_host": "68.180.224.225",
            "remote_logname": null,
            "remote_user": null,
            "request_time": "2015-05-18T07:05:00Z",
            "request_line": "GET /blog/geekery/187.html HTTP/1.1",
            "final_status": 200,
            "bytes_sent": 9201,
            "referer": null,
            "user_agent": "Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)"
        },
        {
            "id": 2580,
            "remote_host": "68.180.224.225",
            "remote_logname": null,
            "remote_user": null,
            "request_time": "2015-05-18T07:05:35Z",
            "request_line": "GET /blog/productivity/181.html HTTP/1.1",
            "final_status": 200,
            "bytes_sent": 9817,
            "referer": null,
            "user_agent": "Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)"
        }