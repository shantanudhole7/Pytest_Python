from dataclasses import asdict, dataclass, field


@dataclass
class Order:
    country: str = "India"
    productOrderedId: str = ""


@dataclass
class CreateOrder:
    orders: list[Order] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)