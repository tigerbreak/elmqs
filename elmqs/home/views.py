from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404

from article.models import Topic

from django.http import HttpResponse
def home(request):
    top_level_topics = Topic.objects.filter(parent__isnull=True)
    return render(request, 'home/home.html', {'top_level_topics': top_level_topics})
