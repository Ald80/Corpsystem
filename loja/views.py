from loja.models import Cliente, Produto, Grupo, Vendedor, Venda, ItemVenda, StatusPedido
from rest_framework import viewsets
from loja.serializers import (ClienteSerializer, ProdutoSerializer, GrupoSerializer, VendedorSerializer, 
                              VendaSerializer, ItemVendaSerializer, StatusPedidoSerializer)
from rest_framework.views import APIView
from django.utils.dateparse import parse_date
import pandas as pd
from io import BytesIO
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.pdfgen import canvas
from datetime import datetime

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class= ClienteSerializer
    
class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class= ProdutoSerializer

class GrupoViewSet(viewsets.ModelViewSet):
    queryset = Grupo.objects.all()
    serializer_class= GrupoSerializer

class VendedorViewSet(viewsets.ModelViewSet):
    queryset = Vendedor.objects.all()
    serializer_class = VendedorSerializer

class VendaViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.all()
    serializer_class = VendaSerializer

class StatusPedidoViewSet(viewsets.ModelViewSet):
    queryset = StatusPedido.objects.all()
    serializer_class = StatusPedidoSerializer

class ItemVendaViewSet(viewsets.ModelViewSet):
    queryset = ItemVenda.objects.all()
    serializer_class = ItemVendaSerializer

class RelatorioPdfView(APIView):
    def get(self, request, *args, **kwargs):
        data = request.query_params.get('data')
        vendedor = request.query_params.get('vendedor')
        cliente= request.query_params.get('cliente')
        
        count_parameter = sum([1 for count in (data, vendedor, cliente) if count])

        if count_parameter > 1:
            return Response({"error": "Definir apenas um parâmetro na url: data, vendedor ou cliente"}, status=status.HTTP_404_NOT_FOUND)
        if data:
            item_venda = ItemVenda.objects.filter(venda__data_pedido=parse_date(data)).all()
        elif vendedor:
            print("vendedor")
            print(vendedor)
            item_venda = ItemVenda.objects.filter(venda__vendedor__nome=vendedor).all()
        elif cliente:
            item_venda = ItemVenda.objects.filter(venda__cliente__nome=cliente).all()
        else:
            return Response({"error": "Definir parâmetro na url: data, vendedor ou cliente"}, status=status.HTTP_404_NOT_FOUND)
        elements = []

        data_frame_dict = {
            'data_pedido': [],
            'produto_nome': [],
            'produto_descricao': [],
            'produto_preco': [],
            'grupo_descricao': [],
            'item_venda_quantidade_vendida': [],
            'vendedor_nome': [],
            'cliente_nome': [],
            'cliente_endereco': [],
            'cliente_email': [],
            'cliente_telefone': [],
            'status_pedido_descricao': [],
        }
        elements = [['data_pedido', 'produto_descricao', 'preco', 'grupo', 'vendedor', 'cliente_nome', 'status_pedido']]
        for i in item_venda:
            # print(i.venda.cliente.nome)
            # print(i.produto.grupo)
            # print(i.venda.cliente.email)
            # print(i.venda.vendedor.nome)
            values = []
            values.append(i.venda.data_pedido)
            values.append(i.produto.descricao)
            values.append(i.produto.preco)
            values.append(i.produto.grupo.descricao)
            values.append(i.venda.vendedor.nome)
            values.append(i.venda.cliente.nome)
            values.append(i.status_pedido.descricao)
            elements.append(values)
        # print(data_frame_dict)
        # df= pd.DataFrame.from_dict(data_frame_dict)
        # df= pd.DataFrame.from_dict(data_frame_dict)
        buffer = BytesIO()
        # doc = SimpleDocTemplate(buffer, pagesize=letter)
        # doc = SimpleDocTemplate(buffer, 
        #                         rightMargin=72,
        #                         leftMargin=72,
        #                         topMargin=72,
        #                         bottomMargin=72,
        #                         pagesize=letter)
        pdf = canvas.Canvas(buffer, pagesize=letter)
        # data = [[df.columns.to_list()], df.values.tolist()]
        # data1 = [
        #     ['data_pedido', 'produto', 'produto', 'preco', 'grupo', 'quantidade_vendida', 'vendedor', 'cliente_nome', 'cliente_endereco', 'cliente_email', 'cliente_telefone', 'status_pedido'],
        #     ['2021-03-02', 'Televisão', 'Smart TV Samsung 55"', '3000.00', 'Televisores', 12, 'Henrique Costa', 'Eduardo Lima', 'Rua XV de Novembro, 789', 'eduardolima@hotmail.com', '(48) 987654325', 'Concluído'],
        #     ['2021-03-02', 'Televisão', 'Smart TV Samsung 55"', '3000.00', 'Televisores', 1, 'João Pedro', 'Bruno Silva', 'Avenida Madre Benvenuta, 1000', 'brunosilva@hotmail.com', '(48) 987654322', 'Cancelado']
        # ]
        data1 = [
            ['data_pedido', 
            #  'produto_nome', 
             'produto_descricao', 'preco', 'grupo', 
            #  'quantidade_vendida', 
             'vendedor', 'cliente_nome', 
            #  'cliente_endereco', 'cliente_email', 'cliente_telefone', 
             'status_pedido'],
            ['2021-03-02', 
            #  'Televisão', 
             'Smart TV Samsung 55"', '3000.00', 'Televisores', 
            #  12, 
             'Henrique Costa', 'Eduardo Lima', 
            # 'Rua XV de Novembro, 789', 'eduardolima@hotmail.com', '(48) 987654325', 
             'Concluído'],
            ['2021-03-02', 
            #  'Televisão', 
             'Smart TV Samsung 55"', '3000.00', 'Televisores', 
            #  1, 
             'João Pedro', 'Bruno Silva', 
            # 'Avenida Madre Benvenuta, 1000', 'brunosilva@hotmail.com', '(48) 987654322', 
             'Cancelado']
        ]
        # table = Table(data1)
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
        table.setStyle(style)
        table.wrapOn(pdf, 0, 0)
        table.drawOn(pdf, 30, 700)
        pdf.showPage()
        pdf.save()
        buffer.seek(0)

        return FileResponse(buffer, as_attachment=True, filename='relatorio.pdf')
    
