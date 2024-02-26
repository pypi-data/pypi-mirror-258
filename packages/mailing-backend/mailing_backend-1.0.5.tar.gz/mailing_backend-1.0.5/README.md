# Mailing backend

Проект для интеграции МС рассылки с другими Django МС.

## Подготовка

Скачать через pip:

```pip
pip install mailing-backend==1.0.5
```

### settings.py

Добавить проект в INSTALLED_APPS

```python
# File: settings.py

INSTALLED_APPS = [
    ...
    "mailing_backend",
]
```

Установить переменную EMAIL_ENDPOINT_URL

```python
# File: settings.py

EMAIL_ENDPOINT_URL = "http://127.0.0.1:8000/api/v1/mailing/message-send/"
```

Установить переменную EMAIL_BACKEND

```python
# File: settings.py

EMAIL_BACKEND = "mailing_backend.backend.EndpointEmailBackend"
```

## Пример использования:

### serializers.py

```python

#serializers.py
from rest_framework import serializers

class SendUserMSSerializer(serializers.Serializer):

    subject = serializers.CharField()
    body = serializers.CharField()
    email_list = serializers.ListField(child=serializers.CharField(max_length=254))
    from_message = serializers.CharField(required=False, allow_blank=True)
```

### views.py

```python

#views.py
from typing import Any
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from django.core.mail import EmailMessage
from ma_apps.serializers import SendUserMSSerializer

class MessageSendMSView(APIView):
    serializer_class = SendUserMSSerializer #пример обращения к сериализатору
    def post(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> Response:  
      
        message_serializer = SendUserMSSerializer(data=request.data)
        message = EmailMessage()
        message.subject = message_serializer.initial_data.get("subject", '') #string
        message.body = message_serializer.initial_data.get("body", '') #string
        message.to = message_serializer.initial_data.get("email_list", []) #list
        message.from_email = message_serializer.initial_data.get("from_message", '') #string

        result = message.send()
        return Response(result) 
```

### urls.py

```python
#urls.py

from appms import views
from django.urls import path

urlpatterns = [
	path("message-ms-send/", views.MessageSendMSView.as_view(), name="send"),
]
```

## Пример запроса

```JSON
{
    "subject": "Тема сообщения",
    "body": "Содержание сообщения",
    "email_list": ["example1@mail.ru", "example2.@mail.ru"],
    "from_message": "Sender"
}
```

## Сборка

Как собрать проект локально

```bash
python3 -m pip install build
python3 -m build 
```

### Проверка собранного пакета

```bash
python3 -m pip install twine
twine check dist/*
```

### Выкладывание проекта в PYPI

```bash
twine upload dist/*
```
