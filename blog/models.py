from django.conf import settings
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


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='post',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='autor',
    )
    text = models.TextField('texto')
    created_at = models.DateTimeField('data de postagem', default=timezone.now)

    class Meta:
        ordering = ['-created_at']  # mais recentes primeiro

    def __str__(self):
        return f'Comentário de {self.author} em {self.post}'
