from django.contrib import admin

# Register your models here.
from django.contrib import admin

# 导入article的ArticlerPost的模型

from .models import ArticlePost
# 注册ArticlePost到admin中


from .models import Topic

class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent')
    list_filter = ('parent',)
    search_fields = ('title',)


admin.site.register(Topic,TopicAdmin)


class ArticlePostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'topic', 'created', 'updated')
    list_filter = ('author', 'topic')
    search_fields = ('title',)

admin.site.register(ArticlePost,ArticlePostAdmin)


