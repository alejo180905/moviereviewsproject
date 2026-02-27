from django.shortcuts import render
from .models import News


def news_list(request):
    # Lista noticias ordenadas por fecha descendente
    news = News.objects.all().order_by('-date')
    return render(request, 'news.html', {'news_list': news})
