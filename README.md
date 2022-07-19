### Веб-проект "Напарники"
Проект "Напарники" - сайт из категории "Блог", бекенд которого целиком написан на [Python](https://github.com/python) и [Django](https://github.com/django/django)

В проекте реализована возможность создания комнат (Room), к которым можно присоединиться в качестве участника (User) и оставлять комментарии (Message), ведя тем самым переписку между участниками комнаты. Каждая комната принадлежит к какой-либо тематике (Topic). 

Любой авторизованный пользователь может создать комнату (Room) и присоеденить её к новой или уже существующей тематике (Topic). Данный пользователь будет закреплен за данной комнатой как создатель (Host). Любой авторизованный пользователь может зайти в комнату и оставить комментарий (Message). Неавторизованные пользователи не могут создавать ни комнат, ни комментариев в комнатах. Авторизованный пользователь может изменить свое имя (Name), никнейм (Username), биографию (Bio) и аватар (Avatar) в настройках профиля.

![alt text](https://github.com/Fr0stFree/Teammates/blob/main/home.jpg?raw=true)

---
### Использованные технологии
1. [Python](https://github.com/python)
2. [Django](https://github.com/django/django)
3. [Django REST framework](https://github.com/encode/django-rest-framework)
4. [pytest](https://github.com/pytest-dev/pytest)
5. [Pillow](https://github.com/python-pillow/Pillow)
6. [Swagger](https://github.com/axnsan12/drf-yasg)
---
### Запуск проекта
- Клонировать репозиторий
```
git clone https://github.com/Fr0stFree/Blog-project
```
- Установить и активировать виртуальное окружение
```
python -m venv venv
source venv/Scripts/activate (Windows OS)
или
source venv/bin/activate (Unix OS)
```
- Установить необходимые зависимости requirements.txt
```
pip install -r requirements.txt
```
- Выполнить миграции:
```
python manage.py makemigrations
python manage.py migrate
```
- Запустить проект
```
python manage.py runserver
```
- Перейти по ссылке http://127.0.0.1:8000/
