from src.backend.models import PurchaseRecord, PurchaseNode


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
