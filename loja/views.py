from rest_framework import viewsets

from loja.models import (Cliente, Grupo, ItemVenda, Produto, StatusPedido, Venda,
                         Vendedor)
from loja.serializers import (ClienteSerializer, GrupoSerializer, ItemVendaSerializer,
                              ProdutoSerializer, StatusPedidoSerializer,
                              VendaSerializer, VendedorSerializer)


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer


class GrupoViewSet(viewsets.ModelViewSet):
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer


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
