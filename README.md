# **Habit Tracker API**

## **Возможности**:

- Регистрация и аутентификация пользователей (JWT)
- CRUD для привычек
- Поддержка публичных и приватных привычек
- Напоминания о привычках через Telegram
- Асинхронные задачи через Celery + Redis + Django Celery Beat
- Документация Swagger (`drf-yasg`)
- Поддержка CORS для фронтенда

---

## **Демо**
Проект доступен по адресу: http://51.250.32.142/
(актуально после деплоя через GitHub Actions)**

---

## **Быстрый старт одной командой**:

Рекомендуемый способ запуска локально:

```docker compose up -d --build```

После выполнения:

API — http://localhost

Swagger — http://localhost/swagger/

ReDoc — http://localhost/redoc/

Админка — http://localhost/admin/

---

## **Альтернативный запуск без Docker**:

1. Клонируйте репозиторий:

```git clone git@github.com:Alexandra-Chigrina/habit-tracker.git```
```cd habit-tracker```

2. Создайте виртуальное окружение (через Poetry или venv):

Через Poetry:
```poetry install```
```poetry shell```

Через venv:
```python -m venv .venv```
```source .venv/bin/activate```   # Windows: .venv\Scripts\activate
```pip install -r requirements.txt```

3. Создайте .env:

```cp .env.sample .env```

Заполните значения в файле .env (SECRET_KEY, DB-настройки и др.).

4. Выполните миграции:

```python manage.py migrate```

5. Создайте суперпользователя:

```python manage.py createsuperuser```

6. Запустите сервер разработки:

```python manage.py runserver```

7. Запустите Celery:

```celery -A config worker -l INFO```

Windows:

```celery -A config worker -l INFO -P eventlet```

8. Запустите Celery Beat:

```celery -A config beat -l INFO```

Windows:

```celery -A config beat -l INFO -S django```

После запуска:

API — http://127.0.0.1:8000

Swagger — http://127.0.0.1:8000/swagger/

ReDoc — http://127.0.0.1:8000/redoc/

Админка — http://127.0.0.1:8000/admin/

---

## **Развёртывание на удалённом сервере**:

1. Подготовка сервера:

- Установите Docker и Docker Compose
- Настройте SSH-доступ по ключу
- Разрешите порты 80, 443, 22

2. Клонируйте репозиторий:

```git clone git@github.com:Alexandra-Chigrina/habit-tracker.git```
```cd habit-tracker```

3. Создайте файл .env на сервере на основе .env.sample:

`cp .env.sample .env`

4. Соберите и запустите проект:

```docker-compose up -d --build```

---

## **CI/CD через GitHub Actions**:

Файл workflow находится в `.github/workflows/ci.yml`

### Что делает workflow:

1. Запускается на каждый push в репозиторий и на каждый pull request.

2. Выполняет:

- Установка зависимостей

- Линтинг кода (flake8)

- Запуск тестов через manage.py test

- Сборка и отправка Docker-образа на Docker Hub

- Автодеплой на сервер через SSH и Docker

### Secrets в GitHub:

- SSH_KEY — приватный SSH-ключ

- SSH_USER — пользователь на сервере

- SERVER_IP — IP-адрес сервера

- DOCKER_HUB_USERNAME — логин Docker Hub

- DOCKER_HUB_ACCESS_TOKEN — токен доступа к Docker Hub

- (опционально) SECRET_KEY

---

## **Проверка работоспособности сервисов**:

1. Django (web)

Проверить административную панель:
```http://localhost/admin/```
Если работает — веб-сервер запущен.

2. PostgreSQL (db)

Можно подключиться через PgAdmin или выполнить команду:
```docker exec -it habit_tracker-db-1 psql -U postgres -d habits -c "SELECT 1;"```
Если видите (1 row) — всё в порядке.

3. Celery

Посмотреть логи воркера:
```docker-compose logs -f celery```

4. Celery Beat

Планировщик автоматически запускает задачи по расписанию.

Проверка:
```docker-compose logs -f celery-beat```
Если вы видите Scheduler: Sending due task end_habit_reminders — работает.

---

## Тестирование

Запуск тестов внутри контейнера:

```docker-compose exec web python manage.py test```

---

## Документация API:

После запуска проекта открой:
```
http://127.0.0.1/swagger/
http://127.0.0.1/redoc/
```

--- 

## Используемые технологии:

- Django & Django REST Framework (DRF) — backend-фреймворк и API
- PostgreSQL — основная база данных
- Celery & Redis — асинхронные задачи и брокер сообщений
- Django Celery Beat — планировщик периодических задач
- Telegram Bot API — интеграция с Telegram для отправки уведомлений
- drf-yasg — автогенерация документации API (Swagger/ReDoc)
- Docker & Docker Compose — контейнеризация и запуск всех сервисов одной командой
- Nginx — обратный прокси и раздача статики
- Poetry — управление зависимостями Python
- GitHub Actions — CI/CD, автоматическое тестирование и деплой
- CORS — поддержка взаимодействия с фронтендом

---

## **Структура проекта**

habit_tracker/
├── config/                         # Конфигурация проекта Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py                   # Настройки Celery
│   ├── settings.py                 # Основные настройки проекта
│   ├── urls.py                     # Главные маршруты проекта
│   └── wsgi.py
│
├── habits/                         # Приложение управления привычками
│   ├── migrations/
│   │   └── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                   # Модель Habit
│   ├── paginators.py               # Кастомная пагинация
│   ├── serializers.py              # Сериализаторы привычек
│   ├── services.py                 # Вспомогательные сервисы (Telegram)
│   ├── tasks.py                    # Задачи Celery для напоминаний
│   ├── tests.py                    # Тесты для приложения
│   ├── urls.py                     # Маршруты для habits
│   ├── validators.py               # Кастомные валидаторы
│   └── views.py                    # Представления (ViewSets)
│
├── users/                          # Приложение управления пользователями
│   ├── management/                 # Команды 
│   ├── migrations/
│   │   └── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                   # Кастомная модель User
│   ├── serializers.py              # Сериализаторы пользователя
│   ├── tests.py                    # Тесты
│   ├── urls.py                     # Маршруты users
│   └── views.py                    # View-контроллеры (регистрация, профиль)
│
├── .github/workflows/ci.yml        # Конфигурация GitHub Actions для CI/CD: линтинг, тесты, сборка и деплой на сервер
│
├── nginx                           # Конфигурация nginx для проксирования запросов к Django-приложению
│   ├── Dockerfile                  # Docker-образ для nginx с копированием nginx.conf
│   ├── nginx.conf                  # Основной конфиг nginx: проксирование к Gunicorn, статика, админка
│
├── media/                          # Загружаемые медиафайлы
├── static/                         #  Директория для хранения cтатических файлов
│
├── .coverage                       # Файл покрытия тестами
├── htmlcov/                        # Отчёты покрытия тестов
├── manage.py                       # Управляющий файл Django
├── .venv                           # Виртуальное окружение
├── .env                            # Файл с переменными окружения
├── .env.sample                     # Пример .env файла
├── .gitignore                      # Исключения Git
├── .dockerignore                   # Исключения Docker
├── Dockerfile                      # Сборка образа Django-приложения
├── docker-compose.yml              # Docker-оркестрация всех сервисов
├── .flake8                         # Настройки линтера flake8
├── poetry.lock                     # Фиксация зависимостей Poetry
├── pyproject.toml                  # Основной конфиг проекта
├── README.md                       # Документация проекта
