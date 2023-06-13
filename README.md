# Продуктовый помощник FoodGram

### Описание проекта

На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, 
добавлять понравившиеся рецепты в список «Избранное», а также в корзину покупок, чтобы перед походом в 
магазин скачивать список продуктов для покупки, необходимых для приготовления всех выбранных блюд.

Сайт разработан в процессе обучения в Яндекс Практикум на курсе Python разрабочик.

Работу сайта можно оценить по адресу: https://foodgram.ermstudio.ru/


### Первый запуск сайта на сервере
Установить на сервере  docker compose:

```
    sudo apt update
    sudo apt install curl
    curl -fSL https://get.docker.com -o get-docker.sh
    sudo sh ./get-docker.sh
    sudo apt-get install docker-compose-plugin 
```

В корне создать директорию kittygram с файлом .env, в котором содержатся переменные:

```
    POSTGRES_USER=...
    POSTGRES_PASSWORD=...
    POSTGRES_DB=... 
    DB_HOST=...
    DB_PORT=...
    SECRET_KEY='...'
```

В директорию kittygram скопировать файл docker-compose.production.yml из этого репозитория.

Далеее выполнить команды:

```
    cd kittygram
    sudo docker compose -f docker-compose.production.yml pull
    sudo docker compose -f docker-compose.production.yml down
    sudo docker compose -f docker-compose.production.yml up -d
    sudo docker compose -f docker-compose.production.yml exec kittygram_backend python manage.py migrate
    sudo docker compose -f docker-compose.production.yml exec kittygram_backend python manage.py collectstatic
    sudo docker compose -f docker-compose.production.yml exec kittygram_backend cp -r /app/collected_static/. /backend_static/static/
```

Проверить работу четырех контейнеров можно командой:

```
    sudo docker container ls -a
```

### CI/CD GitHub Actions
Workflow файл: .github/workflows/main.yml.

Используемые Repository secrets переменные: DOCKER_PASSWORD, DOCKER_USERNAME, SSH_KEY, SSH_PASSPHRASE, HOST, USER, 
POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER, TELEGRAM_TO, TELEGRAM_TOKEN

Описание: 
- При обновлении ветки main срабатывает триггер.
- Запускаются тесты
- Собираются и оправляются новые образы на dockerhub
- На сервере запускается docker-compose.production.yml, обновляются образы Docker, удаляются текущие контейнеры и создаются новые.
- Выполняются операции миграции и статики
- в Телеграмм отправляется уведомление "Деплой успешно выполнен!"


## Author

- [@EugeneErmakov](https://github.com/EugeneErmakov)
