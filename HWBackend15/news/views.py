from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.views import View
from .forms import NewsForm

from .models import News,Comment
# Create your views here.
class NewsUpdateView(View):
    def get(self,request,news_id):
        news=get_object_or_404(News,id=news_id)
        form = NewsForm(instance=news)
        return render(request,'news/edit_news.html',{'form':form,'news':news})

    def post(self,request,news_id):
        news=get_object_or_404(News,id=news_id)
        form=NewsForm(request.POST,instance=news)
        if form.is_valid():
            form.save()
            return redirect('news:news_detail',news_id=news.id)
        return render(request,'news/edit_news.html',{'form':form,'news':news})

def news_list(request):
    news_list = News.objects.all().order_by('-created_at')
    return render(request, 'news/news_list.html', {
        'news_list': news_list
    })
def news_detail(request, news_id):
    news = get_object_or_404(News, id=news_id)
    comments = news.comments.order_by('-created_at')
    return render(request, 'news/news_detail.html', {
        'news': news,
        'comments': comments
    })


from .forms import NewsForm
from django.utils.timezone import now


def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.created_at = now()
            news.save()
            return redirect('news:news_detail', news_id=news.id)
    else:
        form = NewsForm()

    return render(request, 'news/add_news.html', {'form': form})


def add_comment(request, news_id):
    news = get_object_or_404(News, id=news_id)
    if request.method == 'POST':
        content = request.POST['content']
        Comment.objects.create(news=news, content=content, created_at=now())
    return redirect('news:news_detail', news_id=news.id)
