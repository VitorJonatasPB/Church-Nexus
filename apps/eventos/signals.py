# apps/eventos/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.eventos.models import Pagamento

@receiver(post_save, sender=Pagamento)
def atualizar_ativo_e_gerar_movimento(sender, instance, **kwargs):
    """
    Ao salvar um Pagamento:
    1. Atualiza o status do participante (ativo ou não)
    2. Cria o movimento na Tesouraria se confirmado
    """
    # Atualiza status do participante
    if instance.participante:
        instance.participante.atualizar_status()

    # Gera movimento na Tesouraria
    if instance.confirmado and not instance.movimento_gerado:
        instance.registrar_movimento_pagamento()