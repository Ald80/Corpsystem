# Corpsystem

## Dependências
- Django Rest
- Mysql Client
- Pandas
- Reportlab

## Instruções

- Instale o mysql no seu computador local
    
    - Links:
        
        - [Windows](https://dev.mysql.com/downloads/installer/)
        - [Linux](https://dev.mysql.com/doc/refman/8.4/en/linux-installation.html)

- **OBS: Como alternativa, também é possível instalar o banco de dados MariaDB, que é um fork do mysql opensource**

    - Link:
        
        - [Windows/Linux](https://mariadb.org/download/?t=mariadb&p=mariadb&r=11.5.2&os=Linux&cpu=x86_64&i=systemd&mirror=fder)

- Crie o banco de dados a ser usado na aplicação:

```
CREATE DATABASE IF NOT EXISTS loja_venda
```

- Crie um ambiente virtual do projeto:

```
python -m venv venv
```

- Em seguida, instale as dependências necessárias para o projeto:

```
pip install -r requirements.txt
```

- Insira a configuração do seu banco de dados no arquivo `settings.py`:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'loja_venda',
        'USER': '<seu_usuario>',
        'PASSWORD': '<sua_senha>',
        'HOST': '127.0.0.1',
        'PORT': '<porta-usada>',
    }
}
```

- Roda os comandos abaixo para realizar as migrations no banco de dados

```
python manage.py makemigrations
```

```
python manage.py migrate loja
```

- Execute as chamadas HTTP para inserir os dados:

```
url: http://127.0.0.1:8000/api/cliente

POST

{
    "nome": "Ana Paula",
    "endereco": "Rua Delminda Silveira, 123",
    "email": "anapaula@hotmail.com",
    "telefone": "(48) 987654321"
}
```

```
url: http://127.0.0.1:8000/api/grupo

POST

{
    "descricao": "Eletrônicos"
}

```

```
url: http://127.0.0.1:8000/api/produto

POST

{
    "nome": "Notebook",
    "descricao": "Notebook Dell Inspiron",
    "preco": "3500.00",
    "grupo": 1
}
```

```
url: http://127.0.0.1:8000/api/vendedor

POST

{
    "nome": "Fernando Almeida"
}
```

```
url: http://127.0.0.1:8000/api/venda

POST

{
    "data_pedido": "2024-02-02",
    "cliente": 1,
    "vendedor": 1
}
```

```
url: http://127.0.0.1:8000/api/status-pedido

POST

{
    "descricao": "Concluído"
}
```

```
url: http://127.0.0.1:8000/api/status-pedido

POST

{
    "descricao": "Cancelado"
}
```

```
url: http://127.0.0.1:8000/api/item-venda

POST

{
    "quantidade_vendida": 2,
    "venda": 1,
    "produto": 1,
    "status_pedido": 1
}
```

- Gere relatorio tanto excel quanto pdf filtrando por cliente ou vendedor ou data.

    - URLs para excel:
        - http://127.0.0.1:8000/api/relatorio-excel/?data=2024-02-02
        - http://127.0.0.1:8000/api/relatorio-excel/?vendedor=Fernando%20Almeida
        - http://127.0.0.1:8000/api/relatorio-excel/?cliente=Ana%20Paula
    
    - URLs para pdf:
        - http://127.0.0.1:8000/api/relatorio-pdf/?data=2024-02-02
        - http://127.0.0.1:8000/api/relatorio-pdf/?vendedor=Fernando%20Almeida
        - http://127.0.0.1:8000/api/relatorio-pdf/?cliente=Ana%20Paula

- Caso queira mais dados de teste, execute os comandos sql para inserir dados:

```
INSERT INTO loja_cliente (nome, endereco, email, telefone) VALUES
('Bruno Silva', 'Avenida Madre Benvenuta, 1000', 'brunosilva@hotmail.com', '(48) 987654322'),
('Carlos Alberto', 'Rua Antônio Carlos Ferreira, 45', 'carlosalberto@hotmail.com', '(48) 987654323'),
('Daniela Souza', 'Avenida Professor Milton Leite da Costa, 400', 'danisouza@hotmail.com', '(48) 987654324');

INSERT INTO loja_grupo (descricao) VALUES
('Celulares'),
('Televisores'),
('Acessórios de Áudio');

INSERT INTO loja_produto (nome, descricao, preco, grupo_id) VALUES
('Smartphone', 'iPhone 12', 4500.00, 2),
('Televisão', 'Smart TV Samsung 55"', 3000.00, 3),
('Fone de Ouvido', 'Fone Bluetooth JBL', 250.00, 4);

INSERT INTO loja_vendedor (id, nome) VALUES
('Gabriela Martins'),
('Henrique Costa'),
('Isabela Nunes');


INSERT INTO loja_itemvenda (quantidade_vendida,produto_id,venda_id,status_pedido_id) VALUES
	 (12,3,2,1),
	 (1,3,3,2);


INSERT INTO loja_venda (data_pedido,cliente_id,vendedor_id) VALUES
	 ('2024-01-01',1,1),
	 ('2024-02-02',5,3),
	 ('2024-02-02',2,5);
```

- Para rodar os testes unitários, execute o comando:

```
 python manage.py test
```