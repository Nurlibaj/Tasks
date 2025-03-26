from . import views
from django.urls import path
from .views import sign_up

app_name = "news"

urlpatterns = [
    path('', views.news_list, name="news_list"),
    path('<int:news_id>/', views.news_detail, name='news_detail'),
    path('add/', views.add_news, name='add_news'),
    path('<int:news_id>/comment/', views.add_comment, name='add_comment'),
    path('<int:news_id>/edit/',views.NewsUpdateView.as_view(), name='news_edit'),
    path('sign-up/', sign_up, name='sign_up'),
    path('<int:news_id>/delete/', views.delete_news, name='news_delete'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='comment_delete'),

]
