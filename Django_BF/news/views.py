from django.shortcuts import render, redirect
from .BeautifulSoupPars import fill_data
from .models import Category,News

def list_news(request):
    news = News.objects.all()
    context = {'news':news}
    return render(request,'index.html',context=context)


def refresh_news(request):
    fill_data()
    return redirect('news')