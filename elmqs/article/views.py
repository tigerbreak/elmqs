from django.shortcuts import render

# Create your views here.
# 导入 HttpResponse 模块
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import ArticlePost
from .forms import ArticlePostForm
from django.contrib.auth.models import User
# 视图函数
from django.core.paginator import Paginator
import markdown
from .models import Topic

def build_topic_tree(topics):
    """
    构建主题树的结构。

    参数:
        topics (QuerySet): 包含主题的查询集。

    返回:
        list: 一个包含主题及其子主题和相关文章的嵌套列表。
    """
    tree = []  # 初始化主题树
    for topic in topics:  # 遍历每个主题
        sub_topics = topic.children.all()  # 获取当前主题的子主题
        # 添加当前主题的信息，包括子主题的递归结构
        tree.append({
            'topic': topic,
            'articles': topic.articles.all(),  # 获取当前主题的所有文章
            'sub_topics': build_topic_tree(sub_topics),  # 递归调用构建子主题树
        })
    return tree  # 返回构建好的主题树



def article_list(request):
    #取出所有的博客文章
    articles = ArticlePost.objects.all()
    #每页显示2篇文章
    paginator = Paginator(articles, 8)
    #取出第一页的文章
    page = request.GET.get('page')
    articles = paginator.get_page(page)


    topics = Topic.objects.filter(parent__isnull=True)  # 获取顶级主题
    topic_tree = build_topic_tree(topics)  # 构建主题树

    context = {'articles': articles}

    return render(request, 'article/list.html', context)
#这是没有增加marke的版本
# def article_detail(request, id):
#     article = ArticlePost.objects.get(id=id)
#     context = {'article': article}
#     return render(request, 'article/detail.html', context)
#这是增加marke的版本
def article_detail(request, id):
    """
    处理文章详细信息的请求。

    参数:
        request (HttpRequest): 请求对象。
        id (int): 文章的唯一标识符。

    返回:
        HttpResponse: 渲染的文章详情页面。
    """
    # 根据文章的ID获取相应的文章对象
    article = ArticlePost.objects.get(id=id)

    # 浏览量 +1
    article.total_views += 1  # 增加文章的浏览量
    article.save(update_fields=['total_views'])  # 保存更新的浏览量

    # 保存原始的 markdown 内容
    raw_body = article.body  # 备份原始的文章内容
    print("row_body_generated:", raw_body)  # 打印原始内容以供调试

    # 将markdown语法渲染成HTML
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',  # 包含缩写、表格等常用扩展
        'markdown.extensions.codehilite',  # 语法高亮扩展
        'markdown.extensions.toc',  # 目录扩展
    ])

    # 将文章的Markdown内容转换为HTML
    article.body = md.convert(article.body)


    # # 获取文章主题层级
    # topic_hierarchy = []
    # current_topic = article.topic
    #
    # while current_topic:
    #     topic_hierarchy.append(current_topic)
    #     current_topic = current_topic.parent
    # topic_hierarchy.reverse()  # 反转以从顶层到当前层级
    # print(topic_hierarchy)
    # 获取顶级主题
    current_topic = article.topic
    while current_topic.parent:
        current_topic = current_topic.parent

    top_level_topic = current_topic

    # 获取所有子主题及其对应的文章
    def get_all_sub_topics(topic):
        sub_topics = [topic]  # 包含当前主题
        for child in topic.children.all():
            sub_topics.extend(get_all_sub_topics(child))  # 递归获取子主题
        return sub_topics

    topic_hierarchy = get_all_sub_topics(top_level_topic)

    # 获取顶级主题
    top_level_topic = topic_hierarchy[0] if topic_hierarchy else None


    # 递归获取所有层级文章
    def get_all_articles(topic):
        articles = list(ArticlePost.objects.filter(topic=topic))
        for child in topic.children.all():
            articles.extend(get_all_articles(child))

        return articles

    all_articles = get_all_articles(top_level_topic)
    print(all_articles)
    context = {
        'article': article,
        'toc': md.toc,
        'topic_hierarchy': topic_hierarchy,
        'all_articles': all_articles,  # 所有层级的文章
    }

    # 渲染并返回文章详情页面
    return render(request, 'article/detail.html', context)

def article_create(request):
    if request.method == 'POST':
        topics = Topic.objects.all()
        article_post_form = ArticlePostForm(request.POST)
        if article_post_form.is_valid():
            #保存数据，但是不提交到数据库中


            new_article = article_post_form.save(commit=False)
            if request.POST['topic'] != 'none':
                new_article.topic = Topic.objects.get(id=request.POST['topic'])
            new_article.author = User.objects.get(id=1)
            new_article.save()
            return redirect("article:article_list")
    else:
        topics = Topic.objects.all()
        article_get_form = ArticlePostForm()
        context = {'article_get_form': article_get_form,'topics':topics}
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
            if request.POST['topic'] != 'none':
                article.topic = Topic.objects.get(id=request.POST['topic'])
            article.save()
            #article_post_form.save()
            return redirect("article:article_list")
        else:
            return HttpResponse('表单验证失败，请重新填写')
    else:
        article_post_form = ArticlePostForm()
        topics = Topic.objects.all()
        context = {'article': article, 'article_post_form': article_post_form,'topics':topics}
        return render(request, 'article/update.html', context)

