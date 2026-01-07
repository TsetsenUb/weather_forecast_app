# Weather Forecast App
Приложение для получения прогноза погоды для конкретного населённого пункта.


## Архитектура
- **Backend**: FastAPI
- **База данных**: SQLAlchemy + Postgres
- **Кэш**: Redis
- **Валидация данных**: Pydantic
- **Аутентификация**: pwdlib
- **Фронтенд**: SPA в каталоге `frontend`
- **Контейнеризация**: Docker + docker-compose
- **Прокси**: Nginx


## Особенности
- Быстрый REST API на FastAPI
- ORM: SQLAlchemy
- Валидация и схемы: Pydantic
- Redis: хранение прогнозов погоды в кеше (с временем истечения)
- Хранение паролей: pwdlib
- Возможность запуска через Docker / docker-compose
- Nginx в качестве обратного прокси (в docker-compose)
- Client: SPA (frontend) в папке frontend


## Документация OpenAPI
- http://localhost/api/docs
- http://localhost/api/redoc
- http://localhost/api/openapi.json


## Запуск через Docker
- Собрать контейнеры и запустить:
    docker compose up --build
- Остановить и удалить контейнеры:
    docker compose down

## Файлы конфигурации
- .env.example — шаблон переменных окружения
- Dockerfile — сборка образа backend
- docker-compose.yml — конфигурация сервисов (backend, postgres_db, frontend, nginx)
- nginx.conf — настройка обратного прокси (для Docker)
- redis.conf — конфигурация Redis

## Переменные окружения (важные)
- SECRET_KEY — секрет для генерации токенов / сессий
- OWM_APPID — ключ внешнего API погоды (Open weather map)
- ACCESS_TOKEN_EXPIRE_MINUTES — время жизни токена (JWT)
- DB_USER — имя пользователя базы данных
- DB_PASSWORD — пароль базы данных
- DB_NAME — имя базы данных
- REDIS_FORECAST_EXPIRE_SEC — время хранения кэша в Redis (в секундах)

## Структура проекта (важные каталоги и файлы)
- app/ — backend код (FastAPI)main.py — точка входа приложения
- api/ — роутеры и зависимости
- clients/ — клиенты для работы с внешними API погоды
- core/ — конфигурация, аутентификация, настройки
- crud/ — классы crud операций с базой данных
- database/ — фабрика асинхронных сессий к базе данных
- middleware/ — middleware логирования
- models/ — SQLAlchemy модели
- schemas/ — Pydantic схемы
- services/ — логика работы с внешними API (погода) и базой данных
- utils/ - исключения и конвертеры
- frontend/ — SPA frontend (html, css, javascript)
- requirements.txt — зависимости Python
- Dockerfile, docker-compose.yml, nginx.conf — контейнеризация

## Аутентификация и безопасность
- Пароли хранятся в захешированном виде с использованием pwdlib.
- JWT аутентификация
