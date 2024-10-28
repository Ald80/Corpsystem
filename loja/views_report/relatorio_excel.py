from rest_framework.views import APIView
import pandas as pd
from io import BytesIO
from django.http import FileResponse
from .report_utils import validate_query_params, get_item_venda_by_filter, generate_dict_to_excel_report


class RelatorioExcelView(APIView):

    def get(self, request, *args, **kwargs):
        data = request.query_params.get('data')
        vendedor = request.query_params.get('vendedor')
        cliente = request.query_params.get('cliente')

        params_tuple = (data, vendedor, cliente)
        validate_query_params(params_tuple)
        item_venda_data = get_item_venda_by_filter(params_tuple)
        data_frame_dict = generate_dict_to_excel_report(item_venda_data)
        file_name = 'relatorio.xlsx'
        byte_buffer = BytesIO()
        df = pd.DataFrame.from_dict(data_frame_dict)

        writer = pd.ExcelWriter(byte_buffer, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='relatorio', index=True)
        writer.close()
        byte_buffer.seek(0)
        return FileResponse(byte_buffer, filename=file_name, as_attachment=True)
