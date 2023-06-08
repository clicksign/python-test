# python-test

Desenvolver um pequeno sistema de checkout e desconto em produtos.

**Requisitos:**

- Vendedor deve gerenciar (CRUD) dos produtos
- Vendedor deve cadastrar categorias dos produtos
- Usuário deve conseguir efetuar a compra de vários produtos

**Regras de Negócio:**

- Checkout do produto:
	- Desconto de 15% em produtos da categoria material escolar.
	- Levando 3 unidades do mesmo produto da categoria construção:
		- Desconto de 5% no valor total dos produtos dessa categoria.
	- Levando 5 unidades do mesmo produto da categoria construção:
		- Desconto de 7% no valor total dos produtos dessa categoria.
	- Não existe desconto para as demais categorias.

**OBS:**

- Escrever testes
- Usar Django Rest Framework
- Boas práticas no desenvolvimento da API
- Explicar no README como executar o projeto e as decisões técnicas
- Realizar um fork deste repositório e abrir o PR ao finalizar


---

## Como executar o projeto
- Pré-requisitos:
	- Docker
	- Docker Compose


- Variáveis de ambiente:
O arquivo `.env` contém as variáveis de ambiente necessárias para executar o projeto.
	- `cp .env.example .env`

- Executar o projeto:
	- `docker-compose up -d --build`

0s testes rodam automaticamente quando o container é criado.
Também são criados automaticamente alguns usuários de teste, produtos e categorias.
- Usuários:
	- `admin` - `admin123`
	- `seller` - `seller123`
	- `client` - `client123`


- Documentação da API (Swagger):
	- `http://localhost:8000`




## Decisões técnicas
- A estrutura do projeto foi desenvolvida utilizando o framework Django, juntamente com o Django Rest Framework para a criação de uma API RESTful.
- Para garantir a consistência e facilidade de configuração entre diferentes ambientes de desenvolvimento, aptei por utilizar Docker e Docker Compose.
- A fim de manter um alto padrão de qualidade de código, utilizei flake8 para análise estática de código.
- Para manter a consistência na formatação de código, adotamos o autopep8.
- Optamos pelo PostgreSQL como nosso sistema de gerenciamento de banco de dados.
- Segui o padrão de projeto do Django Rest Framework, que se baseia no padrão MVC, para estruturar nosso código.
- Para facilitar a compreensão e rastreabilidade do histórico de commits, adotamos o gitmoji para padronizar nossas mensagens de commit.
- Para garantir a qualidade do código, foram escritos testes unitários para as models, e testes de integração para a API.
- Para documentar a API, foi utilizado o Swagger, que é uma ferramenta de código aberto para documentar APIs RESTful.
