from django.db import models
from django.utils import timezone
from django.db.models import Sum, F
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.apps import apps



class Evento(models.Model):
    nome = models.CharField(max_length=200)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    valor_necessario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Valor necessário para que o participante fique ativo"
    )

    def __str__(self):
        return self.nome


class Participante(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="participantes")
    nome = models.CharField(max_length=150)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    data_inscricao = models.DateField(default=timezone.now)
    valor_necessario = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ativo = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Se valor_necessario não foi definido, pega do evento
        if self.evento and not self.valor_necessario:
            self.valor_necessario = self.evento.valor_necessario
        super().save(*args, **kwargs)

    def __str__(self): 
        return self.nome
    
    @property
    def total_pago(self):
        # self.pagamentos é o related_name do Pagamento
        return sum(p.valor_pago for p in self.pagamentos.all())
        
    def atualizar_status(self):
        self.ativo = self.total_pago >= self.valor_necessario
        self.save()

#class Produto(models.Model):
#    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="produtos")
#    nome = models.CharField(max_length=150)
#    preco = models.DecimalField(max_digits=10, decimal_places=2)
#    estoque = models.PositiveIntegerField(default=0)
#
#    def total_pago(self):
#        return self.pagamentos.aggregate(total=Sum('valor_pago'))['total'] or 0
#
#    def atualizar_status(self):
#        self.ativo = self.total_pago() >= self.valor_necessario
#        self.save() 
#
#    def __str__(self):
#        return self.nome

class Pagamento(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="pagamentos")
    participante = models.ForeignKey(Participante,
                                    related_name='pagamentos',
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank=True,
                                    )
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2)
    forma_pagamento = models.CharField(
        max_length=30,
        choices=[('PIX','PIX'), ('DINHEIRO','Dinheiro'), ('CARTAO','Cartão')]
    )
    conta = models.ForeignKey(
                            'tesouraria.Conta',
                            on_delete=models.PROTECT,
                            null=True,
                            blank=True
                        )
    confirmado = models.BooleanField(default=False)
    data_pagamento = models.DateTimeField(auto_now_add=True)
    movimento_gerado = models.BooleanField(default=False)

    def registrar_movimento_pagamento(self):
        if self.confirmado and not self.movimento_gerado and self.valor_pago > 0:
            from apps.tesouraria.models import Conta, Categoria, Movimento
    
            # Conta padrão caso não escolha
            if not self.conta:
                self.conta, _ = Conta.objects.get_or_create(nome="Caixa Geral")
    
            # Categoria padrão para inscrições
            categoria, _ = Categoria.objects.get_or_create(nome="Inscrição Evento", tipo='E')
    
            # Cria movimento com participante como nome (string)
            Movimento.objects.create(
                tipo='E',
                valor=self.valor_pago,
                conta=self.conta,
                categoria=categoria,
                membro=None,  # não há FK Membro
                nome_participante=self.participante.nome if self.participante else None,
                evento=self.participante.evento if self.participante else None,
                descricao=f"Pagamento inscrição - {self.participante.evento.nome if self.participante else ''}"
            )
    
            self.movimento_gerado = True
            self.save(update_fields=['movimento_gerado'])


