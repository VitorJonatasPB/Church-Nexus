from django.db import models
from django.utils import timezone


class Conta(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    ativa = models.BooleanField(default=True)
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - Saldo: R$ {self.saldo}"


class Categoria(models.Model):
    TIPO_CHOICES = (
        ('E', 'Entrada'),
        ('S', 'Saída'),
    )

    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"


class Movimento(models.Model):
    TIPO_CHOICES = (
        ('E', 'Entrada'),
        ('S', 'Saída'),
    )

    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data = models.DateField(default=timezone.now)
    descricao = models.TextField(blank=True)

    conta = models.ForeignKey(Conta, on_delete=models.PROTECT, related_name='movimentos')
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)

    membro = models.ForeignKey(
        'secretaria.Membro',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    nome_participante = models.CharField(max_length=150, blank=True, null=True)

    evento = models.ForeignKey(
        'eventos.Evento',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    comprovante = models.FileField(upload_to='tesouraria/comprovantes/', blank=True, null=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data', '-criado_em']

    def __str__(self):
        return f"{self.get_tipo_display()} - R$ {self.valor} - {self.data}"
