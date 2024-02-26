from dataclasses import dataclass
from datetime import date, datetime
from typing import Dict, Union


@dataclass
class Trip:
    country: str
    key: str
    departure_date: date
    price: int
    currency: str

    @staticmethod
    def from_dict(data_dict: Dict[str, Union[str, Dict[str, str]]]) -> "Trip":
        data_layer = data_dict.get("DataLayerV4", {})
        currency = data_layer.get("currency", "PLN").upper()
        departure_date = datetime.strptime(
            data_dict.get("TerminWyjazdu"), "%Y-%m-%dT%H:%M:%SZ"
        ).date()
        return Trip(
            country=data_dict.get("Panstwo"),
            key=data_dict.get("Klucz"),
            departure_date=departure_date,
            price=data_dict.get("Cena"),
            currency=currency,
        )
