from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Conta, Categoria, Movimento
from .forms import ContaForm, CategoriaForm, MovimentoForm

# ==================== CONTAS ====================
class ContaListView(LoginRequiredMixin, ListView):
    model = Conta
    template_name = 'tesouraria/conta_list.html'
    context_object_name = 'contas'

class ContaCreateView(LoginRequiredMixin, CreateView):
    model = Conta
    form_class = ContaForm
    template_name = 'tesouraria/conta_form.html'
    success_url = reverse_lazy('tesouraria:conta-list')

class ContaUpdateView(LoginRequiredMixin, UpdateView):
    model = Conta
    form_class = ContaForm
    template_name = 'tesouraria/conta_form.html'
    success_url = reverse_lazy('tesouraria:conta-list')

class ContaDeleteView(LoginRequiredMixin, DeleteView):
    model = Conta
    template_name = 'tesouraria/conta_confirm_delete.html'
    success_url = reverse_lazy('tesouraria:conta-list')

# ==================== CATEGORIAS ====================
class CategoriaListView(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = 'tesouraria/categoria_list.html'
    context_object_name = 'categorias'

class CategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'tesouraria/categoria_form.html'
    success_url = reverse_lazy('tesouraria:categoria-list')

class CategoriaUpdateView(LoginRequiredMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'tesouraria/categoria_form.html'
    success_url = reverse_lazy('tesouraria:categoria-list')

class CategoriaDeleteView(LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'tesouraria/categoria_confirm_delete.html'
    success_url = reverse_lazy('tesouraria:categoria-list')

# ==================== MOVIMENTOS ====================
class MovimentoListView(LoginRequiredMixin, ListView):
    model = Movimento
    template_name = 'tesouraria/movimento_list.html'
    context_object_name = 'movimentos'

class MovimentoCreateView(LoginRequiredMixin, CreateView):
    model = Movimento
    form_class = MovimentoForm
    template_name = 'tesouraria/movimento_form.html'
    success_url = reverse_lazy('tesouraria:movimento-list')

class MovimentoUpdateView(LoginRequiredMixin, UpdateView):
    model = Movimento
    form_class = MovimentoForm
    template_name = 'tesouraria/movimento_form.html'
    success_url = reverse_lazy('tesouraria:movimento-list')

class MovimentoDeleteView(LoginRequiredMixin, DeleteView):
    model = Movimento
    template_name = 'tesouraria/movimento_confirm_delete.html'
    success_url = reverse_lazy('tesouraria:movimento-list')
# ==================== EXPORTS ====================
from django.shortcuts import get_object_or_404
from .exports import (
    exportar_movimentos_csv, exportar_movimentos_pdf, 
    exportar_extrato_conta_csv, exportar_extrato_conta_pdf,
    exportar_contas_csv, exportar_contas_pdf,
    exportar_categorias_csv, exportar_categorias_pdf
)

def exportar_movimentos_csv_view(request):
    return exportar_movimentos_csv(None, request, Movimento.objects.all())

def exportar_movimentos_pdf_view(request):
    return exportar_movimentos_pdf(None, request, Movimento.objects.all())

def exportar_extrato_conta_csv_view(request, pk):
    conta = get_object_or_404(Conta, pk=pk)
    return exportar_extrato_conta_csv(conta)

def exportar_extrato_conta_pdf_view(request, pk):
    conta = get_object_or_404(Conta, pk=pk)
    return exportar_extrato_conta_pdf(conta)

def exportar_contas_csv_view(request):
    return exportar_contas_csv(request, Conta.objects.all())

def exportar_contas_pdf_view(request):
    return exportar_contas_pdf(request, Conta.objects.all())

def exportar_categorias_csv_view(request):
    return exportar_categorias_csv(request, Categoria.objects.all())

def exportar_categorias_pdf_view(request):
    return exportar_categorias_pdf(request, Categoria.objects.all())

from django.views.generic import TemplateView
from django.db.models import Sum, Q
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import json

class AnaliseTesourariaView(LoginRequiredMixin, TemplateView):
    template_name = 'tesouraria/analise.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        first_day_this_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Saldo Total (soma de saldos_iniciais + todas as entradas - todas as saídas)
        # Mais simples: iterar pelas contas e somar `conta.saldo_atual` se for property, ou calcular.
        # Vamos assumir que Conta tem prop saldo_atual (vou checar, se não faço query do Movimento)
        todas_contas = Conta.objects.all()
        saldo_total = sum([c.saldo for c in todas_contas])
        context['saldo_total'] = saldo_total
        
        # Receitas e Despesas do mês atual
        movimentos_mes = Movimento.objects.filter(data__gte=first_day_this_month)
        entradas_mes = movimentos_mes.filter(tipo='E').aggregate(total=Sum('valor'))['total'] or 0
        saidas_mes = movimentos_mes.filter(tipo='S').aggregate(total=Sum('valor'))['total'] or 0
        
        context['entradas_mes'] = entradas_mes
        context['saidas_mes'] = saidas_mes
        context['saldo_mes'] = entradas_mes - saidas_mes
        
        # Grafico 1: Fluxo de Caixa (Ultimos 6 meses)
        meses_labels = []
        entradas_hist = []
        saidas_hist = []
        
        for i in range(5, -1, -1):
            start_m = first_day_this_month - relativedelta(months=i)
            end_m = start_m + relativedelta(months=1)
            meses_labels.append(start_m.strftime('%b/%Y'))
            
            movs_m = Movimento.objects.filter(data__gte=start_m, data__lt=end_m)
            e_m = movs_m.filter(tipo='E').aggregate(total=Sum('valor'))['total'] or 0
            s_m = movs_m.filter(tipo='S').aggregate(total=Sum('valor'))['total'] or 0
            
            entradas_hist.append(float(e_m))
            saidas_hist.append(float(s_m))
            
        context['chart_financeiro_labels'] = meses_labels
        context['chart_financeiro_entradas'] = entradas_hist
        context['chart_financeiro_saidas'] = saidas_hist
        
        # Grafico 2: Despesas por Categoria (Todos os tempos ou do mês atual? do mês atual para ser util)
        categorias_labels = []
        categorias_valores = []
        
        # Agrupa saidas_meses por categoria
        despesas_por_cat = movimentos_mes.filter(tipo='S').values('categoria__nome').annotate(total=Sum('valor')).order_by('-total')
        
        for d in despesas_por_cat:
            cat_nome = d['categoria__nome'] if d['categoria__nome'] else 'Sem Categoria'
            categorias_labels.append(cat_nome)
            categorias_valores.append(float(d['total']))
            
        context['chart_categorias_labels'] = categorias_labels
        context['chart_categorias_valores'] = categorias_valores
        
        return context

