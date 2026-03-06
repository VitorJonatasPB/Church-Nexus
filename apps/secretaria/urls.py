from django.urls import path
from .views import CongregacaoAutocomplete
from .views import (
    AreaCreateView, AreaDeleteView, AreaListView, AreaUpdateView,
    MembroListView, MembroCreateView, MembroUpdateView, MembroDeleteView,
    CongregacaoListView, CongregacaoCreateView, CongregacaoUpdateView, CongregacaoDeleteView
)
from . import views

app_name = 'secretaria'

urlpatterns = [
    # Membros CRUD
    path('membros/', MembroListView.as_view(), name='membro-list'),
    path('membros/novo/', MembroCreateView.as_view(), name='membro-create'),
    path('membros/<int:pk>/editar/', MembroUpdateView.as_view(), name='membro-update'),
    path('membros/<int:pk>/deletar/', MembroDeleteView.as_view(), name='membro-delete'),

    # Áreas CRUD
    path('areas/', AreaListView.as_view(), name='area-list'),
    path('areas/nova/', AreaCreateView.as_view(), name='area-create'),
    path('areas/<int:pk>/editar/', AreaUpdateView.as_view(), name='area-update'),
    path('areas/<int:pk>/deletar/', AreaDeleteView.as_view(), name='area-delete'),

    # Congregações CRUD
    path('congregacoes/', CongregacaoListView.as_view(), name='congregacao-list'),
    path('congregacoes/nova/', CongregacaoCreateView.as_view(), name='congregacao-create'),
    path('congregacoes/<int:pk>/editar/', CongregacaoUpdateView.as_view(), name='congregacao-update'),
    path('congregacoes/<int:pk>/deletar/', CongregacaoDeleteView.as_view(), name='congregacao-delete'),

    path('congregacao-autocomplete/', CongregacaoAutocomplete.as_view(), name='congregacao-autocomplete'),

    # Exports
    path('exportar/membros/csv/', views.exportar_membros_csv_view, name='export-membros-csv'),
    path('exportar/membros/pdf/', views.exportar_membros_pdf_view, name='export-membros-pdf'),
    path('exportar/congregacoes/csv/', views.exportar_congregacoes_csv_view, name='export-congregacoes-csv'),
    path('exportar/congregacoes/pdf/', views.exportar_congregacoes_pdf_view, name='export-congregacoes-pdf'),
    path('exportar/areas/csv/', views.exportar_areas_csv_view, name='export-areas-csv'),
    path('exportar/areas/pdf/', views.exportar_areas_pdf_view, name='export-areas-pdf'),
]
