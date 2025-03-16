from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now

from .models import News,Comment
# Create your views here.
def new_list(request):
    news=News.objects.all().order_by('-created_at')
    html="<h1>Список новостей</h1>"
    for item in news:
        html += f'<li><a href="/news/{item.id}/">{item.title}</a> ({item.created_at})</li>'
    html += "</ul><br><a href='/news/add/'>Добавить новость</a>"
    return HttpResponse(html)


def news_detail(request, news_id):
    news = get_object_or_404(News, id=news_id)
    comments = news.comments.all()
    html = f"<h1>{news.title}</h1><p>{news.content}</p><p><b>Дата:</b> {news.created_at}</p>"
    html += "<h2>Комментарии:</h2><ul>"
    for comment in comments:
        html += f"<li>{comment.content} ({comment.created_at})</li>"
    html += "</ul>"
    html += f"""
    <h3>Добавить комментарий:</h3>
    <form method="post" action="/news/{news.id}/comment/">
        <input type="hidden" name="csrfmiddlewaretoken" value="{request.COOKIES.get('csrftoken')}">
        <input type="text" name="content" required>
        <button type="submit">Добавить</button>
    </form>
    <br><a href='/news/'>Назад</a>
    """
    return HttpResponse(html)


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
