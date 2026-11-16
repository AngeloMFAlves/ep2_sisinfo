from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone

from blog.models import Post, Category, Comment

# Se já existem posts, o banco já foi populado: não faz nada.
if Post.objects.exists():
    print('Banco já populado; nada a fazer.')
    raise SystemExit

User = get_user_model()
agora = timezone.now()


def obter_usuario(username):
    """Cria o usuário se não existir; se já existir, reaproveita."""
    user, criado = User.objects.get_or_create(username=username)
    if criado:
        user.set_unusable_password()
        user.save()
    return user


# Usuários (autores dos comentários)
maria = obter_usuario('maria')
joao = obter_usuario('joao')

# Categorias
tecnologia, _ = Category.objects.get_or_create(
    name='Tecnologia',
    defaults={'description': 'Novidades, projetos e ferramentas de tecnologia'},
)
musica, _ = Category.objects.get_or_create(
    name='Música',
    defaults={'description': 'Música, instrumentos e produção sonora'},
)
medicina, _ = Category.objects.get_or_create(
    name='Medicina',
    defaults={'description': 'Medicina, saúde e bem-estar'},
)

# Post 1: Música + Tecnologia
p1 = Post.objects.create(
    title='Sintetizador MIDI com ESP32',
    content=(
        '<p>Neste projeto, um <strong>ESP32</strong> lê potenciômetros e botões '
        'e transforma cada gesto em uma nota <em>MIDI</em>, enviada por Bluetooth '
        'para o celular ou o computador.</p>'
        '<p>Com isso, o microcontrolador vira um pequeno instrumento musical '
        'sem fio:</p>'
        '<ul>'
        '<li>botões para escolher as notas;</li>'
        '<li>um potenciômetro para controlar o volume;</li>'
        '<li>comunicação sem fio via Bluetooth Low Energy.</li>'
        '</ul>'
    ),
    published_at=agora - timedelta(days=3),
)
p1.categories.add(musica, tecnologia)

# Post 2: Tecnologia + Medicina
p2 = Post.objects.create(
    title='Monitor de batimentos cardíacos com ESP32',
    content=(
        '<p>Usando um <strong>ESP32</strong> e um sensor óptico de pulso, '
        'como o <em>MAX30102</em>, é possível medir a frequência cardíaca e '
        'acompanhar os dados em tempo real.</p>'
        '<p>O projeto é <strong>educacional</strong>: ele mostra como a '
        'eletrônica pode apoiar o acompanhamento da saúde, mas não substitui '
        'um equipamento médico nem serve para diagnóstico.</p>'
    ),
    published_at=agora - timedelta(days=2),
)
p2.categories.add(tecnologia, medicina)

# Post 3: apenas Tecnologia (sem comentários)
p3 = Post.objects.create(
    title='IA embarcada: inteligência artificial em microcontroladores',
    content=(
        '<p>Uma tendência que vem ganhando espaço é a <strong>IA embarcada</strong> '
        '(também chamada de <em>TinyML</em>): modelos pequenos de aprendizado de '
        'máquina que rodam direto em microcontroladores, sem depender da nuvem.</p>'
        '<p>As vantagens são menor latência, menor consumo de energia e mais '
        'privacidade, já que os dados não precisam sair do dispositivo.</p>'
    ),
    published_at=agora - timedelta(days=1),
)
p3.categories.add(tecnologia)

# Comentários do post 1: conversa entre maria e joão
Comment.objects.create(
    post=p1, author=maria,
    text='Adorei o projeto! A latência do Bluetooth ficou boa nos seus testes?',
    created_at=agora - timedelta(days=2, hours=20),
)
Comment.objects.create(
    post=p1, author=joao,
    text=('Ficou bem baixa, dá para tocar sem perceber atraso. '
          'Estou pensando em adicionar um sensor de toque para controlar o volume.'),
    created_at=agora - timedelta(days=2, hours=6),
)
Comment.objects.create(
    post=p1, author=maria,
    text=('Um sensor de toque cairia bem: o ESP32 já tem pinos de toque capacitivo. '
          'Dá para mapear cada pino a uma nota!'),
    created_at=agora - timedelta(days=1, hours=12),
)

# Comentários do post 2: conversa entre joão e maria
Comment.objects.create(
    post=p2, author=joao,
    text='Muito bom! Mas a leitura do sensor não oscila bastante com o movimento do dedo?',
    created_at=agora - timedelta(days=1, hours=20),
)
Comment.objects.create(
    post=p2, author=maria,
    text=('Oscila sim, por isso vale filtrar o sinal com uma média móvel '
          'antes de calcular a frequência cardíaca.'),
    created_at=agora - timedelta(days=1, hours=8),
)
Comment.objects.create(
    post=p2, author=joao,
    text=('Boa dica! Também dá para enviar os dados por Wi-Fi para um painel '
          'e acompanhar a evolução ao longo do dia.'),
    created_at=agora - timedelta(hours=20),
)

print('Dados criados com sucesso.')
print(f'Posts: {Post.objects.count()} | Categorias: {Category.objects.count()} | '
      f'Comentários: {Comment.objects.count()}')
