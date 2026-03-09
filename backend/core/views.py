from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from dateutil.relativedelta import relativedelta

from apps.secretaria.models import Area, Congregacao, Membro

OBREIRO_CARGOS = ['Pastor', 'Pastora', 'Pastor(a)', 'Evangelista', 'Presbítero', 'Missionário', 'Missionária', 'Missionário(a)', 'Diácono', 'Diaconisa']
MEMBRO_COMUM_CARGOS = ['Membro', 'Congregado']
MEMBRESIA_CARGOS = OBREIRO_CARGOS + MEMBRO_COMUM_CARGOS


@login_required
def dashboard(request):
    # Total Membresia = Membros + Obreiros
    total_membros_comuns = Membro.objects.filter(cargo__in=MEMBRO_COMUM_CARGOS).count()
    total_obreiros = Membro.objects.filter(cargo__in=OBREIRO_CARGOS).count()
    total_geral = Membro.objects.filter(cargo__in=MEMBRESIA_CARGOS).count()
    
    # Crescimento
    now = timezone.now()
    first_day_this_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    total_anterior = Membro.objects.filter(data_cadastro__lt=first_day_this_month, cargo__in=MEMBRESIA_CARGOS).count()
    total_atual = total_geral
    
    if total_anterior > 0:
        crescimento_pct = ((total_atual - total_anterior) / total_anterior) * 100.0
    else:
        crescimento_pct = 100.0 if total_atual > 0 else 0.0
        
    crescimento_pct = round(crescimento_pct, 1)
    
    # Data for Charts
    # We need historical growth (e.g. last 6 months)
    meses = []
    crescimento_geral = []
    crescimento_membresia = []
    for i in range(5, -1, -1):
        m_date = first_day_this_month - relativedelta(months=i)
        next_m = m_date + relativedelta(months=1)
        meses.append(m_date.strftime('%b/%Y'))
        crescimento_geral.append(Congregacao.objects.filter(data_cadastro__lt=next_m).count())
        crescimento_membresia.append(Membro.objects.filter(data_cadastro__lt=next_m, cargo__in=MEMBRO_COMUM_CARGOS).count())
        
    # Dados para filtrar por Área nos gráficos
    chart_data_by_area = {}
    for a in Area.objects.all():
        hist_geral_area = []
        hist_memb_area = []
        for i in range(5, -1, -1):
            m_date = first_day_this_month - relativedelta(months=i)
            next_m = m_date + relativedelta(months=1)
            hist_geral_area.append(Congregacao.objects.filter(data_cadastro__lt=next_m, area=a).count())
            hist_memb_area.append(Membro.objects.filter(data_cadastro__lt=next_m, cargo__in=MEMBRO_COMUM_CARGOS, area=a).count())
        
        chart_data_by_area[str(a.id)] = {
            'geral': hist_geral_area,
            'membresia': hist_memb_area
        }
        
    import json
    chart_data_by_area_json = json.dumps(chart_data_by_area)
    
    # Comparativo por Area
    areas_data = []
    for a in Area.objects.all():
        membros_area_count = Membro.objects.filter(area=a, cargo__in=MEMBRESIA_CARGOS).count()
        cong_area_count = Congregacao.objects.filter(area=a).count()
        
        # crescimento_area 
        ant_a = Membro.objects.filter(area=a, data_cadastro__lt=first_day_this_month, cargo__in=MEMBRESIA_CARGOS).count()
        if ant_a > 0:
            cresc_a = ((membros_area_count - ant_a) / ant_a) * 100
        else:
            cresc_a = 100 if membros_area_count > 0 else 0
            
        areas_data.append({
            'obj': a,
            'membros': membros_area_count,
            'congregacoes': cong_area_count,
            'crescimento': round(cresc_a, 1)
        })

    contexto = {
        'total_areas': Area.objects.count(),
        'total_congregacoes': Congregacao.objects.count(),
        'total_membros_comuns': total_membros_comuns,
        'total_obreiros': total_obreiros,
        'total_geral': total_geral,
        'crescimento_pct': crescimento_pct,
        'chart_labels': meses,
        'chart_data_geral': crescimento_geral,
        'chart_data_membresia': crescimento_membresia,
        'chart_data_by_area_json': chart_data_by_area_json,
        'areas_comparativo': areas_data,
    }
    return render(request, 'core/dashboard.html', contexto)