class RelatorioExcelView(APIView):
    def get(self, request, *args, **kwargs):
        data = request.query_params.get('data')
        vendedor = request.query_params.get('vendedor')
        cliente= request.query_params.get('cliente')
        print('asdsadsadsadsadasdasdasdsadasd')
        count_parameter = sum([1 for count in (data, vendedor, cliente) if count])
        print('count_parameter')
        print(count_parameter)

        if count_parameter > 1:
            return Response({"error": "Definir apenas um parâmetro na url: data, vendedor ou cliente"}, status=status.HTTP_404_NOT_FOUND)
        if data:
            item_venda = ItemVenda.objects.filter(venda__data_pedido=parse_date(data)).all()
        elif vendedor:
            print("vendedor")
            print(vendedor)
            item_venda = ItemVenda.objects.filter(venda__vendedor__nome=vendedor).all()
        elif cliente:
            item_venda = ItemVenda.objects.filter(venda__cliente__nome=cliente).all()
        else:
            return Response({"error": "Definir parâmetro na url: data, vendedor ou cliente"}, status=status.HTTP_404_NOT_FOUND)
        # print(data)
        # print(parse_date(data))
        # item_venda = ItemVenda.objects.filter(venda__data_pedido=parse_date(data)).all()
        # item_venda = ItemVenda.objects.filter(venda__data_pedido='2024-10-24')
        # item_venda = ItemVenda.objects.filter(venda__vendedor__nome='Henrique Costa1')
        # print("item_venda.count")
        # print(item_venda.count())
        # print(item_venda)

        columns = ['data_pedido', 'produto_nome', 'produto_descricao', 'produto_preco', 'grupo_descricao', 
                   'item_venda_quantidade_vendida', 'vendedor_nome', 'cliente_nome', 'cliente_endereco', 'cliente_email', 
                   'cliente_telefone', 'status_pedido_descricao']
        # item_venda = ItemVenda.objects.filter(venda__cliente__nome='Eduardo Lima')
        # items_venda = ItemVenda.objects.select_related(
        # 'venda',               # Join com Venda
        # 'venda__vendedor',     # Join com Vendedor através de Venda
        # 'venda__cliente',      # Join com Cliente através de Venda
        # 'produto',             # Join com Produto
        # 'produto__grupo',      # Join com Grupo através de Produto
        # 'status_pedido'        # Join com StatusPedido
        # ).filter(
        #     venda__cliente__nome='Ana Paula'  # Filtro por nome do cliente
        # )
    
        # 'status_pedido'
        data_frame_dict = {
            'data_pedido': [],
            'produto_nome': [],
            'produto_descricao': [],
            'produto_preco': [],
            'grupo_descricao': [],
            'item_venda_quantidade_vendida': [],
            'vendedor_nome': [],
            'cliente_nome': [],
            'cliente_endereco': [],
            'cliente_email': [],
            'cliente_telefone': [],
            'status_pedido_descricao': [],
        }

        for i in item_venda:
            # print(i.venda.cliente.nome)
            # print(i.produto.grupo)
            # print(i.venda.cliente.email)
            # print(i.venda.vendedor.nome)
            
            data_frame_dict['data_pedido'].append(i.venda.data_pedido)
            data_frame_dict['produto_nome'].append(i.produto.nome)
            data_frame_dict['produto_descricao'].append(i.produto.descricao)
            data_frame_dict['produto_preco'].append(i.produto.preco)
            data_frame_dict['grupo_descricao'].append(i.produto.grupo.descricao)
            data_frame_dict['item_venda_quantidade_vendida'].append(i.quantidade_vendida)
            data_frame_dict['vendedor_nome'].append(i.venda.vendedor.nome)
            data_frame_dict['cliente_nome'].append(i.venda.cliente.nome)
            data_frame_dict['cliente_endereco'].append(i.venda.cliente.endereco)
            data_frame_dict['cliente_email'].append(i.venda.cliente.email)
            data_frame_dict['cliente_telefone'].append(i.venda.cliente.telefone)
            data_frame_dict['status_pedido_descricao'].append(i.status_pedido.descricao)
        # print(data_frame_dict)
        # df= pd.DataFrame.from_dict(data_frame_dict)
        file_name = 'relatorio.xlsx'
        byte_buffer = BytesIO()
        df= pd.DataFrame.from_dict(data_frame_dict)

        writer = pd.ExcelWriter(byte_buffer, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='relatorio', index=True)
        writer.close()
        # .from_dict(data_frame_dict)
        print(df)
        byte_buffer.seek(0)
        return FileResponse(byte_buffer, filename=file_name, as_attachment=True)
  
        # print(ItemVenda.objects.select_related('venda'))
        # print(._meta.get_fields())
        # venda = ItemVenda.objects.select_related('venda').all()
        # print(ItemVenda.objects.all())
        
        # for i in venda.model._meta.get_fields():
        #     print(i.name)

        # for i in venda:
        #     print(i)
        # return 1