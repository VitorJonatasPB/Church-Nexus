from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from dal import autocomplete

from apps.eventos.models import Evento, Participante, Pagamento
from .forms import EventoForm, ParticipanteForm, PagamentoForm

# ==================== EVENTOS ====================
class EventoListView(LoginRequiredMixin, ListView):
    model = Evento
    template_name = 'eventos/evento_list.html'
    context_object_name = 'eventos'
    ordering = ['-data_inicio']

class EventoCreateView(LoginRequiredMixin, CreateView):
    model = Evento
    form_class = EventoForm
    template_name = 'eventos/evento_form.html'
    success_url = reverse_lazy('eventos:evento-list')

class EventoUpdateView(LoginRequiredMixin, UpdateView):
    model = Evento
    form_class = EventoForm
    template_name = 'eventos/evento_form.html'
    success_url = reverse_lazy('eventos:evento-list')

class EventoDeleteView(LoginRequiredMixin, DeleteView):
    model = Evento
    template_name = 'eventos/evento_confirm_delete.html'
    success_url = reverse_lazy('eventos:evento-list')

# ==================== PARTICIPANTES ====================
class ParticipanteListView(LoginRequiredMixin, ListView):
    model = Participante
    template_name = 'eventos/participante_list.html'
    context_object_name = 'participantes'
    ordering = ['nome']

class ParticipanteCreateView(LoginRequiredMixin, CreateView):
    model = Participante
    form_class = ParticipanteForm
    template_name = 'eventos/participante_form.html'
    success_url = reverse_lazy('eventos:participante-list')

    # Pre-selecionar evento se passado na URL
    def get_initial(self):
        initial = super().get_initial()
        evento_id = self.request.GET.get('evento')
        if evento_id:
            initial['evento'] = evento_id
        return initial

class ParticipanteUpdateView(LoginRequiredMixin, UpdateView):
    model = Participante
    form_class = ParticipanteForm
    template_name = 'eventos/participante_form.html'
    success_url = reverse_lazy('eventos:participante-list')

class ParticipanteDeleteView(LoginRequiredMixin, DeleteView):
    model = Participante
    template_name = 'eventos/participante_confirm_delete.html'
    success_url = reverse_lazy('eventos:participante-list')

# ==================== PAGAMENTOS ====================
class PagamentoListView(LoginRequiredMixin, ListView):
    model = Pagamento
    template_name = 'eventos/pagamento_list.html'
    context_object_name = 'pagamentos'
    ordering = ['-data_pagamento']

class PagamentoCreateView(LoginRequiredMixin, CreateView):
    model = Pagamento
    form_class = PagamentoForm
    template_name = 'eventos/pagamento_form.html'
    success_url = reverse_lazy('eventos:pagamento-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        try:
            if self.object.participante:
                self.object.participante.atualizar_status()
            self.object.registrar_movimento_pagamento()
        except Exception as e:
            # Em caso de erro, ao menos loggar ou mostrar algo (ideal com messages framework)
            pass
        return response

class PagamentoUpdateView(LoginRequiredMixin, UpdateView):
    model = Pagamento
    form_class = PagamentoForm
    template_name = 'eventos/pagamento_form.html'
    success_url = reverse_lazy('eventos:pagamento-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        try:
            if self.object.participante:
                self.object.participante.atualizar_status()
            self.object.registrar_movimento_pagamento()
        except Exception as e:
            pass
        return response

class PagamentoDeleteView(LoginRequiredMixin, DeleteView):
    model = Pagamento
    template_name = 'eventos/pagamento_confirm_delete.html'
    success_url = reverse_lazy('eventos:pagamento-list')

# ==================== HELPERS ====================
def participantes_por_evento(request, evento_id):
    participantes = Participante.objects.filter(evento__id=evento_id)
    data = [{'id': p.id, 'nome': p.nome} for p in participantes]
    return JsonResponse(data, safe=False)

class ParticipanteAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Participante.objects.all()
        evento_id = self.forwarded.get('evento', None)
        if evento_id:
            qs = qs.filter(evento_id=evento_id)
        if self.q:
            qs = qs.filter(nome__icontains=self.q)
        return qs

# ==================== EXPORTS ====================
from django.shortcuts import get_object_or_404
from .exports import (
    exportar_eventos_csv, exportar_eventos_pdf, 
    exportar_evento_csv, exportar_evento_pdf,
    exportar_participantes_csv, exportar_participantes_pdf,
    exportar_pagamentos_csv, exportar_pagamentos_pdf
)

def exportar_eventos_csv_view(request):
    return exportar_eventos_csv(None, request, Evento.objects.all())

def exportar_eventos_pdf_view(request):
    return exportar_eventos_pdf(None, request, Evento.objects.all())

def exportar_evento_participantes_csv_view(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    return exportar_evento_csv(evento)

def exportar_evento_participantes_pdf_view(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    return exportar_evento_pdf(evento)

def exportar_participantes_csv_view(request):
    return exportar_participantes_csv(request, Participante.objects.all())

def exportar_participantes_pdf_view(request):
    return exportar_participantes_pdf(request, Participante.objects.all())

def exportar_pagamentos_csv_view(request):
    return exportar_pagamentos_csv(request, Pagamento.objects.all())

def exportar_pagamentos_pdf_view(request):
    return exportar_pagamentos_pdf(request, Pagamento.objects.all())