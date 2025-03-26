from django.contrib.auth.decorators import login_required,permission_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.views import View
from .forms import NewsForm, SignUpForm
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden
from .forms import NewsForm
from django.utils.timezone import now

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




@permission_required('news.add_news')
@login_required
def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.created_at = now()
            news.save()
            return redirect('news:news_detail', news_id=news.id)
    else:
        form = NewsForm()

    return render(request, 'news/add_news.html', {'form': form})


@login_required
def add_comment(request, news_id):
    news = get_object_or_404(News, id=news_id)
    if request.method == 'POST':
        content = request.POST['content']
        Comment.objects.create(
            news=news,
            content=content,
            author=request.user,
            created_at=now()
        )
    return redirect('news:news_detail', news_id=news.id)



def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='default')
            user.groups.add(group)

            login(request, user)
            return redirect('news:news_list')
    else:
        form = SignUpForm()
    return render(request, 'news/sign_up.html', {'form': form})

@permission_required('news.delete_news')
@login_required
def delete_news(request, news_id):
    news = get_object_or_404(News, id=news_id)
    if request.user == news.author or request.user.has_perm('news.delete_news'):
        news.delete()
        return redirect('news:news_list')
    return HttpResponseForbidden("Вы не можете удалить эту новость.")

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author or request.user.has_perm('news.delete_comment'):
        comment.delete()
        return redirect('news:news_detail', news_id=comment.news.id)
    return HttpResponseForbidden("Вы не можете удалить этот комментарий.")
