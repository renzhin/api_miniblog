### Описание проекта:

Проект API_FINAL_YATUBE.

Репозиторий бекэнд составляющей приложения блога(инфоресурса).

Проект реализован на языке python, при помощи фрейворков:  Django, Django REST Framework.

В прроекте реализован API для работы с публикациями, комментариями к публикациям и взаимодействию пользователей. На примере приложения можно ознакомится с основами работы Django REST Framework.


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:IvanMarchenko69/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение в Windows:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```


### Примеры:

Всю мнформацию о форме запросов и ответов приложения можно найти после развертывания и запуска приложения по адресу url: 
```
http://127.0.0.1:8000/redoc/
```
Примеры запросов:
Запрос отдельного поста.
адресу url: 
```
http://127.0.0.1:8000/api/v1/posts/{id}/
```
metod GET
ожидаемый результат:
{
    "id": 0,
    "author": "string",
    "text": "string",
    "pub_date": "2019-08-24T14:15:22Z",
    "image": "string",
    "group": 0
}

Создание комментария.
адресу url: 
```
http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/
```
metod POST
{
    "text": "string"
}
ожидаемый результат:
{
    "id": 0,
    "author": "string",
    "text": "string",
    "created": "2019-08-24T14:15:22Z",
    "post": 0
}

Получение токена.
адресу url: 
```
http://127.0.0.1:8000/api/v1/jwt/create/
```
metod POST
{
    "username": "string",
    "password": "string"
}

ожидаемый результат:
{
    "refresh": "string",
    "access": "string"
}

### Авторы:
Марченко И.Н.
e-mail: ionmen@mail.ru
