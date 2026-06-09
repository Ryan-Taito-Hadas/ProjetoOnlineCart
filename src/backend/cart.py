from src.backend.models import Product, CartItem, PurchaseRecord


class Cart:
    def __init__(self) -> None:
        self._items: list[CartItem] = []
        self._undo_stack: list[tuple[str, int, int]] = []

    def add_product(self, product: Product, quantity: int) -> CartItem:
        if quantity <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        if quantity > product.quantity:
            raise ValueError("Quantidade indisponível em estoque.")

        item = self._find_item(product.code)
        if item is None:
            item = CartItem(
                product_code=product.code,
                name=product.name,
                category=product.category,
                unit_price=product.price,
                quantity=quantity,
            )
            self._items.append(item)
        else:
            item.quantity += quantity

        product.quantity -= quantity
        self._undo_stack.append(("add", product.code, quantity))
        return item

    def remove_product(self, product: Product, quantity: int) -> CartItem:
        if quantity <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")

        item = self._find_item(product.code)
        if item is None or item.quantity < quantity:
            raise ValueError("Quantidade indisponível no carrinho.")

        item.quantity -= quantity
        if item.quantity == 0:
            self._items.remove(item)

        product.quantity += quantity
        self._undo_stack.append(("remove", product.code, quantity))
        return item

    def undo_last_action(self, product_array) -> str:
        if not self._undo_stack:
            raise ValueError("Não há ações para desfazer.")

        action, product_code, quantity = self._undo_stack.pop()
        product = product_array.find_by_code(product_code)
        if product is None:
            raise ValueError("Produto não encontrado para desfazer a ação.")

        if action == "add":
            item = self._find_item(product_code)
            if item is None or item.quantity < quantity:
                raise ValueError("Carrinho inconsistente para desfazer a ação.")
            item.quantity -= quantity
            if item.quantity == 0:
                self._items.remove(item)
            product.quantity += quantity
            return "Adição desfeita com sucesso."

        item = self._find_item(product_code)
        if item is None:
            item = CartItem(
                product_code=product.code,
                name=product.name,
                category=product.category,
                unit_price=product.price,
                quantity=quantity,
            )
            self._items.append(item)
        else:
            item.quantity += quantity

        if product.quantity < quantity:
            raise ValueError("Estoque insuficiente para desfazer a remoção.")
        product.quantity -= quantity
        return "Remoção desfeita com sucesso."

    def checkout(self, purchase_id: int) -> PurchaseRecord:
        if not self._items:
            raise ValueError("O carrinho está vazio.")

        record = PurchaseRecord(
            purchase_id=purchase_id,
            items=[
                CartItem(
                    product_code=item.product_code,
                    name=item.name,
                    category=item.category,
                    unit_price=item.unit_price,
                    quantity=item.quantity,
                )
                for item in self._items
            ],
            total=self.total(),
        )
        self._items.clear()
        self._undo_stack.clear()
        return record

    def items(self) -> list[CartItem]:
        return [
            CartItem(
                product_code=item.product_code,
                name=item.name,
                category=item.category,
                unit_price=item.unit_price,
                quantity=item.quantity,
            )
            for item in self._items
        ]

    def total(self) -> float:
        return sum(item.unit_price * item.quantity for item in self._items)

    def has_items(self) -> bool:
        return bool(self._items)

    def _find_item(self, product_code: int) -> CartItem | None:
        for item in self._items:
            if item.product_code == product_code:
                return item
        return None
