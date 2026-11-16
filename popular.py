from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone

from blog.models import Post, Category, Comment

User = get_user_model()
agora = timezone.now()

# Usuários (autores dos comentários)
maria = User.objects.create_user('maria', password='senha12345')
joao = User.objects.create_user('joao', password='senha12345')

# Categorias
django, _ = Category.objects.get_or_create(
    name='Django', defaults={'description': 'Posts sobre o framework Django'})
python, _ = Category.objects.get_or_create(
    name='Python', defaults={'description': 'Posts sobre a linguagem Python'})
git, _ = Category.objects.get_or_create(
    name='Git', defaults={'description': 'Posts sobre controle de versão com Git'})

# Posts
p1 = Post.objects.create(
    title='Introdução ao Django',
    content='<p>O <strong>Django</strong> é um framework web feito em Python.</p>',
    published_at=agora - timedelta(days=3),
)
p1.categories.add(django, python)

p2 = Post.objects.create(
    title='Automatizando tarefas com Python e Git',
    content='<p>Scripts em <em>Python</em> e hooks do <strong>Git</strong> poupam tempo.</p>',
    published_at=agora - timedelta(days=2),
)
p2.categories.add(python, git)

p3 = Post.objects.create(
    title='Dicas de templates no Django',
    content='<p>Use <strong>herança de templates</strong> para evitar repetição.</p>',
    published_at=agora - timedelta(days=1),
)
p3.categories.add(django)

# Comentários (o post 3 fica sem comentários de propósito)
Comment.objects.create(post=p1, author=maria, text='Ótima introdução!',
                       created_at=agora - timedelta(days=2, hours=5))
Comment.objects.create(post=p1, author=joao, text='Ajudou muito, obrigado.',
                       created_at=agora - timedelta(days=2))
Comment.objects.create(post=p1, author=maria, text='Quero ver mais sobre models.',
                       created_at=agora - timedelta(days=1, hours=3))

Comment.objects.create(post=p2, author=joao, text='Boa ideia usar hooks.',
                       created_at=agora - timedelta(days=1, hours=6))
Comment.objects.create(post=p2, author=maria, text='Vou testar isso hoje.',
                       created_at=agora - timedelta(hours=12))

print('Dados criados com sucesso.')
