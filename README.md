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
