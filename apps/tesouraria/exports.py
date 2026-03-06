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

def exportar_movimentos_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="movimentos_export.csv"'
    
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['ID', 'Tipo', 'Valor', 'Data', 'Conta', 'Categoria', 'Membro', 'Evento', 'Descrição'])
    
    for mov in queryset:
        tipo = 'Entrada' if mov.tipo == 'E' else 'Saída'
        membro = mov.membro.nome if mov.membro else (mov.nome_participante or '')
        evento = mov.evento.nome if mov.evento else ''
        
        writer.writerow([
            mov.id,
            tipo,
            f"{mov.valor:.2f}".replace('.', ','),
            mov.data.strftime('%d/%m/%Y'),
            mov.conta.nome if mov.conta else '',
            mov.categoria.nome if mov.categoria else '',
            membro,
            evento,
            mov.descricao
        ])
        
    return response

exportar_movimentos_csv.short_description = "Exportar Movimentos (CSV)"

def exportar_movimentos_pdf(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="movimentos_export.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    elements.append(Paragraph("Relatório de Movimentações", styles['Title']))
    elements.append(Spacer(1, 12))
    
    data = [['Data', 'Tipo', 'Valor', 'Conta', 'Categoria', 'Membro']]
    
    for mov in queryset:
        tipo = 'Entrada' if mov.tipo == 'E' else 'Saída'
        membro = mov.membro.nome if mov.membro else (mov.nome_participante or '')
        
        data.append([
            mov.data.strftime('%d/%m/%Y'),
            tipo,
            f"R$ {mov.valor:.2f}".replace('.', ','),
            Paragraph(mov.conta.nome if mov.conta else '', styles['Normal']),
            Paragraph(mov.categoria.nome if mov.categoria else '', styles['Normal']),
            Paragraph(membro, styles['Normal'])
        ])
        
    t = Table(data, colWidths=[60, 50, 60, 100, 100, 100])
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

exportar_movimentos_pdf.short_description = "Exportar Movimentos (PDF)"


def exportar_extrato_conta_csv(conta):
    movimentos = conta.movimentos.all().order_by('data', 'criado_em')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="extrato_conta_{conta.id}.csv"'
    
    writer = csv.writer(response, delimiter=';')
    writer.writerow([f'Extrato da Conta: {conta.nome}'])
    writer.writerow([f'Saldo Atual: R$ {conta.saldo:.2f}'.replace('.', ',')])
    writer.writerow([])
    writer.writerow(['Data', 'Tipo', 'Valor', 'Categoria', 'Descrição'])
    
    for mov in movimentos:
        tipo = 'Entrada' if mov.tipo == 'E' else 'Saída'
        writer.writerow([
            mov.data.strftime('%d/%m/%Y'),
            tipo,
            f"{mov.valor:.2f}".replace('.', ','),
            mov.categoria.nome if mov.categoria else '',
            mov.descricao
        ])
        
    return response


def exportar_extrato_conta_pdf(conta):
    movimentos = conta.movimentos.all().order_by('data', 'criado_em')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="extrato_conta_{conta.id}.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    elements.append(Paragraph(f"Extrato da Conta: {conta.nome}", styles['Title']))
    elements.append(Paragraph(f"Saldo Atual: R$ {conta.saldo:.2f}".replace('.', ','), styles['Heading2']))
    elements.append(Spacer(1, 12))
    
    data = [['Data', 'Tipo', 'Valor', 'Categoria', 'Descrição']]
    
    for mov in movimentos:
        tipo = 'Entrada' if mov.tipo == 'E' else 'Saída'
        data.append([
            mov.data.strftime('%d/%m/%Y'),
            tipo,
            f"R$ {mov.valor:.2f}".replace('.', ','),
            Paragraph(mov.categoria.nome if mov.categoria else '', styles['Normal']),
            Paragraph(mov.descricao, styles['Normal'])
        ])
        
    t = Table(data, colWidths=[60, 50, 70, 100, 180])
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


def exportar_contas_csv(request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contas_export.csv"'
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['ID', 'Nome', 'Saldo', 'Status', 'Descrição'])
    for c in queryset:
        writer.writerow([
            c.id, c.nome, 
            f"{c.saldo:.2f}".replace('.', ','),
            'Ativa' if c.ativa else 'Inativa',
            c.descricao
        ])
    return response

def exportar_contas_pdf(request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="contas_export.pdf"'
    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    elements.append(Paragraph("Relatório de Contas", styles['Title']))
    elements.append(Spacer(1, 12))
    data = [['Nome', 'Saldo', 'Status']]
    for c in queryset:
        data.append([
            Paragraph(c.nome, styles['Normal']),
            f"R$ {c.saldo:.2f}".replace('.', ','),
            'Ativa' if c.ativa else 'Inativa'
        ])
    t = Table(data, colWidths=[200, 100, 100])
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

def exportar_categorias_csv(request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="categorias_export.csv"'
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['ID', 'Nome', 'Tipo'])
    for c in queryset:
        writer.writerow([
            c.id, c.nome, 'Entrada' if c.tipo == 'E' else 'Saída'
        ])
    return response

def exportar_categorias_pdf(request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="categorias_export.pdf"'
    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    elements.append(Paragraph("Relatório de Categorias", styles['Title']))
    elements.append(Spacer(1, 12))
    data = [['Nome', 'Tipo']]
    for c in queryset:
        data.append([
            Paragraph(c.nome, styles['Normal']),
            'Entrada' if c.tipo == 'E' else 'Saída'
        ])
    t = Table(data, colWidths=[200, 150])
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
