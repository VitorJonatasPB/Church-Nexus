import csv
from django.http import HttpResponse

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
except ModuleNotFoundError:
    class _MissingReportLab:
        def __getattr__(self, _):
            raise ModuleNotFoundError('A dependência reportlab não está instalada.')

    def _missing_reportlab(*args, **kwargs):
        raise ModuleNotFoundError('A dependência reportlab não está instalada.')

    A4 = None
    colors = _MissingReportLab()
    SimpleDocTemplate = Table = TableStyle = Paragraph = Spacer = _missing_reportlab

    def getSampleStyleSheet():
        raise ModuleNotFoundError('A dependência reportlab não está instalada.')

def exportar_evento_csv(evento):
    participantes = evento.participantes.all().order_by('nome')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="evento_{evento.id}_participantes.csv"'
    
    # Using ; as delimiter for Brazilian Excel
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['Nome', 'E-mail', 'Telefone', 'Status', 'Total Pago', 'Valor Necessário'])
    
    for p in participantes:
        status = 'Ativo' if p.ativo else 'Inativo'
        writer.writerow([
            p.nome, 
            p.email or '', 
            p.telefone or '', 
            status, 
            f"{p.total_pago:.2f}".replace('.', ','),
            f"{p.valor_necessario:.2f}".replace('.', ',')
        ])
        
    return response

def exportar_evento_pdf(evento):
    participantes = evento.participantes.all().order_by('nome')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="evento_{evento.id}_participantes.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # Titulo
    elements.append(Paragraph(f"Relatório do Evento: {evento.nome}", styles['Title']))
    elements.append(Spacer(1, 12))
    
    # Tabela de Participantes
    data = [['Nome', 'Status', 'Total Pago', 'Valor Rel.']]
    
    for p in participantes:
        status = 'Ativo' if p.ativo else 'Inativo'
        data.append([
            Paragraph(p.nome, styles['Normal']),
            status,
            f"R$ {p.total_pago:.2f}".replace('.', ','),
            f"R$ {p.valor_necessario:.2f}".replace('.', ',')
        ])
        
    t = Table(data, colWidths=[200, 80, 100, 100])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    
    elements.append(t)
    doc.build(elements)
    
    return response

from django.db.models import Sum

def exportar_eventos_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="eventos_export.csv"'
    
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['ID', 'Nome', 'Data Início', 'Data Fim', 'Valor Necessário', 'Total Arrecadado'])
    
    for evento in queryset:
        total_arrecadado = evento.pagamentos.aggregate(total=Sum('valor_pago'))['total'] or 0
        writer.writerow([
            evento.id,
            evento.nome,
            evento.data_inicio.strftime('%d/%m/%Y'),
            evento.data_fim.strftime('%d/%m/%Y'),
            f"{evento.valor_necessario:.2f}".replace('.', ','),
            f"{total_arrecadado:.2f}".replace('.', ',')
        ])
        
    return response

def exportar_eventos_pdf(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="eventos_export.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # Titulo
    elements.append(Paragraph("Relatório de Eventos", styles['Title']))
    elements.append(Spacer(1, 12))
    
    # Tabela de Eventos
    data = [['ID', 'Nome', 'Data Início', 'Total Arrecadado']]
    
    for evento in queryset:
        total_arrecadado = evento.pagamentos.aggregate(total=Sum('valor_pago'))['total'] or 0
        data.append([
            str(evento.id),
            Paragraph(evento.nome, styles['Normal']),
            evento.data_inicio.strftime('%d/%m/%Y'),
            f"R$ {total_arrecadado:.2f}".replace('.', ',')
        ])
        
    t = Table(data, colWidths=[40, 200, 100, 100])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    
    elements.append(t)
    doc.build(elements)
    
    return response

exportar_eventos_csv.short_description = "Exportar Eventos (CSV)"
exportar_eventos_pdf.short_description = "Exportar Eventos (PDF)"

def exportar_participantes_csv(request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="participantes_export.csv"'
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['ID', 'Nome', 'Email', 'Telefone', 'Evento', 'Valor Necessário', 'Total Pago', 'Status'])
    for p in queryset:
        writer.writerow([
            p.id, p.nome, p.email, p.telefone, 
            p.evento.nome if p.evento else '',
            f"{p.valor_necessario:.2f}".replace('.', ','),
            f"{p.total_pago:.2f}".replace('.', ','),
            'Ativo' if p.ativo else 'Inativo'
        ])
    return response

def exportar_participantes_pdf(request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="participantes_export.pdf"'
    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    elements.append(Paragraph("Relatório de Participantes", styles['Title']))
    elements.append(Spacer(1, 12))
    data = [['Nome', 'Evento', 'Total Pago', 'Status']]
    for p in queryset:
        data.append([
            Paragraph(p.nome, styles['Normal']),
            Paragraph(p.evento.nome if p.evento else '', styles['Normal']),
            f"R$ {p.total_pago:.2f}".replace('.', ','),
            'Ativo' if p.ativo else 'Inativo'
        ])
    t = Table(data, colWidths=[150, 150, 100, 80])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(t)
    doc.build(elements)
    return response

def exportar_pagamentos_csv(request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pagamentos_export.csv"'
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['ID', 'Participante', 'Evento', 'Valor', 'Forma Pagamento', 'Data'])
    for pg in queryset:
        writer.writerow([
            pg.id, 
            pg.participante.nome if pg.participante else '',
            pg.evento.nome if pg.evento else '',
            f"{pg.valor_pago:.2f}".replace('.', ','),
            pg.get_forma_pagamento_display(),
            pg.data_pagamento.strftime('%d/%m/%Y %H:%M')
        ])
    return response

def exportar_pagamentos_pdf(request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="pagamentos_export.pdf"'
    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    elements.append(Paragraph("Relatório de Pagamentos", styles['Title']))
    elements.append(Spacer(1, 12))
    data = [['Participante', 'Evento', 'Valor', 'Data']]
    for pg in queryset:
        data.append([
            Paragraph(pg.participante.nome if pg.participante else '', styles['Normal']),
            Paragraph(pg.evento.nome if pg.evento else '', styles['Normal']),
            f"R$ {pg.valor_pago:.2f}".replace('.', ','),
            pg.data_pagamento.strftime('%d/%m/%Y %H:%M')
        ])
    t = Table(data, colWidths=[150, 150, 80, 100])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(t)
    doc.build(elements)
    return response
