from django.shortcuts import render

# Create your views here.
# 导入 HttpResponse 模块
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import ArticlePost
from .forms import ArticlePostForm
from django.contrib.auth.models import User
# 视图函数
import markdown
def article_list(request):
    #取出所有的博客文章
    articles = ArticlePost.objects.all()
    context = {'articles': articles}
    return render(request, 'article/list.html', context)
#这是没有增加marke的版本
# def article_detail(request, id):
#     article = ArticlePost.objects.get(id=id)
#     context = {'article': article}
#     return render(request, 'article/detail.html', context)
#这是增加marke的版本
def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)
    #将markdown语法渲染成html样式,将article的body进行markwdown渲染
    article.body = markdown.markdown(article.body, extensions=[
        #包含缩写，表格等常用拓展
        'markdown.extensions.extra',
        #语法高亮拓展
        'markdown.extensions.codehilite',
    ])
    context = {'article': article}
    return render(request, 'article/detail.html', context)

def article_create(request):
    if request.method == 'POST':
        article_post_form = ArticlePostForm(request.POST)
        if article_post_form.is_valid():
            #保存数据，但是不提交到数据库中
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=1)
            new_article.save()
            return redirect("article:article_list")
    else:
        article_get_form = ArticlePostForm()
        context = {'article_get_form': article_get_form}
        return render(request, 'article/create.html', context)

def article_delete(request, id):
    article = ArticlePost.objects.get(id=id)
    article.delete()
    return redirect("article:article_list")


def article_update(request,id):
    """
    更新文章的视图函数
    通过POST方法提交表单，更新titile、body字段
    GET方法进入初始表单页面
    id： 文章的 id
    """
    #获取当前的IDarticle实例
    article = ArticlePost.objects.get(id=id)
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            #问题：为什么不直接保存article_post_form,原因：如果使用的话，还得传参atuhor的id。而且改变的可能不是这个id的Article,也有可能是，还没实验。
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            #article_post_form.save()
            return redirect("article:article_list")
        else:
            return HttpResponse('表单验证失败，请重新填写')
    else:
        article_post_form = ArticlePostForm()
        context = {'article': article, 'article_post_form': article_post_form}
        return render(request, 'article/update.html', context)
