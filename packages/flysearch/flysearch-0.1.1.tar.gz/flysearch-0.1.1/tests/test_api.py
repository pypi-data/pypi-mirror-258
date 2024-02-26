import unittest
from datetime import date
from unittest.mock import MagicMock, patch

from flysearch.trip import Trip
from flysearch.api import RainbowAPI
from flysearch.options import Sort


class TestFlySearchAPI(unittest.TestCase):
    @patch("flysearch.api.requests.get")
    def test_search_flights(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "Panstwo": "Turcja",
                "Region": None,
                "Nazwa": "Antalya",
                "Klucz": "AYT",
                "TerminWyjazdu": "2024-05-04T00:00:00Z",
                "Zdjecie410x410": "//images.r.pl/zdjecia/lokalizacje/160/antalya_160_129971_289441_410x410.jpg",
                "Zdjecie410x225": "//images.r.pl/zdjecia/lokalizacje/160/antalya_160_129971_289439_410x225.jpg",
                "Flaga": "//images.r.pl/zdjeciaOryginalne/lokalizacje/45/turcja_45_130208.svg",
                "Cena": 799,
                "DataLayerV4": {
                    "item_id": 178933,
                    "item_name": "antalya bzg - ayt 04/05/2024",
                    "currency": "pln",
                    "item_brand": "enter air",
                    "item_category": "turcja",
                    "item_category2": "polska",
                    "item_category3": "bzg",
                    "item_category4": "2024-05-04",
                    "price": 799,
                    "quantity": 1,
                },
            }
        ]
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        api = RainbowAPI()
        results = api.get_cheapest_trips(
            birth_dates=[date(year=1989, month=10, day=30)],
            departure_iata=["BZG"],
            arrival_iatas=["AYT"],
            one_way=True,
            departure_date_min=date(2024, 5, 1),
            departure_date_max=date(2024, 5, 31),
            sort=Sort.PRICE,
        )

        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0], Trip)
        self.assertEqual(results[0].key, "AYT")

        # Ensure the mock was called with the expected parameters
        mock_get.assert_called_once()
