from django import forms
# 引入文章模型
from .models import ArticlePost
#将写文章的类实例成一个表单实例

class ArticlePostForm(forms.ModelForm):
    class Meta:
        # 指定表单对应的模型
        model = ArticlePost
        # 指定表单显示的字段
        fields = ('title', 'body')

