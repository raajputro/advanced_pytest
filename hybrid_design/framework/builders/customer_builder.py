"""Builder: create independent, immutable test-data objects."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Customer:
    first_name: str
    last_name: str
    postal_code: str


class CustomerBuilder:
    def __init__(self):
        self._first_name = "Ada"
        self._last_name = "Lovelace"
        self._postal_code = "1205"

    def with_name(self, first: str, last: str):
        self._first_name, self._last_name = first, last
        return self

    def with_postal_code(self, code: str):
        self._postal_code = code
        return self

    def build(self) -> Customer:
        return Customer(self._first_name, self._last_name, self._postal_code)
