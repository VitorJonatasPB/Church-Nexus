from django.urls import path
from . import views

app_name = 'tesouraria'

urlpatterns = [
    # Contas
    path('contas/', views.ContaListView.as_view(), name='conta-list'),
    path('contas/nova/', views.ContaCreateView.as_view(), name='conta-create'),
    path('contas/<int:pk>/editar/', views.ContaUpdateView.as_view(), name='conta-update'),
    path('contas/<int:pk>/deletar/', views.ContaDeleteView.as_view(), name='conta-delete'),

    # Categorias
    path('categorias/', views.CategoriaListView.as_view(), name='categoria-list'),
    path('categorias/nova/', views.CategoriaCreateView.as_view(), name='categoria-create'),
    path('categorias/<int:pk>/editar/', views.CategoriaUpdateView.as_view(), name='categoria-update'),
    path('categorias/<int:pk>/deletar/', views.CategoriaDeleteView.as_view(), name='categoria-delete'),

    # Movimentos
    path('movimentos/', views.MovimentoListView.as_view(), name='movimento-list'),
    path('movimentos/novo/', views.MovimentoCreateView.as_view(), name='movimento-create'),
    path('movimentos/<int:pk>/editar/', views.MovimentoUpdateView.as_view(), name='movimento-update'),
    path('movimentos/<int:pk>/deletar/', views.MovimentoDeleteView.as_view(), name='movimento-delete'),

    # Exports
    path('movimentos/exportar/csv/', views.exportar_movimentos_csv_view, name='export-movimentos-csv'),
    path('movimentos/exportar/pdf/', views.exportar_movimentos_pdf_view, name='export-movimentos-pdf'),
    path('contas/<int:pk>/exportar_csv/', views.exportar_extrato_conta_csv_view, name='export-extrato-conta-csv'),
    path('contas/<int:pk>/exportar_pdf/', views.exportar_extrato_conta_pdf_view, name='export-extrato-conta-pdf'),
    path('contas/exportar/csv/', views.exportar_contas_csv_view, name='export-contas-csv'),
    path('contas/exportar/pdf/', views.exportar_contas_pdf_view, name='export-contas-pdf'),
    path('categorias/exportar/csv/', views.exportar_categorias_csv_view, name='export-categorias-csv'),
    path('categorias/exportar/pdf/', views.exportar_categorias_pdf_view, name='export-categorias-pdf'),
]