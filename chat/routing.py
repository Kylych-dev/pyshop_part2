from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/socket-server/', consumers.ChatConsumer.as_asgi()),
]


'''
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/socket-server/', consumers.ChatConsumer)
]

'''


'''
TypeError: 'list' object is not callable WebSocket closed for ['127.0.0.1', 54468]


'''