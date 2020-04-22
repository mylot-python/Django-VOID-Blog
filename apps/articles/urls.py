from django.urls import path
from . import views

app_name = 'article'

urlpatterns = [
    path('', views.IndexView.as_view(), name='IndexPage'),
    path('article/<int:article_id>/', views.ArticleDetail.as_view(), name='ArticleDetail'),
    path('article/comments/<int:id>/', views.ArticleComments.as_view(), name='ArticleComments'),
    path('article/vote/', views.ArticleVote.as_view(), name='ArticleVote'),
    path('tag/<str:tag_name>/', views.ArticleForTag.as_view(), name='ArticleForTag'),
    path('category/<str:cls_name>/', views.ArticleForCategory.as_view(), name='ArticleForCategory'),
    path('archives/', views.ArticleArchives.as_view(), name='ArticleArchives'),
    path('search/', views.SearchJson.as_view(), name='SearchJson'),
]


