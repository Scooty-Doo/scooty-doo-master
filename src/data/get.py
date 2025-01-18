import httpx
from ..utils.settings import Settings
from ..utils.file import File

def _url(url, endpoint):
    return f'{url.rstrip("/")}/{endpoint.lstrip("/")}'

def _extract_data_from_response_json(data):
    """Extracts the 'data' key from the response.json() that has JSON:API formatting."""
    return data['data']

class Get:
    def __init__(self):
        self.endpoints = Settings.Endpoints()
        self.url = self.endpoints.backend_url
        self.token = Settings.Endpoints.token
        self.data_folder = Settings.Directory.data
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}',
        }

    async def _get_data(self, url, filename, save_to_json, limit=9999):
        """Generic method to GET data asynchronously."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params={"limit": limit}, headers=self.headers, timeout=20.0)
                response.raise_for_status()
                result = _extract_data_from_response_json(response.json())
                if save_to_json:
                    await File.Save.to_json(data=result, folder=self.data_folder, filename=filename)
                return result
            except httpx.RequestError as e:
                raise httpx.RequestError(f"Failed to request {filename[:-5]}: {e}") from e

    async def bikes(self, save_to_json=True, limit=9999):
        url = _url(self.url, self.endpoints.Bikes.get_all)
        return await self._get_data(url, 'bikes.json', save_to_json, limit)

    async def trips(self, save_to_json=True, limit=9999):
        url = _url(self.url, self.endpoints.Trips.get_all)
        return await self._get_data(url, 'trips.json', save_to_json, limit)

    async def users(self, save_to_json=True, limit=9999):
        url = _url(self.url, self.endpoints.Users.get_all)
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params={"limit": limit, "is_eligable": True}, headers=self.headers, timeout=20.0)
                response.raise_for_status()
                result = _extract_data_from_response_json(response.json())
                if save_to_json:
                    await File.Save.to_json(data=result, folder=self.data_folder, filename="users.json")
                return result
            except httpx.RequestError as e:
                raise httpx.RequestError(f"Failed to request: {e}") from e

    async def zones(self, save_to_json=True, limit=9999):
        url = _url(self.url, self.endpoints.Zones.get_all)
        return await self._get_data(url, 'zones.json', save_to_json, limit)

    async def zone_types(self, save_to_json=True, limit=9999):
        url = _url(self.url, self.endpoints.Zones.get_types)
        return await self._get_data(url, 'zone_types.json', save_to_json, limit)
