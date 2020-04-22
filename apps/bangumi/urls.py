from django.urls import path
from . import views

app_name = 'bangumi'

urlpatterns = [
    path('bangumi/', views.BangumiPage.as_view(), name='BangumiPage'),
    path('bangumi/json/', views.BangumiJson.as_view(), name='BangumiJson'),
]
