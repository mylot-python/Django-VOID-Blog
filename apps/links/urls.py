from django.urls import path
from . import views

app_name = 'links'

urlpatterns = [
    path('links/', views.LinksPage.as_view(), name='LinksPage'),
]

