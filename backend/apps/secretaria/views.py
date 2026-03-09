from django.urls import reverse_lazy
from dal import autocomplete
from .models import Area, Congregacao, Membro
from .forms import MembroForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

class MembroListView(LoginRequiredMixin, ListView):
    model = Membro
    template_name = 'secretaria/membro_list.html'
    context_object_name = 'membros'
    ordering = ['nome']
    
    def get_queryset(self):
        qs = super().get_queryset()
        # Aqui no futuro poderemos injetar os filtros de tela
        return qs

class MembroCreateView(LoginRequiredMixin, CreateView):
    model = Membro
    form_class = MembroForm
    template_name = 'secretaria/membro_form.html'
    success_url = reverse_lazy('secretaria:membro-list')

class MembroUpdateView(LoginRequiredMixin, UpdateView):
    model = Membro
    form_class = MembroForm
    template_name = 'secretaria/membro_form.html'
    success_url = reverse_lazy('secretaria:membro-list')

class MembroDeleteView(LoginRequiredMixin, DeleteView):
    model = Membro
    template_name = 'secretaria/membro_confirm_delete.html'
    success_url = reverse_lazy('secretaria:membro-list')

class AreaListView(LoginRequiredMixin, ListView):
    model = Area
    template_name = 'secretaria/area_list.html'
    context_object_name = 'areas'

class AreaCreateView(LoginRequiredMixin, CreateView):
    model = Area
    fields = ['nome']
    template_name = 'secretaria/area_form.html'
    success_url = reverse_lazy('secretaria:area-list')

class AreaUpdateView(LoginRequiredMixin, UpdateView):
    model = Area
    fields = ['nome']
    template_name = 'secretaria/area_form.html'
    success_url = reverse_lazy('secretaria:area-list')

class AreaDeleteView(LoginRequiredMixin, DeleteView):
    model = Area
    template_name = 'secretaria/area_confirm_delete.html'
    success_url = reverse_lazy('secretaria:area-list')


from .forms import CongregacaoForm

class CongregacaoListView(LoginRequiredMixin, ListView):
    model = Congregacao
    template_name = 'secretaria/congregacao_list.html'
    context_object_name = 'congregacoes'

class CongregacaoCreateView(LoginRequiredMixin, CreateView):
    model = Congregacao
    form_class = CongregacaoForm
    template_name = 'secretaria/congregacao_form.html'
    success_url = reverse_lazy('secretaria:congregacao-list')

class CongregacaoUpdateView(LoginRequiredMixin, UpdateView):
    model = Congregacao
    form_class = CongregacaoForm
    template_name = 'secretaria/congregacao_form.html'
    success_url = reverse_lazy('secretaria:congregacao-list')

class CongregacaoDeleteView(LoginRequiredMixin, DeleteView):
    model = Congregacao
    template_name = 'secretaria/congregacao_confirm_delete.html'
    success_url = reverse_lazy('secretaria:congregacao-list')

class CongregacaoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Congregacao.objects.all()

        area_id = self.forwarded.get('area', None)
        if area_id:
            qs = qs.filter(area_id=area_id)

        if self.q:
            qs = qs.filter(nome__icontains=self.q)
        return qs

# ==================== EXPORTS ====================
from .exports import (
    exportar_membros_csv, exportar_membros_pdf,
    exportar_congregacoes_csv, exportar_congregacoes_pdf,
    exportar_areas_csv, exportar_areas_pdf
)

def exportar_membros_csv_view(request):
    return exportar_membros_csv(request, Membro.objects.all())

def exportar_membros_pdf_view(request):
    return exportar_membros_pdf(request, Membro.objects.all())

def exportar_congregacoes_csv_view(request):
    return exportar_congregacoes_csv(request, Congregacao.objects.all())

def exportar_congregacoes_pdf_view(request):
    return exportar_congregacoes_pdf(request, Congregacao.objects.all())

def exportar_areas_csv_view(request):
    return exportar_areas_csv(request, Area.objects.all())

def exportar_areas_pdf_view(request):
    return exportar_areas_pdf(request, Area.objects.all())

from django.views.generic import TemplateView
from django.utils import timezone
from dateutil.relativedelta import relativedelta

class AnaliseSecretariaView(LoginRequiredMixin, TemplateView):
    template_name = 'secretaria/analise.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # KPIs
        context['total_areas'] = Area.objects.count()
        context['total_congregacoes'] = Congregacao.objects.count()
        
        # Definições de Cargos
        cargos_obreiros = ['Pastor', 'Pastora', 'Pastor(a)', 'Evangelista', 'Presbítero', 'Missionário', 'Missionária', 'Missionário(a)', 'Diácono', 'Diaconisa']
        cargos_membros_comuns = ['Membro', 'Congregado']
        cargos_membresia = cargos_obreiros + cargos_membros_comuns

        # Total Membresia = Membros + Obreiros
        context['total_membros_comuns'] = Membro.objects.filter(cargo__in=cargos_membros_comuns).count()
        context['total_obreiros'] = Membro.objects.filter(cargo__in=cargos_obreiros).count()
        context['total_geral'] = Membro.objects.filter(cargo__in=cargos_membresia).count()
        
        # Crescimento
        now = timezone.now()
        first_day_this_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        total_anterior = Membro.objects.filter(data_cadastro__lt=first_day_this_month, cargo__in=cargos_membresia).count()
        total_atual = context['total_geral']
        
        if total_anterior > 0:
            crescimento_pct = ((total_atual - total_anterior) / total_anterior) * 100.0
        else:
            crescimento_pct = 100.0 if total_atual > 0 else 0.0
            
        context['crescimento_pct'] = round(crescimento_pct, 1)
        
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
            crescimento_membresia.append(Membro.objects.filter(data_cadastro__lt=next_m, cargo__in=cargos_membros_comuns).count())
            
        context['chart_labels'] = meses
        context['chart_data_geral'] = crescimento_geral
        context['chart_data_membresia'] = crescimento_membresia
        
        # Dados para filtrar por Área nos gráficos
        chart_data_by_area = {}
        for a in Area.objects.all():
            hist_geral_area = []
            hist_memb_area = []
            for i in range(5, -1, -1):
                m_date = first_day_this_month - relativedelta(months=i)
                next_m = m_date + relativedelta(months=1)
                hist_geral_area.append(Congregacao.objects.filter(data_cadastro__lt=next_m, area=a).count())
                hist_memb_area.append(Membro.objects.filter(data_cadastro__lt=next_m, cargo__in=cargos_membros_comuns, area=a).count())
            chart_data_by_area[str(a.id)] = {
                'geral': hist_geral_area,
                'membresia': hist_memb_area
            }
            
        import json
        context['chart_data_by_area_json'] = json.dumps(chart_data_by_area)
        
        # Comparativo por Area
        areas_data = []
        for a in Area.objects.all():
            membros_area_count = Membro.objects.filter(area=a, cargo__in=cargos_membresia).count()
            cong_area_count = Congregacao.objects.filter(area=a).count()
            
            # crescimento_area 
            ant_a = Membro.objects.filter(area=a, data_cadastro__lt=first_day_this_month, cargo__in=cargos_membresia).count()
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
            
        context['areas_comparativo'] = areas_data
        
        # Comparativo por Congregação
        congregacoes_data = []
        for c in Congregacao.objects.all():
            congregacoes_data.append({
                'obj': c,
            })
        context['congregacoes_comparativo'] = congregacoes_data
        
        return context
