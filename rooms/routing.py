from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/rooms/room/(?P<room_code>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/rooms/room/(?P<room_code>\w+)/join/$', consumers.CallConsumer.as_asgi()),
]