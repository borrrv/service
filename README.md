![main](https://github.com/borrrv/foodgram-project-react/actions/workflows/main.yml/badge.svg)
# Foodgram «Продуктовый помощник»
Foodgram - это онлайн-сервис, на котором пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
## Инструкция для деплой на сервер
#### Для деплоя на сервер вам нужно предварительно установить на сервере ```docker``` и ```docker-compose```
#### Для успешного автодеплоя вам нужно добавить следующие переменные в ```Actions```
```
- ALLOWED_HOSTS (IP-адрес вашего сервера)
- AUTHORIZED_KEYS (Публичный ssh-ключ)
- DB_ENGINE (Укажите, что используете postgresql)
- DB_HOST (Укажите хост)
- DB_NAME (Укажите имя созданной базы данных)
- DB_PORT (Укажите порт для подключения к базе)
- DEBUG (Опционально)
- DOCKER_PASSWORD (Пароль на DockerHub)
- DOCKER_USERNAME (Логин на DockerHub)
- PASSPHRASE (Если ssh-ключ защищен фразой-паролем)
- POSTGRES_PASSWORD (Укажите пароль для пользователя)
- POSTGRES_USER (Укажите имя пользователя)
- SECRET_KEY 
- SSH_KEY (Приватный ssh-ключ)
- USER (Пользователь сервера)
```
После успешного коммита и прохождения тестов ваш проект автоматически будет настроен на сервере. 
### При первом деплое
Запустите миграции на сервере и соберите статику
```
- sudo docker-compose exec backend python manage.py makemigrations 
- sudo docker-compose exec backend python manage.py migrate
- sudo docker-compose exec backend python manage.py collectstatic --no-input
```
(Опционально) Заполнение базы данных
- Зайдите на сервер
```sudo docker-compose exec backend bash```
Выполните следующие команды
```
- python manage.py shell
- from django.conrtib.contenttypes.models import ContentType
- ContentType.objects.all().delete()
- quit()
- python manage.py loaddata dump.json
```
#### Технологии
- Python 3.8
- Django 2.2.16
- DRF 3.2.14
- Djoser
- Postgresql
- Docker
- Docker-compose
- nginx
- gunicorn
