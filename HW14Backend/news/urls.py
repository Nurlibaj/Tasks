from . import views
from django.urls import path

app_name = "news"

urlpatterns = [
    path('', views.new_list, name="new_list"),
    path('<int:news_id>/', views.news_detail, name='news_detail'),
    path('add/', views.add_news, name='add_news'),
    path('<int:news_id>/comment/', views.add_comment, name='add_comment'),
]
