from django.urls import path
from . import views

app_name = 'book'

urlpatterns = [
    path('book/', views.BookPage.as_view(), name='BookPage'),
    path('book/json/', views.BookJson.as_view(), name='BookJson'),
]