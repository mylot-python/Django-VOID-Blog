from django.urls import path
from . import views

app_name = 'music'

urlpatterns = [
    path('music/', views.MusicPage.as_view(), name='MusicPage'),
]


