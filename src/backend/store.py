from src.backend.models import Product, PurchaseRecord
from src.backend.product_array import ProductArray
from src.backend.cart import Cart
from src.backend.purchase_history import PurchaseHistory


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
