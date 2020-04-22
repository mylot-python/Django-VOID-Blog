from django.urls import path
from . import views

app_name = 'movie'

urlpatterns = [
    path('movie/', views.MoviePage.as_view(), name='MoviePage'),
    path('movie/json/', views.MovieJson.as_view(), name='MovieJson'),
]

