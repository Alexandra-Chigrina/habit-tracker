# **Habit Tracker API**

## **Возможности**:

- Регистрация и аутентификация пользователей (JWT)
- CRUD для привычек
- Поддержка публичных и приватных привычек
- Напоминания о привычках через Telegram
- Асинхронные задачи через Celery + Redis + Django Celery Beat
- Документация Swagger (`drf-yasg`)
- Поддержка CORS для фронтенда

## **Установка**:

1. Клонируйте репозиторий

```
git@github.com:Alexandra-Chigrina/habit-tracker.git
```

2. В терминале инициализируйте Poetry и активируйте виртуальное окружение

```
poetry init
poetry shell
```

Или, если используете venv:

```commandline
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Создайте .env на основе .env.example

4. Выполните миграции и создайте суперпользователя:

```commandline
python manage.py migrate
python manage.py createsuperuser
```
Панель администратора:
`http://127.0.0.1:8000/admin/`

## **Использование**:

### Запуск проекта:

1. Основной сервер:
```
python manage.py runserver
```

`http://127.0.0.1:8000/`

2. Celery воркер:
```
celery -A config worker -l INFO
```
для Windows:
```
celery -A config worker -l INFO -P eventlet   
```

3. Celery Beat (для периодических задач):
```
celery -A config beat -l info

```
для Windows:
```
celery -A config beat -l info -S django  
```

### Запуск тестов:

```
python manage.py test
```

### Документация API:

После запуска проекта открой:
```
http://127.0.0.1:8000/swagger/
http://127.0.0.1:8000/redoc/
```

### Используемые технологии:

- Django & DRF
- PostgreSQL
- Celery & Redis
- Django Celery Beat
- Telegram Bot API
- drf-yasg 


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
├── media/                          # Загружаемые медиафайлы
├── htmlcov/                        # Отчёты покрытия тестов
├── manage.py                       # Управляющий файл Django
├── .venv                           # Виртуальное окружение
├── .env                            # Файл с переменными окружения
├── .env.sample                     # Пример .env файла
├── .gitignore                      # Исключения Git
├── .flake8                         # Настройки линтера flake8
├── poetry.lock                     # Фиксация зависимостей Poetry
├── pyproject.toml                  # Основной конфиг проекта
├── README.md                       # Документация проекта

