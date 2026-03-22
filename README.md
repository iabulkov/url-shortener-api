Сервис для сокращения ссылок с аналитикой и управлением.

API позволяет создавать короткие ссылки, управлять ими и получать статистику переходов.

Основные функции:

Публичные
- `GET /` - информация об API
- `GET /docs` - документация Swagger
- `GET /redoc` - документация ReDoc

Аутентификация
- `POST /auth/register` - регистрация пользователя
- `POST /auth/token` - получение токена
- `GET /auth/me` - информация о текущем пользователе

Работа со ссылками
- `POST /links/shorten` - создание короткой ссылки
- `GET /links/test` - тестовый эндпоинт (проверка БД)
- `GET /{short_code}` - редирект на оригинальный URL
- `DELETE /links/{short_code}` - удаление ссылки
- `PUT /links/{short_code}` - обновление ссылки
- `GET /links/{short_code}/stats` - статистика по ссылке
- `GET /links/search?original_url={url}` - поиск по оригинальному URL


Установка

Клонируйте репозиторий:
```bash
git clone https://github.com/iluan/url-shortener-api.git
cd url-shortener-api

### Запуск тестов

```bash
# Установите зависимости
pip install -r requirements.txt
pip install pytest pytest-cov

# Запустите тесты
PYTHONPATH=$(pwd) pytest tests/test_final_coverage.py tests/test_auth_mock.py -v

# Запустите с отчётом о покрытии
PYTHONPATH=$(pwd) pytest tests/test_final_coverage.py tests/test_auth_mock.py -v --cov=app --cov-report=term --cov-report=html
