from django.urls import path
from .views import redoc, redoc_json

urlpatterns = [
    path("", redoc),
    path("json/", redoc_json)
]
