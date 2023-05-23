from django.urls import path

from .views import ListTask, DetailTask

urlpatterns = [
    path('task/', ListTask.as_view()),
    path('task/<int:pk>/', DetailTask.as_view()),
]