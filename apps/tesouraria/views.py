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
