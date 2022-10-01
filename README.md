### О проекте:

Данный проект является классическим примером отзовика с возможностями API и автоматизированным развертыванием на виртуальном сервере при помощи программного обеспечения Docker.
В качестве фреймворка использовался Django 2.2.16.
Дополнительно использовались следующие пакеты: Django-filter 22.1, Django REST framework 3.12.4, Simple JWT 4.7.2, Docker, Docker-compos.


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Nedrya/yamdb_fina
```

```
cd yamdb_fina
```

Отредактируйте хосты в файле  "api_yamdb\api_yamdb\setting.py":

```
ALLOWED_HOSTS = ['указать IP или Host']
```



Выполните в коандной строке команды:

```
git add .
```
```
git commit -m 'test'
```
```
git push
```

Выполните терминальное соединение с контейнером:

```
sudo docker exec -it camana_web_1 bash
```

Выполнить в терминальном соединении миграции и создайте суперюзера:

```
python3 manage.py makemigrations
```
```
python3 manage.py migrate
```
```
python manage.py createsuperuser
```


### Управление контейнерами:


Для запуска или останова контейнеров используйте команды:

```
sudo docker-compose up -d
```
```
sudo docker-compose down
```

### Бейдж о статусе работы workflow:

![example workflow](https://github.com/Nedrya/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

### Информация:

Регистрация:
Регистрация происходит путем отправки POST запроса с указание пользовательского имени и адреса электронной почты.

Пример запроса регистрации нового пользрвателя:
```
POST http://127.0.0.1:8000/api/v1/auth/signup/
Content-Type: application/json

{
    "username": "1112",
    "email": "1112@qwe.ru"
}
```

Пример ответа:
```
{
  "email": "1112@qwe.ru",
  "username": "1112"
}
```

После успешной регистрации на почту придет секретный код, который позволит подтвердить почту и получить токен аутентификации.
Пример секретного кода: MSBrKI8ZkD


Подтверждение адреса электронной почты и получение токена аутентификации:

Пример запроса:
```
POST http://127.0.0.1:8000/api/v1/auth/signup/
Content-Type: application/json

{
    "username": "1112",
    "confirmation_code": "MSBrKI8ZkD"
}
```

Пример ответа:
```
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU3NjEyMzg1LCJqdGkiOiJiNjI4N2Y3Y2JhMGQ0ZThjOGM3NGM2MTcwMDI4NjdkMCIsInVzZXJfaWQiOjEsInVzZXJuYW1lIjoiMTExMiIsImNvbmZpcm1hdGlvbl9jb2RlIjoiTVNCcktJOFprRCJ9.5wo80prs8WWwIZrsESG-fL9xl0jfNSYVq5mdFdpIVxs"
}
```

Подробнее с примерами запросов можно ознакомиться по ссылке http://127.0.0.1:8000/redoc/ .

Автор проекта: Недря Сергей
