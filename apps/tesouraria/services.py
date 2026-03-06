from django.db.models import Sum
from .models import Movimento


def total_entradas_mes(mes, ano):
    return Movimento.objects.filter(
        tipo='E',
        data__month=mes,
        data__year=ano
    ).aggregate(total=Sum('valor'))['total'] or 0


def total_saidas_mes(mes, ano):
    return Movimento.objects.filter(
        tipo='S',
        data__month=mes,
        data__year=ano
    ).aggregate(total=Sum('valor'))['total'] or 0
