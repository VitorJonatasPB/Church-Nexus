from django.db import models
from django.utils.html import mark_safe

class Area(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.nome
class Congregacao(models.Model):
    nome = models.CharField(max_length=100)
    data_cadastro = models.DateField(auto_now_add=True, db_index=True)
    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='congregacao'
    )
    class Meta:
        verbose_name = "Congregação"
        verbose_name_plural = "Congregações"
    def __str__(self):
        return f"{self.nome}"
    
class Membro(models.Model):
    CARGO_CHOICES = [
        ('Membro', 'Membro'),
        ('Congregado', 'Congregado'),
        ('Discípulo(a)', 'Discípulo(a)'),
        ('Diácono(a)', 'Diácono(a)'),
        ('Missionário(a)', 'Missionário(a)'),
        ('Presbítero', 'Presbítero'),
        ('Evangelista', 'Evangelista'),
        ('Pastor(a)', 'Pastor(a)'),
    ]
    area = models.ForeignKey(
        Area,
        on_delete=models.PROTECT,
        related_name='membros'
    )
    
    congregacao = models.ForeignKey(
        'Congregacao',
        on_delete=models.PROTECT,
        related_name='membros',
    )
    
    nome = models.CharField(max_length=100)
    data_cadastro = models.DateField(auto_now_add=True, db_index=True)
    data_de_nascimento = models.DateField()
    email = models.EmailField(unique=True,
                            null = True,
                            blank = True)
    
    telefone = models.CharField(max_length=20)
    endereco = models.TextField()
    cargo = models.CharField(max_length=50)
    cargo = models.CharField(max_length=50, 
                            choices=CARGO_CHOICES, 
                            default='Membro')
    ativo = models.BooleanField(default=True)
    foto = models.ImageField(upload_to='fotos_membros/', null=True, blank=True)
    def foto_preview(self):
        if self.foto:
            return mark_safe(f'<img src="{self.foto.url}" width="100" height="100" style="object-fit: cover;"/>')
        return "Sem foto"
    foto_preview.short_description = "Foto"
    def __str__(self):
        return self.nome
