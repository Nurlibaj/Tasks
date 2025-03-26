from django.db import models
from django.contrib.auth.models import User


class News(models.Model):
    title=models.CharField(max_length=255)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return self.title

    def has_comments(self):
        return self.comments.exists()


class Comment(models.Model):
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    news=models.ForeignKey(News,on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.news.title
