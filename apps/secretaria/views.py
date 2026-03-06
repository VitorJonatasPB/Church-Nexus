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
