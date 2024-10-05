from django.shortcuts import render

# Create your views here.
# 导入 HttpResponse 模块
from django.http import HttpResponse
from django.shortcuts import render
from .models import ArticlePost
# 视图函数
def article_list(request):
    #取出所有的博客文章
    articles = ArticlePost.objects.all()
    context = {'articles': articles}
    return render(request, 'article/list.html', context)