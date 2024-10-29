from django.db import models

# Create your models here.
from django.db import models
#导入django的内建user模型
from django.contrib.auth.models import User
from django.utils import timezone
#引入表单类
from django import forms

class Topic(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    @property
    def level(self):
        # 计算主题层级，顶级为0，子主题依次加1
        level = 0
        current = self.parent
        while current:
            level += 1
            current = current.parent
        return level
    def __str__(self):
        return self.title
class ArticlePost(models.Model):
    # 文章作者。参数 on_delete 用于指定数据删除的方式，当关联的用户（作者）被删除时，与该用户关联的所有文章也会被自动删除。
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    #文章标题。
    title = models.CharField(max_length=200)
    #文章的正文。保存大量文本使用TextField
    body = models.TextField()

    #文章的浏览量
    total_views = models.PositiveIntegerField(default=0)
    #文章发布时间。
    created = models.DateTimeField(default=timezone.now)
    #文章最后修改时间。
    updated = models.DateTimeField(auto_now=True)
    #设置主题的外键
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE,null=True,blank=True,related_name='articles')

    class Meta:
         # 文章按照发布时间倒序排列。
        ordering = ['-created']

    def __str__(self):
        return self.title

