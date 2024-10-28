from rest_framework.response import Response
from rest_framework import status
from loja.models import ItemVenda
from django.utils.dateparse import parse_date


def validate_query_params(params_tuple):
    count_parameter = sum([1 for count in (params_tuple) if count])

    if count_parameter > 1:
        return Response(
            {'error': 'Definir apenas um parâmetro na url: data, vendedor ou cliente'},
            status=status.HTTP_404_NOT_FOUND)
    elif count_parameter == 0:
        return Response(
            {'error': 'Definir parâmetro na url: data, vendedor ou cliente'},
            status=status.HTTP_404_NOT_FOUND)


def get_item_venda_by_filter(params_tuple):
    data, vendedor, cliente = params_tuple
    if data:
        return ItemVenda.objects.filter(venda__data_pedido=parse_date(data)).all()
    elif vendedor:
        return ItemVenda.objects.filter(venda__vendedor__nome=vendedor).all()
    elif cliente:
        return ItemVenda.objects.filter(venda__cliente__nome=cliente).all()


def generate_dict_to_excel_report(item_venda_data):
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

    for i in item_venda_data:
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

    return data_frame_dict


def generate_list_to_pdf_report(item_venda_data):
    elements = [[
        'data_pedido', 'produto_descricao', 'preco', 'grupo', 'vendedor',
        'cliente_nome', 'status_pedido'
    ]]
    for i in item_venda_data:
        values = []
        values.append(i.venda.data_pedido)
        values.append(i.produto.descricao)
        values.append(i.produto.preco)
        values.append(i.produto.grupo.descricao)
        values.append(i.venda.vendedor.nome)
        values.append(i.venda.cliente.nome)
        values.append(i.status_pedido.descricao)
        elements.append(values)

    return elements
