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
- **Тестирование**: Pytest
- **Зависимости**: UV
- **Линтер и форматер**: ruff

## Демонстрация работы приложения

<div style="display: flex; flex-direction: column; width: 100%; gap: 40px;">
  <div style="width: 100%;">
    <h3 style="text-align: center; margin-bottom: 10px;">Получение прогноза</h3>
    <img src="gif_files/get_forecast.gif" alt="Получение прогноза" style="width: 100%; height: auto; display: block;"/>
  </div>

  <div style="width: 100%;">
    <h3 style="text-align: center; margin-bottom: 10px;">Регистрация</h3>
    <img src="gif_files/registration.gif" alt="Регистрация" style="width: 100%; height: auto; display: block;"/>
  </div>

  <div style="width: 100%;">
    <h3 style="text-align: center; margin-bottom: 10px;">Вход в систему</h3>
    <img src="gif_files/login.gif" alt="Вход в систему" style="width: 100%; height: auto; display: block;"/>
  </div>

  <div style="width: 100%;">
    <h3 style="text-align: center; margin-bottom: 10px;">Выход и окно изменения пользователя</h3>
    <img src="gif_files/quite.gif" alt="Выход" style="width: 100%; height: auto; display: block;"/>
  </div>
</div>

## Как пользоваться
- В файле .env установить свои:
  - OWM_APPID (appid от Open weather map API)
  - SECRET_KEY (сгенерировать можно командой openssl rand -hex 32)
  - параметры для подключения к БД
  - ALLOW_ORIGINS, ALLOW_METHODS, ALLOW_HEADERS
- Собрать образ Docker и запустить командой: docker compose up -d --build
- И пользоваться (по умолчанию по адресу localhost:80)

## Особенности
- Быстрый REST API на FastAPI
- ORM: SQLAlchemy
- Валидация и схемы: Pydantic
- Redis: хранение прогнозов погоды в кеше (с временем истечения)
- Хранение паролей: pwdlib
- Возможность запуска через Docker / docker-compose
- Nginx в качестве обратного прокси (в docker-compose)
- Client: SPA (frontend) в папке frontend
- Тестирование: Pytest

## Аутентификация и безопасность
- Пароли хранятся в захешированном виде с использованием pwdlib.
- JWT аутентификация

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
- pytest.ini - конфигурация pytest

## Переменные окружения (важные)
- SECRET_KEY — секрет для генерации токенов / сессий
- OWM_APPID — ключ внешнего API погоды (Open weather map)
- ACCESS_TOKEN_EXPIRE_MINUTES — время жизни токена (JWT)
- DB_USER — имя пользователя базы данных
- DB_PASSWORD — пароль базы данных
- DB_NAME — имя базы данных
- REDIS_FORECAST_EXPIRE_SEC — время хранения кэша в Redis (в секундах)
- TEST_DATABASE_URL - тестовая база данных

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
- tests/ - тестирование
- frontend/ — SPA frontend (html, css, javascript)
- requirements.txt — зависимости Python
- Dockerfile, docker-compose.yml, nginx.conf — контейнеризация
