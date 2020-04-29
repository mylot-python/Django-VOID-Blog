from django.urls import path
from . import views

app_name = 'music'

urlpatterns = [
    path('music/', views.MusicPage.as_view(), name='MusicPage'),
    path('music/api/', views.MusicApi.as_view(), name='MusicApi'),
]


