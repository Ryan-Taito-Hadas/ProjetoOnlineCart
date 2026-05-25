from dataclasses import dataclass


@dataclass(slots=True)
class Product:
    code: int
    name: str
    category: str
    price: float
    quantity: int


@dataclass(slots=True)
class CartItem:
    product_code: int
    name: str
    category: str
    unit_price: float
    quantity: int


@dataclass(slots=True)
class PurchaseRecord:
    purchase_id: int
    items: list[CartItem]
    total: float


@dataclass(slots=True)
class PurchaseNode:
    record: PurchaseRecord
    next: "PurchaseNode | None" = None


class ProductArray:
    def __init__(self) -> None:
        self._products: list[Product] = []
        self._by_code: dict[int, Product] = {}
        self._next_code = 1

    def add_product(self, name: str, category: str, price: float, quantity: int) -> Product:
        product = Product(
            code=self._next_code,
            name=name.strip(),
            category=category.strip(),
            price=price,
            quantity=quantity,
        )
        self._products.append(product)
        self._by_code[product.code] = product
        self._next_code += 1
        return product

    def list_products(self) -> list[Product]:
        return list(self._products)

    def sorted_by_name(self) -> list[Product]:
        return sorted(self._products, key=lambda product: product.name.lower())

    def sorted_by_price(self) -> list[Product]:
        return sorted(self._products, key=lambda product: product.price)

    def search_by_name(self, query: str) -> list[Product]:
        normalized_query = query.strip().lower()
        return [
            product
            for product in self._products
            if normalized_query in product.name.lower()
        ]

    def search_by_category(self, query: str) -> list[Product]:
        normalized_query = query.strip().lower()
        return [
            product
            for product in self._products
            if normalized_query in product.category.lower()
        ]

    def find_by_code(self, code: int) -> Product | None:
        return self._by_code.get(code)

    def has_products(self) -> bool:
        return bool(self._products)


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

    def undo_last_action(self, product_array: ProductArray) -> str:
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


class PurchaseHistory:
    def __init__(self) -> None:
        self._head: PurchaseNode | None = None
        self._tail: PurchaseNode | None = None

    def add(self, record: PurchaseRecord) -> None:
        node = PurchaseNode(record=record)
        if self._head is None:
            self._head = node
            self._tail = node
            return

        assert self._tail is not None
        self._tail.next = node
        self._tail = node

    def list_records(self) -> list[PurchaseRecord]:
        records: list[PurchaseRecord] = []
        current = self._head
        while current is not None:
            records.append(current.record)
            current = current.next
        return records


class Store:
    def __init__(self) -> None:
        self.products = ProductArray()
        self.cart = Cart()
        self.history = PurchaseHistory()
        self._next_purchase_id = 1

    def add_product(self, name: str, category: str, price: float, quantity: int) -> Product:
        return self.products.add_product(name, category, price, quantity)

    def finalize_purchase(self) -> PurchaseRecord:
        record = self.cart.checkout(self._next_purchase_id)
        self.history.add(record)
        self._next_purchase_id += 1
        return record