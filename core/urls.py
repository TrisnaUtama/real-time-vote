from django.contrib import admin
from django.urls import path, include
from core.consumers import PollConsumer

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("app.urls"))
]

websocket_urlpatterns = [
    path('ws/polls/', PollConsumer.as_asgi()), 
    path('ws/polls/<str:poll_id>/', PollConsumer.as_asgi()), 
]
