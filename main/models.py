from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Screenshot(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_screenshots')
    title = models.CharField(max_length=255)
    screenshot = models.ImageField(upload_to='%Y/%m/%d', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('screen_detail', args=[self.pk])








