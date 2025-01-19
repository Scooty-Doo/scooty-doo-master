# pylint: disable=import-error, no-name-in-module, too-few-public-methods
"""Outgoing requests to backend and hivemind."""

import json
from typing import Union, List
import httpx
from src.utils.settings import Settings

def _url(url, endpoint):
    """Concatenate url and endpoint."""
    return f'{url.rstrip("/")}/{endpoint.lstrip("/")}'

BACKEND_URL = 'http://api:8000/'
HIVEMIND_URL = 'http://bike_hivemind:8001/'

class Outgoing:
    """Outgoing requests to backend and hivemind."""
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
    """Outgoing requests to backend for trips."""
    def __init__(self, backend_url, headers):
        self.endpoints = Settings.Endpoints()
        self.backend_url = backend_url
        self.headers = headers

    async def start_trip(self, user_id: int, bike_id: int, token: str):
        """Start a trip for a user on a bike."""
        url = _url(self.backend_url, "/v1/trips/")
        payload = {
            "bike_id": bike_id
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers={
                            'Content-Type': 'application/json',
                            'Authorization': f'Bearer {token}',
                }, data=json.dumps(payload))
                response.raise_for_status()
                print(f"Succesfully started trip for user {user_id} on bike {bike_id}")
                return response.json()
            except httpx.RequestError as e:
                print(f"Failed to start trip for url: {url}")
                raise httpx.RequestError(f"Failed to start trip: {e}") from e

    async def end_trip(self, user_id: int, bike_id: int, trip_id: int, token: str):
        """End a trip for a user on a bike."""
        url = _url(self.backend_url, f"/v1/trips/{trip_id}")
        payload = {
            "bike_id": bike_id
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.patch(url, headers={
                            'Content-Type': 'application/json',
                            'Authorization': f'Bearer {token}',
                }, data=json.dumps(payload))
                response.raise_for_status()
                print(f"Succesfully ended trip for user {user_id} on bike {bike_id}")
                return response.json()
            except httpx.RequestError as e:
                print(f"Failed to end trip for url: {url}")
                raise httpx.RequestError(f"Failed to end trip: {e}") from e

class Bikes:
    """Outgoing requests to hivemind for bikes."""
    def __init__(self, hivemind_url, headers):
        self.endpoints = Settings.Endpoints()
        self.hivemind_url = hivemind_url
        self.headers = headers

    async def move(self, bike_id: int, position_or_linestring: Union[tuple, List[tuple]]):
        """Move a bike to a position or along a linestring."""
        url = _url(self.hivemind_url, "/move")
        payload = {
            "position_or_linestring": position_or_linestring
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url, params={"bike_id": bike_id},
                    headers=self.headers, data=json.dumps(payload))
                response.raise_for_status()
                print(f"Succesfully moved bike {bike_id}")
                return response.json()
            except httpx.RequestError as e:
                print(f"Failed to move bike for url: {url}")
                raise httpx.RequestError(f"Failed to move bike: {e}") from e
