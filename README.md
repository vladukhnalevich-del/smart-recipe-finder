# Smart Recipe Finder



**Система управления рецептами с REST API и веб-интерфейсом**

[![Django](https://img.shields.io/badge/Django-4.0-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

##  Содержание
- Быстрый старт
- Веб-интерфейсы
- API документация
- Структура проекта
- Команды
- Примеры
- Отладка
## Технологии
- **Backend:** Django 6.x, Django REST Framework
- **Frontend:** HTML, CSS, JavaScript (Vanilla)
- **База данных:** SQLite3
- **Язык:** Python 3.13
# Быстрый старт

### Клонирование репозитория
```bash
git clone https://github.com/vladukhnalevich-del/smart-recipe-finder.git
cd smart-recipe-finder
```

### Активируйте виртуальное окружение
```bash
python -m venv venv 
.venv\Scripts\activate
```

# Установите зависимости
```bash
pip install -r requirements.txt
```

### Настройте базу данных
```bash
python manage.py migrate

python manage.py createsuperuser
```

### Запустите сервер
```bash
python manage.py runserver
```

#  Веб-интерфейсы

| Интерфейс | URL | Описание |
|-----------|-----|----------|
|  Главная | http://127.0.0.1:8000/ | Информация о проекте |
|  Клиент | http://127.0.0.1:8000/client/ | Управление рецептами |
|  API | http://127.0.0.1:8000/api/recipes/ | REST API |


#  API документация
### Основные endpoints

GET    /api/recipes/          # Получить все рецепты

POST   /api/recipes/          # Создать новый рецепт

GET    /api/recipes/{id}/     # Получить рецепт по ID

DELETE /api/recipes/{id}/     # Удалить рецепт

#  Структура проекта

```bash
smart-recipe-finder/
├── apps/
│   └── recipes/                          # Приложение рецептов
│       ├── migrations/                    # Миграции базы данных
│       ├── tests/                         # Тесты
│       │   ├── __init__.py
│       │   ├── test_models.py             # Тесты моделей
│       │   ├── test_api.py                 # Тесты API
│       │   ├── test_validation.py          # Тесты валидации
│       │   ├── test_edge_cases.py          # Граничные случаи
│       │   ├── test_performance.py         # Тесты производительности
│       │   ├── test_security.py            # Тесты безопасности
│       │   └── test_integration.py         # Интеграционные тесты
│       ├── __init__.py
│       ├── admin.py                        # Админ-панель
│       ├── apps.py                          # Конфигурация приложения
│       ├── models.py                        # Модели данных
│       ├── urls.py                          # Маршруты приложения
│       └── views.py                         # Представления и логика
├── config/                                 # Настройки проекта
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py                         # Конфигурация Django
│   ├── urls.py                              # Главные маршруты
│   └── wsgi.py
├── static/                                  # Статические файлы
│   ├── css/
│   │   └── client.css                       # Стили для клиента
│   └── js/
│       └── client.js                         # JavaScript для клиента
├── templates/                               # HTML шаблоны
│   └── recipes/
│       ├── base.html                         # Базовый шаблон
│       ├── client.html                        # Клиентский интерфейс
│       └── home.html                          # Главная страница
├── media/                                    # Загружаемые файлы
├── manage.py                                 # Управление Django
├── README.md                                 # Документация
├── requirements.txt                          # Зависимости Python
└── db.sqlite3                                # База данных
```

#  Команды управления

### Проверить проект
```bash
python manage.py check
```
### Создать миграции
```bash
python manage.py makemigrations
```
### Применить миграции
```bash
python manage.py migrate
```
### Создать администратора
```bash
python manage.py createsuperuser
```
### Запустить сервер
```bash
python manage.py runserver
```
### Запустить shell
```bash
python manage.py shell
```
## Тестирование

### Запуск всех тестов
```bash
python manage.py test apps.recipes
```
### Запуск конкретных тестов
```bash
# Тесты моделей
python manage.py test apps.recipes.tests.test_models

# Тесты API
python manage.py test apps.recipes.tests.test_api

# Тесты валидации
python manage.py test apps.recipes.tests.test_validation
```


#  Примеры запросов

### Создание рецепта:
```bash
curl -X POST http://127.0.0.1:8000/api/recipes/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Борщ",
    "ingredients": ["свекла", "капуста", "морковь"],
    "instructions": "1. Сварить бульон\n2. Добавить овощи",
    "cooking_time": 90,
    "cuisine": "russian",
    "difficulty": "medium"
  }'
```
### Ответ 
```bash
{
  "id": 1,
  "name": "Борщ",
  "ingredients": ["свекла", "капуста", "морковь"],
  "instructions": "1. Сварить бульон\n2. Добавить овощи",
  "cooking_time": 90,
  "cuisine": "russian",
  "difficulty": "medium"
}
```
#  Отладка

Если возникают ошибки:

Проверьте миграции: python manage.py showmigrations

Очистите базу: удалите db.sqlite3 и выполните python manage.py migrate

Проверьте импорты: убедитесь, что в views.py есть from .models import Recipe