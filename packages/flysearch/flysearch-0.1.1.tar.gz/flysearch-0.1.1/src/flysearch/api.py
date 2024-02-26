from datetime import date
from enum import Enum
from typing import Dict, List, Optional

import requests

from .trip import Trip
from .options import Sort


class RainbowAPI:
    API_BASE_URL = "https://biletyczarterowe.r.pl/api/wyszukiwanie/wyszukajDataLayerV4"

    def __init__(self):
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "cache-control": "no-cache",
            "pragma": "no-cache",
        }

    def _format_date_for_api(self, date_obj: Optional[date]) -> str:
        """Formats a datetime.date object into a string suitable for the API."""
        if date_obj is None:
            return ""
        return date_obj.strftime("%Y-%m-%d")

    def get_cheapest_trips(
        self,
        birth_dates: List[date],
        departure_iata: Optional[List[str]],
        arrival_iatas: Optional[List[str]],
        one_way: bool = False,
        departure_date_min: Optional[date] = None,
        departure_date_max: Optional[date] = None,
        sort: Sort = Sort.PRICE,
    ) -> List[Dict[str, str]]:
        """
        Searches for flights based on the given criteria.

        :param birth_dates: List of birth dates for each passenger.
        :param departure_iata: List of departure IATA codes, searches from any location if None.
        :param arrival_iatas: List of arrival IATA codes, searches to any location if None.
        :param one_way: Specifies if only one-way tickets should be searched.
        :param departure_date_min: The minimum departure date for flights. If None, no minimum constraint is applied.
        :param departure_date_max: The maximum departure date for flights. If None, no maximum constraint is applied.
        :param sort: The sorting option for flight search results.
        :return: A list of dictionaries, each representing a flight offer.
        """

        # Validate the provided dates
        if (
            departure_date_min
            and departure_date_max
            and departure_date_min > departure_date_max
        ):
            raise ValueError(
                "departure_date_min must be before or equal to departure_date_max"
            )

        # by default the search is performed only for one passenger
        formatted_birth_dates = [
            self._format_date_for_api(date) for date in birth_dates
        ]

        params = {
            "oneWay": str(one_way).lower(),
            "dataUrodzenia[]": formatted_birth_dates,
            "dataWylotuMin": self._format_date_for_api(departure_date_min),
            "dataWylotuMax": self._format_date_for_api(departure_date_max),
            "dataPrzylotuMin": "",
            "dataPrzylotuMax": "",
            "sortowanie": sort.value,
        }
        if departure_iata is not None:
            params["iataSkad[]"] = departure_iata
        if arrival_iatas is not None:
            params["iataDokad[]"] = arrival_iatas

        response = requests.get(self.API_BASE_URL, params=params, headers=self.headers)
        response.raise_for_status()  # Raises a HTTPError if the response was an error

        data = response.json()
        if data is None:
            return []

        return [Trip.from_dict(flight_offer_dict) for flight_offer_dict in data]
