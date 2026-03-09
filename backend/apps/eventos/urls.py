from django.urls import path
from . import views

app_name = 'eventos'

urlpatterns = [
    # Eventos
    path('lista/', views.EventoListView.as_view(), name='evento-list'),
    path('novo/', views.EventoCreateView.as_view(), name='evento-create'),
    path('<int:pk>/editar/', views.EventoUpdateView.as_view(), name='evento-update'),
    path('<int:pk>/deletar/', views.EventoDeleteView.as_view(), name='evento-delete'),
    path('exportar/csv/', views.exportar_eventos_csv_view, name='export-eventos-csv'),
    path('exportar/pdf/', views.exportar_eventos_pdf_view, name='export-eventos-pdf'),
    path('<int:pk>/exportar_csv/', views.exportar_evento_participantes_csv_view, name='export-evento-participantes-csv'),
    path('<int:pk>/exportar_pdf/', views.exportar_evento_participantes_pdf_view, name='export-evento-participantes-pdf'),

    # Participantes
    path('participantes/', views.ParticipanteListView.as_view(), name='participante-list'),
    path('participantes/novo/', views.ParticipanteCreateView.as_view(), name='participante-create'),
    path('participantes/<int:pk>/editar/', views.ParticipanteUpdateView.as_view(), name='participante-update'),
    path('participantes/<int:pk>/deletar/', views.ParticipanteDeleteView.as_view(), name='participante-delete'),

    # Pagamentos
    path('pagamentos/', views.PagamentoListView.as_view(), name='pagamento-list'),
    path('pagamentos/novo/', views.PagamentoCreateView.as_view(), name='pagamento-create'),
    path('pagamentos/<int:pk>/editar/', views.PagamentoUpdateView.as_view(), name='pagamento-update'),
    path('pagamentos/<int:pk>/deletar/', views.PagamentoDeleteView.as_view(), name='pagamento-delete'),

    # Autocompletes & Helpers
    path('admin/participantes_por_evento/<int:evento_id>/', views.participantes_por_evento),
    path('participante-autocomplete/', views.ParticipanteAutocomplete.as_view(), name='participante-autocomplete'),

    # Exports Globais
    path('participantes/exportar/csv/', views.exportar_participantes_csv_view, name='export-participantes-csv'),
    path('participantes/exportar/pdf/', views.exportar_participantes_pdf_view, name='export-participantes-pdf'),
    path('pagamentos/exportar/csv/', views.exportar_pagamentos_csv_view, name='export-pagamentos-csv'),
    path('pagamentos/exportar/pdf/', views.exportar_pagamentos_pdf_view, name='export-pagamentos-pdf'),
]
