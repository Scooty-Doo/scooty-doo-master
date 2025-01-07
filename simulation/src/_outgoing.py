import json
from typing import Union, List, Dict
import httpx
from src.utils.settings import Settings

def _url(url, endpoint):
    return f'{url.rstrip("/")}/{endpoint.lstrip("/")}'

BACKEND_URL = 'http://api:8000/'
HIVEMIND_URL = 'http://bike_hivemind:8001/'

class Outgoing:
    def __init__(self, token: str):
        self.endpoints = Settings.Endpoints()
        self.backend_url = BACKEND_URL
        self.hivemind_url = HIVEMIND_URL
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}',
        }
        self.trips = Trips(self.backend_url, self.headers)
        self.bikes = Bikes(self.hivemind_url, self.headers)

class Trips:
    def __init__(self, backend_url, headers):
        self.endpoints = Settings.Endpoints()
        self.backend_url = backend_url
        self.headers = headers

    async def start_trip(self, user_id: int, bike_id: int):
        url = _url(self.backend_url, "/v1/trips/")
        payload = {
            "user_id": user_id,
            "bike_id": bike_id
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=self.headers, data=json.dumps(payload), timeout=10.0)
                response.raise_for_status()
                print(response.json())
                return response.json()
            except httpx.RequestError as e:
                raise httpx.RequestError(f"Failed to start trip: {e}") from e

    async def end_trip(self, trip_id: int, user_id: int, bike_id: int, maintenance: bool = False, ignore_zone: bool = True):
        url = _url(self.backend_url, f"/v1/trips/{trip_id}")
        payload = {
            "user_id": user_id,
            "bike_id": bike_id,
            "maintenance": maintenance,
            "ignore_zone": ignore_zone
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.patch(url, headers=self.headers, data=json.dumps(payload), timeout=10.0)
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                raise httpx.RequestError(f"Failed to end trip: {e}") from e

class Bikes:
    def __init__(self, hivemind_url, headers):
        self.endpoints = Settings.Endpoints()
        self.hivemind_url = hivemind_url
        self.headers = headers

    async def move(self, bike_id: int, position_or_linestring: Union[tuple, List[tuple]]):
        url = _url(self.hivemind_url, f"/v1/move?bike_id={bike_id}")
        payload = {
            "position_or_linestring": position_or_linestring
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=self.headers, data=json.dumps(payload), timeout=10.0)
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                raise httpx.RequestError(f"Failed to move bike: {e}") from e
