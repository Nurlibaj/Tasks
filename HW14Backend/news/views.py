from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now

from .models import News,Comment
# Create your views here.
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



def add_news(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        news = News.objects.create(title=title, content=content, created_at=now())
        return redirect('news:news_detail', news_id=news.id)

    html = """
    <h1>Добавить новость</h1>
    <form method="post">
        <input type="text" name="title" placeholder="Название" required><br>
        <textarea name="content" placeholder="Текст новости" required></textarea><br>
        <button type="submit">Добавить</button>
    </form>
    <br><a href='/news/'>Назад</a>
    """

    return HttpResponse(html)
def add_comment(request, news_id):
    news = get_object_or_404(News, id=news_id)
    if request.method == 'POST':
        content = request.POST['content']
        Comment.objects.create(news=news, content=content, created_at=now())
    return redirect('news:news_detail', news_id=news.id)
