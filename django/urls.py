from django.urls import path
from .views import Analyze

app_name = "count_objects"
urlpatterns = [
    path('submit/<pk>/',Analyze.as_view(),name="analyze"),
]
