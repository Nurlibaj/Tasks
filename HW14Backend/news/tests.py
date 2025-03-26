from django.test import TestCase
from .models import News, Comment
from django.utils import timezone
from django.urls import reverse

class NewsModelTests(TestCase):
    def test_has_comments_true(self):
        news = News.objects.create(title="Test", content="Some text", created_at=timezone.now())
        Comment.objects.create(news=news, content="Comment", created_at=timezone.now())
        self.assertTrue(news.has_comments())

    def test_has_comments_false(self):
        news = News.objects.create(title="Test", content="Some text", created_at=timezone.now())
        self.assertFalse(news.has_comments())


class NewsViewsTests(TestCase):
    def setUp(self):
        self.news1 = News.objects.create(title="Old News", content="old", created_at=timezone.now())
        self.news2 = News.objects.create(title="New News", content="new", created_at=timezone.now())

    def test_news_list_sorted(self):
        response = self.client.get(reverse('news:news_list'))
        self.assertEqual(response.status_code, 200)
        news_list = list(response.context['news_list'])
        self.assertTrue(news_list[0].created_at >= news_list[1].created_at)

    def test_news_detail(self):
        response = self.client.get(reverse('news:news_detail', args=[self.news1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.news1.title)

    def test_news_detail_comment_order(self):
        Comment.objects.create(news=self.news1, content="Old comment", created_at=timezone.now())
        Comment.objects.create(news=self.news1, content="New comment", created_at=timezone.now())
        response = self.client.get(reverse('news:news_detail', args=[self.news1.pk]))
        comments = list(response.context['comments'])
        self.assertTrue(comments[0].created_at >= comments[1].created_at)
