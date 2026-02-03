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
├── apps/                           # Django приложения
│   └── recipes/                    # Приложение рецептов
│       ├── migrations/             # Миграции базы данных
│       ├── __init__.py
│       ├── apps.py                # Конфигурация приложения
│       ├── models.py              # Модели данных
│       ├── urls.py                # Маршруты приложения
│       └── views.py               # Представления и логика
├── config/                         # Настройки проекта
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py                # Конфигурация Django
│   ├── urls.py                    # Главные маршруты
│   └── wsgi.py
├── static/                        # Статические файлы
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   └── images/
├── templates/                     # HTML шаблоны
│   ├── base.html                  # Базовый шаблон
│   ├── home.html                  # Главная страница
│   └── client.html                # Клиентский интерфейс
├── media/                         # Загружаемые файлы 
│   └── recipe_images/
├── manage.py                      # Управление Django
├── README.md                      # Документация
├── requirements.txt               # Зависимости Python
├── db.sqlite3                     # База данных (только для разработки)
└── tests/                         # Тесты
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
### Запустить сервеh
```bash
python manage.py runserver
```
### Запустить shell
```bash
python manage.py shell
```

#  Примеры данных

### JSON для создания рецепта
```bash
{
  "name": "Оливье",
  "ingredients": ["картошка", "морковь", "горошек", "колбаса", "майонез"],
  "instructions": "1. Отварить овощи\n2. Нарезать кубиками\n3. Смешать с майонезом",
  "cooking_time": 60
}
```
### Ответ API
```bash
{
  "id": 1,
  "name": "Оливье",
  "ingredients": ["картошка", "морковь", "горошек", "колбаса", "майонез"],
  "instructions": "1. Отварить овощи\n2. Нарезать кубиками\n3. Смешать с майонезом",
  "cooking_time": 60
}
```
#  Отладка

Если возникают ошибки:

Проверьте миграции: python manage.py showmigrations

Очистите базу: удалите db.sqlite3 и выполните python manage.py migrate

Проверьте импорты: убедитесь, что в views.py есть from .models import Recipe