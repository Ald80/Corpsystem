from rest_framework.views import APIView
from io import BytesIO
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.pdfgen import canvas
from .report_utils import validate_query_params, get_item_venda_by_filter, generate_list_to_pdf_report


class RelatorioPdfView(APIView):

    def get(self, request, *args, **kwargs):
        data = request.query_params.get('data')
        vendedor = request.query_params.get('vendedor')
        cliente = request.query_params.get('cliente')

        params_tuple = (data, vendedor, cliente)
        validate_query_params(params_tuple)
        item_venda_data = get_item_venda_by_filter(params_tuple)
        elements = generate_list_to_pdf_report(item_venda_data)
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        table = Table(elements)
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (80, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        filename = 'relatorio.pdf'
        table.setStyle(style)
        table.wrapOn(pdf, 0, 0)
        table.drawOn(pdf, 30, 700)
        pdf.showPage()
        pdf.save()
        buffer.seek(0)

        return FileResponse(buffer, as_attachment=True, filename=filename)
