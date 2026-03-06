import csv

from django.http import HttpResponse


REPORTLAB_AVAILABLE = True
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
except ModuleNotFoundError:
    REPORTLAB_AVAILABLE = False


def _pdf_dependency_error_response():
    return HttpResponse(
        'Exportação em PDF indisponível porque a dependência "reportlab" não está instalada.',
        status=503,
        content_type='text/plain; charset=utf-8',
    )


def exportar_membros_csv(request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="membros_export.csv"'

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['ID', 'Nome', 'Email', 'Telefone', 'Cargo', 'Congregação', 'Área', 'Ativo'])

    for obj in queryset:
        writer.writerow(
            [
                obj.id,
                obj.nome,
                obj.email,
                obj.telefone,
                obj.cargo,
                obj.congregacao.nome if obj.congregacao else '',
                obj.area.nome if obj.area else '',
                'Sim' if obj.ativo else 'Não',
            ]
        )

    return response


def exportar_membros_pdf(request, queryset):
    if not REPORTLAB_AVAILABLE:
        return _pdf_dependency_error_response()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="membros_export.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph('Relatório de Membros', styles['Title']))
    elements.append(Spacer(1, 12))

    data = [['Nome', 'Telefone', 'Cargo', 'Congregação']]

    for obj in queryset:
        data.append(
            [
                Paragraph(obj.nome, styles['Normal']),
                Paragraph(obj.telefone, styles['Normal']),
                Paragraph(obj.cargo, styles['Normal']),
                Paragraph(obj.congregacao.nome if obj.congregacao else '', styles['Normal']),
            ]
        )

    t = Table(data, colWidths=[150, 80, 100, 150])
    t.setStyle(
        TableStyle(
            [
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]
        )
    )

    elements.append(t)
    doc.build(elements)
    return response


def exportar_congregacoes_csv(request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="congregacoes_export.csv"'
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['ID', 'Nome', 'Área'])
    for obj in queryset:
        writer.writerow([obj.id, obj.nome, obj.area.nome if obj.area else ''])
    return response


def exportar_congregacoes_pdf(request, queryset):
    if not REPORTLAB_AVAILABLE:
        return _pdf_dependency_error_response()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="congregacoes_export.pdf"'
    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    elements.append(Paragraph('Relatório de Congregações', styles['Title']))
    elements.append(Spacer(1, 12))
    data = [['Nome', 'Área']]
    for obj in queryset:
        data.append([Paragraph(obj.nome, styles['Normal']), Paragraph(obj.area.nome if obj.area else '', styles['Normal'])])
    t = Table(data, colWidths=[200, 200])
    t.setStyle(
        TableStyle(
            [
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]
        )
    )
    elements.append(t)
    doc.build(elements)
    return response


def exportar_areas_csv(request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="areas_export.csv"'
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['ID', 'Nome'])
    for obj in queryset:
        writer.writerow([obj.id, obj.nome])
    return response


def exportar_areas_pdf(request, queryset):
    if not REPORTLAB_AVAILABLE:
        return _pdf_dependency_error_response()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="areas_export.pdf"'
    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    elements.append(Paragraph('Relatório de Áreas', styles['Title']))
    elements.append(Spacer(1, 12))
    data = [['ID', 'Nome']]
    for obj in queryset:
        data.append([obj.id, Paragraph(obj.nome, styles['Normal'])])
    t = Table(data, colWidths=[50, 300])
    t.setStyle(
        TableStyle(
            [
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]
        )
    )
    elements.append(t)
    doc.build(elements)
    return response



def exportar_quantitativo_csv(request, queryset):
    return exportar_membros_csv(request, queryset)


def exportar_quantitativo_pdf(request, queryset):
    return exportar_membros_pdf(request, queryset)
