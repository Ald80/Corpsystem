from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from loja.models import Cliente


class ClienteViewSet(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.cliente = Cliente.objects.create(nome='Otávio Ribeiro',
                                              endereco='Avenida Rio Branco, 415',
                                              email='otavioribeiro@hotmail.com',
                                              telefone='(48) 987654334')
        self.list_url = reverse('cliente-list')
        self.detail_url = reverse('cliente-detail', args=[self.cliente.pk])

    def test_get_cliente(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_post_cliente(self):
        cliente_data = {
            'nome': 'Natália Costa',
            'endereco': 'Rua José Francisco Dias, 98',
            'email': 'nataliacosta@hotmail.com',
            'telefone': '(48) 987654333'
        }

        response = self.client.post(self.list_url, cliente_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cliente.objects.count(), 2)

    def test_retrieve_cliente(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], 'Otávio Ribeiro')

    def test_update_cliente(self):
        cliente_data = {
            'nome': 'Otávio Ribeiro Almeida',
            'endereco': 'Avenida Rio Branco, 415',
            'email': 'otavioribeiro@hotmail.com',
            'telefone': '(48) 987654334'
        }

        response = self.client.put(self.detail_url, cliente_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], 'Otávio Ribeiro Almeida')

    def test_delete_cliente(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Cliente.objects.count(), 0)
