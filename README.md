# Веб-приложение на Flask

## Описание
Веб-приложение на основе **Flask** предоставляет REST-API и веб-интерфейс для управления пользователями. Поддерживает авторизацию, регистрацию, просмотр, создание, обновление и удаление пользователей через API. Веб-интерфейс включает страницу для взаимодействия с API, где авторизованные пользователи могут управлять списком пользователей. Приложение использует SQLite для хранения данных, Alembic для миграций, Flask-Login для авторизации, pytest для тестирования и CSS для стилизации интерфейса.

## Функционал
- **Веб-интерфейс**:
  - Регистрация новых пользователей (`/register`).
  - Авторизация и выход из системы (`/login`, `/logout`).
  - Главная страница для авторизованных пользователей (`/`).
  - Страница управления пользователями (`/users`) с возможностью просмотра списка пользователей, создания, обновления и удаления через AJAX-запросы к API.
- **REST-API**:
  - `GET /api/users` — получить список всех пользователей.
  - `POST /api/users` — создать нового пользователя.
  - `GET /api/users/<id>` — получить данные пользователя по ID.
  - `PUT /api/users/<id>` — обновить данные пользователя.
  - `DELETE /api/users/<id>` — удалить пользователя.
- **Безопасность**:
  - Пароли хешируются с использованием `werkzeug.security`.
  - Доступ к защищённым страницам и API ограничен авторизацией через Flask-Login.
- **Тестирование**:
  - Полное покрытие API тестами с использованием pytest.
  - Тест рендеринга страницы управления пользователями.
- **Миграции**:
  - Управление схемой базы данных через Alembic.

## Требования
- Python 3.8+
- Виртуальное окружение (`venv`)
- Установленные зависимости (см. `requirements.txt`)

## Структура проекта
```
flask_app/
│
├── app/
│   ├── init.py       # Инициализация Flask-приложения
│   ├── api.py            # Маршруты REST-API
│   ├── models.py         # Модели базы данных
│   ├── routes.py         # Маршруты веб-интерфейса
│   ├── static/
│   │   └── style.css     # Стили для веб-интерфейса
│   ├── templates/
│   │   ├── base.html     # Базовый шаблон
│   │   ├── index.html    # Главная страница
│   │   ├── login.html    # Страница входа
│   │   ├── register.html # Страница регистрации
│   │   └── users.html    # Страница управления пользователями
│
├── migrations/           # Миграции базы данных (Alembic)
├── tests/
│   └── test_api.py       # Тесты API и веб-интерфейса
├── config.py             # Конфигурация приложения
├── requirements.txt      # Зависимости проекта
└── README.md             # Документация
```


## Установка
1. Клонируйте репозиторий:
   ```bash
   git clone <repository-url>
   cd flask_app
2. Создайте виртуальное окружение:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # На Windows: .venv\Scripts\activate
3. Установите зависимости:
    ```bash
    pip install -r requirements.txt
4. Настройте переменную окружения FLASK_APP:
    ```bash
    export FLASK_APP=app  # На Windows: set FLASK_APP=app
5. Инициализируйте базу данных и примените миграции:
    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade

## Запуск приложения
- Убедитесь, что FLASK_APP установлена:
    ```bash
    export FLASK_APP=app
- Запустите сервер разработки:
    ```bash
    flask run
- Откройте приложение в браузере: http://127.0.0.1:5000/

## Использование
### Веб-интерфейс
- Регистрация: Перейдите на /register, введите имя пользователя и пароль.
- Вход: Используйте /login для авторизации.
- Главная страница: После входа доступна по адресу /.
- Управление пользователями: Страница /users позволяет:
  - Просматривать список пользователей (через GET /api/users).
  - Создавать новых пользователей (POST /api/users).
  - Обновлять данные пользователей (PUT /api/users/<id>).
  - Удалять пользователей (DELETE /api/users/<id>).
- Выход: Используйте /logout для завершения сессии.

## REST-API
#### Примеры запросов с использованием curl:
- Получить список пользователей:
    ```bash
    curl http://127.0.0.1:5000/api/users
- Создать пользователя:
    ```bash
    curl -X POST http://127.0.0.1:5000/api/users -H "Content-Type: application/json" -d '{"username":"newuser","password":"newpass"}'
- Получить пользователя по ID:
    ```bash
    curl http://127.0.0.1:5000/api/users/1
- Обновить пользователя:
    ```bash
    curl -X PUT http://127.0.0.1:5000/api/users/1 -H "Content-Type: application/json" -d '{"username":"updateduser","password":"updatedpass"}'
- Удалить пользователя:
    ```bash
    curl -X DELETE http://127.0.0.1:5000/api/users/1

## Тестирование
- Убедитесь, что зависимости для тестирования установлены:
    ```bash
    pip install pytest
- Запустите тесты:
    ```bash
    pytest tests/ -v
Тесты покрывают:
- Все методы REST-API (GET, POST, PUT, DELETE).
- Рендеринг страницы управления пользователями (/users).

## Продакшен-рекомендации
- **База данных**: Замените SQLite (SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db') на PostgreSQL или MySQL.
- **Секретный ключ**: Используйте безопасный SECRET_KEY в config.py, сгенерированный, например, с помощью:'
    ```python
    import os
    print(os.urandom(24).hex())

- **Сервер**: Используйте WSGI-сервер, например, Gunicorn:
    ```bash
    pip install gunicorn
    gunicorn -w 4 -b 0.0.0.0:8000 app:app

- **HTTPS**: Настройте обратный прокси (например, Nginx) с SSL-сертификатом.
- **Логирование**: Настройте логирование ошибок и запросов.

## Устранение неполадок
- **Ошибка** Could not import 'app': 
Убедитесь, что переменная FLASK_APP установлена:
    ```bash
    export FLASK_APP=app
- **Ошибка** No such command 'db':
Убедитесь, что Flask-Migrate установлен:
    ```bash
    pip install flask-migrate
- **Предупреждения SQLAlchemy** (LegacyAPIWarning):
Все случаи Query.get() заменены на db.session.get() для совместимости с SQLAlchemy 2.0.

- **Тесты не проходят**:
Проверьте наличие всех шаблонов (base.html, users.html, и т.д.) и маршрутов в app/routes.py. Убедитесь, что база данных инициализирована:
    ```bash
    flask db upgrade

## Зависимости
Содержимое requirements.txt:
```bash
Flask==2.3.2
Flask-SQLAlchemy==3.0.3
Flask-Migrate==4.0.4
Flask-Login==0.6.2
Werkzeug==2.3.6
pytest==7.4.0
```

## Лицензия
MIT License.

## Контакты
...

