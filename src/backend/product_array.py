from src.backend.models import Product


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