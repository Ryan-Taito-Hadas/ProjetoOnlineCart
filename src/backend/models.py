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
