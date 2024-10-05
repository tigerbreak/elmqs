from django.urls import path
app_name = 'article'
from . import views
urlpatterns = [
    path('article-list/', views.article_list, name='article_list'),
]