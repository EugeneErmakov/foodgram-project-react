# Продуктовый помощник FoodGram

### Описание проекта

На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, 
добавлять понравившиеся рецепты в список «Избранное», а также в корзину покупок, чтобы перед походом в 
магазин скачивать список продуктов для покупки, необходимых для приготовления всех выбранных блюд.

Сайт разработан в процессе обучения в Яндекс Практикум на курсе Python разрабочик.

Работу сайта можно оценить по адресу: https://foodgram.ermstudio.ru/

Доступ к админке: adm admadmadm

## Технологии
[![Python](https://img.shields.io/badge/-Python-464646?style=plastic&logo=Python&logoColor=56C0C0&color=508050)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=plastic&logo=Django&logoColor=56C0C0&color=508050)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=plastic&logo=Django%20REST%20Framework&logoColor=16C0C0&color=508050)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=plastic&logo=PostgreSQL&logoColor=56C0C0&color=508050)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=plastic&logo=NGINX&logoColor=56C0C0&color=508050)](https://nginx.org/ru/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=plastic&logo=Docker&logoColor=56C0C0&color=508050)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=plastic&logo=GitHub%20actions&logoColor=56C0C0&color=508050)](https://github.com/features/actions)


### Первый запуск сайта на сервере
Установить на сервере  docker compose:

```
    sudo apt update
    sudo apt install curl
    curl -fSL https://get.docker.com -o get-docker.sh
    sudo sh ./get-docker.sh
    sudo apt-get install docker-compose-plugin 
```

В корне создать директорию foodgram с файлом .env, в котором содержатся переменные:

```
    POSTGRES_USER=...
    POSTGRES_PASSWORD=...
    POSTGRES_DB=... 
    DB_HOST=...
    DB_PORT=...
    SECRET_KEY='...'
```

В директорию foodgram скопировать файл docker-compose.production.yml из этого репозитория.

Далеее выполнить команды:

```
    cd foodgram
    sudo docker compose -f docker-compose.production.yml pull
    sudo docker compose -f docker-compose.production.yml down
    sudo docker compose -f docker-compose.production.yml up -d
    sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
    sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
    sudo docker compose -f docker-compose.production.yml exec backend python manage.py importcsv
```

Проверить работу четырех контейнеров можно командой:

```
    sudo docker container ls -a
```

### CI/CD GitHub Actions
Workflow файл: .github/workflows/main.yml.

Используемые Repository secrets переменные: DOCKER_PASSWORD, DOCKER_USERNAME, SSH_KEY, SSH_PASSPHRASE, HOST, USER, TELEGRAM_TO, TELEGRAM_TOKEN

Описание: 
- При обновлении ветки master срабатывает триггер.
- Запускаются тесты
- Собираются и оправляются новые образы на dockerhub
- На сервере запускается docker-compose.production.yml, обновляются образы Docker, удаляются текущие контейнеры и создаются новые.
- Выполняются операции миграции и статики
- в Телеграмм отправляется уведомление "Деплой успешно выполнен!"


## Author

- [@EugeneErmakov](https://github.com/EugeneErmakov)
