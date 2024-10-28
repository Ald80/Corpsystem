from django.test import TestCase
from loja.serializers import ClienteSerializer

class ClienteSerializerTest(TestCase):
    def setUp(self):
        self.data_valid = {'nome': 'Otávio Ribeiro', 
                                'endereco': 'Avenida Rio Branco, 415', 
                                'email': 'otavioribeiro@hotmail.com', 
                                'telefone': '(48) 987654334'
                                }
        self.data_invalid = {'nome': '', 
                                'endereco': 'Avenida Rio Branco, 415', 
                                'email': 'otavioribeiro@hotmail.com', 
                                'telefone': '(48) 987654334'
                                }

    def test_serializer_valid(self):
        serializer = ClienteSerializer(data=self.data_valid)
        self.assertTrue(serializer.is_valid())

    def test_serializer_invalid(self):
        serializer = ClienteSerializer(data=self.data_invalid)
        serializer.is_valid()
        self.assertFalse(serializer.is_valid())
        self.assertIn('nome', serializer.errors)