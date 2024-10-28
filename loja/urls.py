from django.urls import path, include
from rest_framework.routers import DefaultRouter
from loja.views import (ClienteViewSet, ProdutoViewSet, GrupoViewSet, VendedorViewSet,
                        VendaViewSet, ItemVendaViewSet, StatusPedidoViewSet)
from loja.views_report.relatorio_excel import RelatorioExcelView
from loja.views_report.relatorio_pdf import RelatorioPdfView

router = DefaultRouter(trailing_slash=False)
router.register(r'cliente', ClienteViewSet)
router.register(r'produto', ProdutoViewSet)
router.register(r'grupo', GrupoViewSet)
router.register(r'vendedor', VendedorViewSet)
router.register(r'venda', VendaViewSet)
router.register(r'item-venda', ItemVendaViewSet)
router.register(r'status-pedido', StatusPedidoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('relatorio-excel/', RelatorioExcelView.as_view(), name='relatorio-excel'),
    path('relatorio-pdf/', RelatorioPdfView.as_view(), name='relatorio-pdf'),
]
