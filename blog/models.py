from django.db import models
from django.utils import timezone


class Post(models.Model):
    title = models.CharField('título', max_length=200)
    content = models.TextField('conteúdo')  # guarda HTML
    published_at = models.DateTimeField('data de postagem', default=timezone.now)

    class Meta:
        ordering = ['-published_at']  # mais recentes primeiro

    def __str__(self):
        return self.title
