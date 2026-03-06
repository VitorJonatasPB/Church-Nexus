from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.db.models.functions import ExtractYear
from django.shortcuts import render
from django.utils import timezone

from apps.secretaria.models import Area, Congregacao, Membro


OBREIRO_CARGOS = ['Diácono(a)', 'Missionário(a)', 'Presbítero', 'Evangelista', 'Pastor(a)']


@login_required
def dashboard(request):
    ano_atual = timezone.now().year

    congregacoes_por_ano = {
        item['ano']: item['total']
        for item in Congregacao.objects.annotate(ano=ExtractYear('data_cadastro'))
        .values('ano')
        .annotate(total=Count('id'))
    }

    membros_por_ano = {
        item['ano']: item
        for item in Membro.objects.annotate(ano=ExtractYear('data_cadastro'))
        .values('ano')
        .annotate(
            membros=Count('id'),
            congregados=Count('id', filter=Q(cargo='Congregado')),
            obreiros=Count('id', filter=Q(cargo__in=OBREIRO_CARGOS)),
        )
    }

    anos_disponiveis = sorted(set(congregacoes_por_ano) | set(membros_por_ano))
    if not anos_disponiveis:
        anos_disponiveis = [ano_atual]

    comparativo_anual = []
    for ano in anos_disponiveis:
        metricas_membros = membros_por_ano.get(ano, {})
        comparativo_anual.append(
            {
                'ano': ano,
                'congregacoes': congregacoes_por_ano.get(ano, 0),
                'obreiros': metricas_membros.get('obreiros', 0),
                'membros': metricas_membros.get('membros', 0),
                'congregados': metricas_membros.get('congregados', 0),
            }
        )

    comparativo_departamentos = []
    departamentos = Area.objects.annotate(
        congregacoes_total=Count('congregacao', distinct=True),
        membros_total=Count('membros', distinct=True),
        congregados_total=Count('membros', filter=Q(membros__cargo='Congregado'), distinct=True),
        obreiros_total=Count('membros', filter=Q(membros__cargo__in=OBREIRO_CARGOS), distinct=True),
    )

    for area in departamentos:
        anos_area = defaultdict(lambda: {'congregacoes': 0, 'membros': 0, 'congregados': 0, 'obreiros': 0})

        for item in (
            Congregacao.objects.filter(area=area)
            .annotate(ano=ExtractYear('data_cadastro'))
            .values('ano')
            .annotate(total=Count('id'))
        ):
            anos_area[item['ano']]['congregacoes'] = item['total']

        for item in (
            Membro.objects.filter(area=area)
            .annotate(ano=ExtractYear('data_cadastro'))
            .values('ano')
            .annotate(
                membros=Count('id'),
                congregados=Count('id', filter=Q(cargo='Congregado')),
                obreiros=Count('id', filter=Q(cargo__in=OBREIRO_CARGOS)),
            )
        ):
            anos_area[item['ano']]['membros'] = item['membros']
            anos_area[item['ano']]['congregados'] = item['congregados']
            anos_area[item['ano']]['obreiros'] = item['obreiros']

        comparativo_departamentos.append(
            {
                'nome': area.nome,
                'totais': {
                    'congregacoes': area.congregacoes_total,
                    'obreiros': area.obreiros_total,
                    'membros': area.membros_total,
                    'congregados': area.congregados_total,
                },
                'anos': [
                    {
                        'ano': ano,
                        **metricas,
                    }
                    for ano, metricas in sorted(anos_area.items())
                ],
            }
        )

    contexto = {
        'comparativo_anual': comparativo_anual,
        'comparativo_departamentos': comparativo_departamentos,
        'totais_gerais': {
            'congregacoes': Congregacao.objects.count(),
            'obreiros': Membro.objects.filter(cargo__in=OBREIRO_CARGOS).count(),
            'membros': Membro.objects.count(),
            'congregados': Membro.objects.filter(cargo='Congregado').count(),
        },
    }
    return render(request, 'core/dashboard.html', contexto)
