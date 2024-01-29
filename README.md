# Foodgram - онлайн-сервис для публикации рецептов

### О проекте

На сайте «Фудграм» пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся 
рецепты в «Избранное», а также скачивать список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
* На сайте доступна система регистрации и авторизации пользователей. 
* Неавторизованным пользователям доступен просмотр рецептов на главной странице с фильтрацией по тегам; страниц отдельных рецептов.

### Стек технологий

* Frontend проекта написан на `React` (Javascript), backend - на `Django` (Python).
* Frontend и backend взаимодействуют через API (реализовано через `Django Rest Framework`).
* При развертывании проекта использован веб-сервер `nginx`, WSGI-сервер `Gunicorn` и `Docker`.
* Проект использует базу данных PostgreSQL.
* Настроено `CI/CD`.

### Конфигурация

Контейнеры Docker:
1. foodgram_db
2. foodgram_backend
3. foodgram_frontend
4. foodgram_nginx

Файлы docker-compose:
1. `infra/docker-compose.yml` - для локального запуска.
2. `docker-compose.production.yml` - для запуска на сервере.

### Локальный запуск

Необходимо создать файл `.env`:

```
POSTGRES_DB=
POSTGRES_USER=user
POSTGRES_PASSWORD=password
DB_NAME=
DB_HOST=db
DB_PORT=5432
SECRET_KEY=
ALLOWED_HOSTS=127.0.0.1,localhost
DEBUG=
```

* Собрать образы и запустить контейнеры Docker. Из директории infra/ выполнить:

```
docker compose up --build
```

* Применить миграции:

```
docker compose exec backend python manage.py migrate
```

* Собрать статику:
```
docker compose exec backend python manage.py collectstatic
```
```docker compose exec backend cp -r /app/collected_static/. /backend_static/
```

* Cоздать суперпользователя:

```
docker compose exec backend python manage.py createsuperuser
```

* Документация будет доступна по адресу: http://localhost/api/docs/.

### Информация

* Проект доступен по адресу: https://yandextaski.ddns.net/.

