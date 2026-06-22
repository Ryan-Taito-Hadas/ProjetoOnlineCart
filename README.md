# Projeto Online Cart

## Integrantes

- Vinicius Antonio Lourençon
- Nicolas Wolf
- Ryan Lopes Hadas

## Tema / Projeto escolhido

**Projeto 02 — Carrinho de compras**

## Descrição do projeto

Este projeto foi desenvolvido para a disciplina de **Estrutura de Dados**.

O sistema simula o funcionamento de um carrinho de compras de uma loja virtual. O usuário pode cadastrar produtos, buscar e ordenar produtos, adicionar produtos ao carrinho, remover produtos, desfazer a última ação realizada, visualizar o resumo da compra, finalizar a compra e consultar o histórico de compras realizadas.

Durante o desenvolvimento, foram aplicados conceitos de estruturas de dados estudados na disciplina, como pilha, lista encadeada, algoritmos de busca, algoritmos de ordenação e tabela hash.

## Tecnologia de front-end escolhida

A interface do sistema foi desenvolvida via **terminal**, utilizando Python.

Essa escolha foi feita para manter o foco principal na lógica do sistema e na implementação das estruturas de dados, conforme solicitado na disciplina.

## Backend

O backend foi desenvolvido em **Python 3**, versão **3.8 ou superior**.

A lógica do sistema e as estruturas de dados exigidas (pilha e lista encadeada) foram implementadas manualmente pelo grupo, sem o uso de bibliotecas prontas para substituí-las. Para a etapa de busca e ordenação, foram utilizados recursos nativos do Python (`sorted()` e list comprehensions).

## Estruturas de dados utilizadas

- **Pilha:** utilizada para desfazer a última ação realizada no carrinho.
- **Lista encadeada:** utilizada para armazenar o histórico de compras realizadas.
- **Tabela hash:** utilizada para localizar rapidamente produtos por código.
- **Algoritmos de ordenação:** utilizados para ordenar produtos por nome ou preço.
- **Algoritmos de busca:** utilizados para buscar produtos por nome ou categoria.

## Funcionalidades implementadas

- Cadastrar produto com nome, categoria, preço e quantidade em estoque.
- Exibir todos os produtos cadastrados.
- Buscar produto por nome (busca parcial, sem diferenciar maiúsculas/minúsculas).
- Buscar produto por categoria (busca parcial, sem diferenciar maiúsculas/minúsculas).
- Ordenar produtos por nome (ordem alfabética).
- Ordenar produtos por preço (ordem crescente).
- Adicionar produto ao carrinho com a quantidade desejada.
- Remover produto do carrinho.
- Desfazer a última ação realizada no carrinho (pilha de undo).
- Exibir resumo do carrinho com total atualizado.
- Finalizar compra e atualizar estoque.
- Exibir histórico de compras realizadas (lista encadeada).
- Localizar rapidamente produto por código utilizando tabela hash.

## Instruções para execução do projeto

1. Clone o repositório:

```bash
git clone https://github.com/Ryan-Taito-Hadas/ProjetoOnlineCart
```

2. Acesse a pasta do projeto:

```bash
cd ProjetoOnlineCart
```

3. Execute o arquivo principal:

```bash
python main.py
```

## Estrutura do projeto

```
main.py                        # ponto de entrada da aplicação
src/backend/models.py          # entidades (Product, CartItem, PurchaseRecord, PurchaseNode)
src/backend/product_array.py   # cadastro, busca e ordenação de produtos
src/backend/cart.py            # carrinho de compras e pilha de undo
src/backend/purchase_history.py # histórico de compras (lista encadeada)
src/backend/store.py           # integração entre produtos, carrinho e histórico
src/ui/terminal_app.py         # interface de terminal (menu)
```

## Status

Todas as funcionalidades previstas estão implementadas e funcionando via menu de terminal.
