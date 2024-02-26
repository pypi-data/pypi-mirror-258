import unittest
from datetime import date

from flysearch.trip import Trip


class TestFlightOffer(unittest.TestCase):
    def test_from_dict(self):
        test_data = {
            "Panstwo": "TestCountry",
            "Nazwa": "TestName",
            "Klucz": "TestKey",
            "TerminWyjazdu": "2024-05-01T00:00:00Z",
            "Cena": 1000,
            "DataLayerV4": {"currency": "USD"},
        }
        expected_result = Trip(
            country="TestCountry",
            key="TestKey",
            departure_date=date(2024, 5, 1),
            price=1000,
            currency="USD",
        )
        result = Trip.from_dict(test_data)
        self.assertEqual(result, expected_result)
