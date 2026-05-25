from src.backend.product_array import Product, Store


def _format_currency(value: float) -> str:
    return f"R$ {value:.2f}".replace(".", ",", 1)


def _read_non_empty_text(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("O valor não pode estar vazio.")


def _read_int(prompt: str, minimum: int = 0) -> int:
    while True:
        try:
            value = int(input(prompt).strip())
            if value < minimum:
                print(f"Digite um valor maior ou igual a {minimum}.")
                continue
            return value
        except ValueError:
            print("Digite um número inteiro válido.")


def _read_float(prompt: str, minimum: float = 0.0) -> float:
    while True:
        try:
            value = float(input(prompt).strip().replace(",", "."))
            if value < minimum:
                print(f"Digite um valor maior ou igual a {minimum}.")
                continue
            return value
        except ValueError:
            print("Digite um número válido.")


def _show_products(products: list[Product]) -> None:
    products = list(products)

    print("\nProdutos cadastrados:")
    if not products:
        print("Nenhum produto cadastrado ainda.")
        return

    for product in products:
        print(
            f"{product.code}. {product.name} | {product.category} | "
            f"{_format_currency(product.price)} | Estoque: {product.quantity}"
        )


def _show_cart(store: Store) -> None:
    items = store.cart.items()
    print("\nCarrinho:")
    if not items:
        print("O carrinho está vazio.")
        return

    for item in items:
        subtotal = item.unit_price * item.quantity
        print(
            f"{item.product_code}. {item.name} | {item.category} | "
            f"Qtd: {item.quantity} | Subtotal: {_format_currency(subtotal)}"
        )

    print(f"Total: {_format_currency(store.cart.total())}")


def _show_history(store: Store) -> None:
    records = store.history.list_records()
    print("\nHistórico de compras:")
    if not records:
        print("Nenhuma compra finalizada ainda.")
        return

    for record in records:
        print(f"Compra {record.purchase_id} - Total: {_format_currency(record.total)}")
        for item in record.items:
            print(
                f"  {item.product_code}. {item.name} | {item.category} | "
                f"Qtd: {item.quantity} | {_format_currency(item.unit_price)}"
            )


def _show_search_results(title: str, products: list[Product]) -> None:
    print(f"\n{title}")
    if not products:
        print("Nenhum resultado encontrado.")
        return

    _show_products(products)


def main() -> None:
    store = Store()

    while True:
        print("\n=== Projeto Online Cart ===")
        print("1. Cadastrar produto")
        print("2. Exibir produtos")
        print("3. Buscar produto por nome")
        print("4. Buscar produto por categoria")
        print("5. Ordenar produtos por nome")
        print("6. Ordenar produtos por preço")
        print("7. Adicionar produto ao carrinho")
        print("8. Remover produto do carrinho")
        print("9. Desfazer última ação")
        print("10. Exibir carrinho")
        print("11. Finalizar compra")
        print("12. Exibir histórico")
        print("0. Sair")

        option = input("Escolha uma opção: ").strip()

        if option == "1":
            print("\nCadastro de produto")
            name = _read_non_empty_text("Nome: ")
            category = _read_non_empty_text("Categoria: ")
            price = _read_float("Preço: ", minimum=0.0)
            quantity = _read_int("Quantidade em estoque: ", minimum=0)

            product = store.add_product(name, category, price, quantity)
            print(f"Produto cadastrado com sucesso. Código: {product.code}")
            _show_products(store.products.list_products())
        elif option == "2":
            _show_products(store.products.list_products())
        elif option == "3":
            query = _read_non_empty_text("Nome para buscar: ")
            _show_search_results("Resultados da busca por nome:", store.products.search_by_name(query))
        elif option == "4":
            query = _read_non_empty_text("Categoria para buscar: ")
            _show_search_results("Resultados da busca por categoria:", store.products.search_by_category(query))
        elif option == "5":
            _show_products(store.products.sorted_by_name())
        elif option == "6":
            _show_products(store.products.sorted_by_price())
        elif option == "7":
            code = _read_int("Código do produto: ", minimum=1)
            quantity = _read_int("Quantidade: ", minimum=1)
            product = store.products.find_by_code(code)
            if product is None:
                print("Produto não encontrado.")
                continue
            try:
                store.cart.add_product(product, quantity)
                print("Produto adicionado ao carrinho.")
            except ValueError as error:
                print(error)
        elif option == "8":
            code = _read_int("Código do produto: ", minimum=1)
            quantity = _read_int("Quantidade: ", minimum=1)
            product = store.products.find_by_code(code)
            if product is None:
                print("Produto não encontrado.")
                continue
            try:
                store.cart.remove_product(product, quantity)
                print("Produto removido do carrinho.")
            except ValueError as error:
                print(error)
        elif option == "9":
            try:
                message = store.cart.undo_last_action(store.products)
                print(message)
            except ValueError as error:
                print(error)
        elif option == "10":
            _show_cart(store)
        elif option == "11":
            try:
                record = store.finalize_purchase()
                print(f"Compra finalizada com sucesso. Total: {_format_currency(record.total)}")
            except ValueError as error:
                print(error)
        elif option == "12":
            _show_history(store)
        elif option == "0":
            print("Encerrando aplicação.")
            break
        else:
            print("Opção inválida.")