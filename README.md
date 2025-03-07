## Изменения по урокам

**Урок 1**. Реализовали ручки приложения с фейковой базой и сериализаторами.

**Урок 2**. Провели рефакторинг. Разложили сериализаторы и ручки по отдельным пакетам.
Подключили настоящую БД в Докере и создали модели.

**Урок 3**. Провели рефакторинг.

Поместили питонячий код в папку src (чтобы тесты запускались корректно и код был отделен от окружения).

Написали по одному тесту к ручкам.

Настроили pytest и фикстуры. Пример почти идеальной настройки фикстур для работы с БД.

Добавили .env файл и модуль settings для хранения переменных окружения и их легкого использования.

## Структура проекта

Для удобства и соблюдения принципов чистой архитектуры проект разделен на следующие пакеты:

- `configurations` — слой для хранения конфигураций, констант, параметров и настроек проекта.

- `models` — слой для хранения моделей (ORM или Data Classes).

- `routers` — слой для настроек урлов для различных эндпоинтов.

- `schemas` — слой содержащий схемы pydantic, отвечает за сериализацию и валидацию.

## Полезные ссылки (в основном на английском)

#### По Fastapi:

1. [Официальная документация](https://fastapi.tiangolo.com/)

2. [Лучшие практики](https://github.com/zhanymkanov/fastapi-best-practices)

3. [Собрание полезных библиотек и пакетов](https://github.com/mjhea0/awesome-fastapi)

4. [Полезная статья по структуре проекта](https://camillovisini.com/coding/abstracting-fastapi-services)

#### По принципам REST архитектуры:

5. [Полезные рекомендации по правильному написанию REST API](<https://github.com/stickfigure/blog/wiki/How-to-(and-how-not-to)-design-REST-APIs>)

#### По SQLAlchemy:

6. [Хороший бесплатный видеокурс на YouTube. На русском языке](https://youtube.com/playlist?list=PLeLN0qH0-mCXARD_K-USF2wHctxzEVp40&si=V7rZGqu1KVJvidLz)
