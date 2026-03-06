from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Movimento


@receiver(post_save, sender=Movimento)
def atualizar_saldo_ao_criar(sender, instance, created, **kwargs):
    if created:
        if instance.tipo == 'E':
            instance.conta.saldo += instance.valor
        else:
            instance.conta.saldo -= instance.valor
        instance.conta.save()


@receiver(post_delete, sender=Movimento)
def atualizar_saldo_ao_deletar(sender, instance, **kwargs):
    if instance.tipo == 'E':
        instance.conta.saldo -= instance.valor
    else:
        instance.conta.saldo += instance.valor
    instance.conta.save()
