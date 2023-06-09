# python-test

## Requisitos

- Python 3.8.x
- Poetry

## Instalação

Ir para o diretório do projeto e executar o comando:
```
poetry install
```

## Como executar

Criar arquivo .env:
```
cp local.env .env
```

Ativar env do poetry:
```
poetry shell
```

Executar migrações do projeto:
```
python manage.py makemigration
```
```
python manage.py migrate
```

Para facilitar o uso da aplicação pode ser importado os users "admin" e "buyer" através de comando, se não será necessário efetuar a criação através de comando e atribuir o perfil:
```
python manage.py loaddata users
```
```
user:superuser password:superuser

user:admin password:pass12345

user:buyer password:pass12345
```

Executar a aplicação:
```
python manage.py runserver
```

Para executar os testes do projeto:
```
poetry run pytest -sx
```

Também é possível utilizar o arquivo Makefile que possui comandos facilitadores, exemplo para executar testes e linter:
```
make test
```
```
make lint
```

Swagger da API:
```
http://127.0.0.1:8000/v1/docs/
```

Endpoint de login para gerar token:
```
http://127.0.0.1:8000/v1/login/
```

Demais requisições incluir header conforme a seguir:
```
Authorization: Token xxxx
```

## Decisões Lógicas

Foi utilizado a autenticação nativa do DRF, sendo criado uma app "users" qual armazena a role do usuário, com as opções "buyer" ou "admin".
Buyer possui acesso de comprador, com possibilidade de recuperar produtos e criar pedidos.
Admin possui acesso total a API, como cadastrar produtos, outros usuário "admin" e atualizar/deletar registros.
Mantido o banco de dados SQLite apenas para facilitar a execução do projeto.

Para tratar os descontos por categoria, foram criados os modelos "Product", "Category" e "CategoryDiscount".
Caso um produto pertença a uma categoria com "CategoryDiscount" registrado, ele estará qualificado para obter desconto, este modelo possui os campos "discount_percentage" e "product_quantity".
No momento da compra será verificado as categorias pertecentes ao produto, filtrando assim a quantidade a ser adquirida com o campo "product_quantity", retornando o maior desconto válido para o produto.

Modelos do projeto:

- Product: Produtos a serem vendidos
- Category: Categorias de um produto
- CategoryDiscount: Descontos de uma categoria por quantidade
- Order: Pedidos realizados
- OrderItems: Produtos de um pedido
- UserProfile: Extensão do modelo User que armazena a permissão do usuário
