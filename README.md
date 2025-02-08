# Library API

Library API — это RESTful API для управления библиотекой, включая книги, авторов, читателей и выдачу книг.

## Features

- **Регистрация и аутентификация пользователей** (JWT).
- **CRUD-операции** для книг, авторов и читателей.
- **Выдача и возврат книг**.
- **Пагинация и фильтрация** для списков книг и авторов.
- **Разделение ролей**:
  - Администраторы могут управлять всеми ресурсами.
  - Читатели могут просматривать книги, обновлять свои данные и брать книги.
- **Ограничение прав доступа**:
  - Только администраторы могут создавать, обновлять и удалять книги и авторов.
  - Читатели могут обновлять только свою информацию.

---

## Архитектура проекта

Проект построен на основе архитектуры **Clean Architecture**, что делает его модульным, тестируемым и легко расширяемым. Основные компоненты:

1. **Модели (`models/`)**:

   - Определение таблиц базы данных с использованием SQLAlchemy.
   - Пример: `Book`, `Author`, `Reader`, `Lending`.

2. **Схемы (`schemas/`)**:

   - Pydantic-схемы для валидации входящих и исходящих данных.
   - Пример: `BookCreate`, `BookResponse`, `ReaderLogin`.

3. **Сервисы (`services/`)**:

   - Бизнес-логика приложения.
   - Пример: `BookService`, `AuthorService`, `ReaderService`.

4. **API-эндпоинты (`api/v1/`)**:

   - Маршрутизация и обработка HTTP-запросов.
   - Пример: `/books/`, `/authors/`, `/readers/`.

5. **Безопасность (`core/security.py`)**:

   - Хеширование паролей и работа с JWT-токенами.

6. **Конфигурация (`core/config.py`)**:

   - Настройки приложения, такие как параметры базы данных и секретные ключи.

7. **Тесты (`tests/`)**:
   - Юнит-тесты для проверки функциональности.

---

## Installation

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/MaskedGod/pat_test
cd library-api
```

### 2. Создайте виртуальное окружение

```bash
python -m venv venv
source venv/bin/activate  # Для Linux/MacOS
venv\Scripts\activate     # Для Windows
```

### 3. Установите зависимости

```bash
pip install -r requirements.txt
```

### 4. Настройте переменные окружения

Создайте файл `.env` в корне проекта и добавьте следующие переменные:

```env
# Основная база данных
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=library

# Настройки JWT
JWT_SECRET_KEY=mysecretkey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> **Важно**: Замените `your_db_user`, `your_db_password` и другие значения на реальные данные.

### 5. Примените миграции

```bash
alembic upgrade head
```

### 6. Запустите приложение

```bash
uvicorn app.main:app --reload
```

Приложение будет доступно по адресу: [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## API Documentation

Документация API доступна по следующим ссылкам:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Project Structure

```
library-api/
├── app/
│   ├── __init__.py
│   ├── core/
│   │   ├── config.py          # Настройки приложения
│   │   └── database.py        # Настройка SQLAlchemy
│   │   └── security.py        # Настройка безопасности
│   ├── models/
│   │   ├── base.py            # Базовая модель
│   │   ├── book.py            # Модель книги
│   │   ├── author.py          # Модель автора
│   │   ├── reader.py          # Модель читателя
│   │   └── lending.py         # Модель выдачи книг
│   ├── schemas/
│   │   ├── book.py            # Pydantic-схемы для книг
│   │   ├── author.py          # Pydantic-схемы для авторов
│   │   ├── reader.py          # Pydantic-схемы для читателей
│   │   └── lending.py         # Pydantic-схемы для выдачи книг
│   ├── services/
│   │   ├── book_service.py    # Сервис для работы с книгами
│   │   ├── author_service.py  # Сервис для работы с авторами
│   │   ├── reader_service.py  # Сервис для работы с читателями
│   │   └── lending_service.py # Сервис для работы с выдачей книг
│   ├── api/
│   │   ├── v1/
│   │       ├── books.py       # Эндпоинты для книг
│   │       ├── authors.py     # Эндпоинты для авторов
│   │       ├── readers.py     # Эндпоинты для читателей
│   │       └── lending.py     # Эндпоинты для выдачи книг
│   └── main.py                # Главный файл приложения
├── alembic/                   # Миграции базы данных
├── .env                       # Переменные окружения
├── README.md                  # Документация проекта
└── requirements.txt           # Зависимости
```
