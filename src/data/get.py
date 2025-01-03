import requests
from ..utils.settings import Settings
from ..utils.file import File
from ._fallback import Fallback

def _url(url, endpoint):
    return f'{url}/{endpoint}'

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

    def bikes(self, save_to_json=True, fallback=False):
        url = _url(self.url, self.endpoints.Bikes.get_all)
        try:
            response = requests.get(url, headers=self.headers, timeout=(5, 10))
            response.raise_for_status()
            result = _extract_data_from_response_json(response.json())
            if save_to_json:
                File.Save.to_json(data=result, folder=self.data_folder, filename='bikes.json')
            return result
        except requests.exceptions.RequestException as e:
            if fallback:
                result = Fallback.bikes(save_to_json=save_to_json)
                return result
            raise requests.exceptions.RequestException(f"Failed to request bikes: {e}") from e
    
    def trips(self, save_to_json=True, fallback=False):
        url = _url(self.url, self.endpoints.Trips.get_all)
        try:
            response = requests.get(url, headers=self.headers, timeout=(5, 10))
            response.raise_for_status()
            result = _extract_data_from_response_json(response.json())
            if save_to_json:
                File.Save.to_json(data=result, folder=self.data_folder, filename='trips.json')
            return result
        except requests.exceptions.RequestException as e:
            if fallback:
                result = Fallback.trips(save_to_json=save_to_json)
                return result
            raise requests.exceptions.RequestException(f"Failed to request zones: {e}") from e
        
    def users(self, save_to_json=True, fallback=False):
        url = _url(self.url, self.endpoints.Users.get_all)
        try:
            response = requests.get(url, headers=self.headers, timeout=(5, 10))
            response.raise_for_status()
            result = _extract_data_from_response_json(response.json())
            if save_to_json:
                File.Save.to_json(data=result, folder=self.data_folder, filename='users.json')
            return result
        except requests.exceptions.RequestException as e:
            if fallback:
                result = Fallback.users(save_to_json=save_to_json)
                return result
            raise requests.exceptions.RequestException(f"Failed to request zones: {e}") from e
        
    def zones(self, save_to_json=True, fallback=True):
        url = _url(self.url, self.endpoints.Zones.get_all)
        try:
            response = requests.get(url, headers=self.headers, timeout=(5, 10))
            response.raise_for_status()
            result = _extract_data_from_response_json(response.json())
            if save_to_json:
                File.Save.to_json(data=result, folder=self.data_folder, filename='zones.json')
            return result
        except requests.exceptions.RequestException as e:
            if fallback:
                result = Fallback.zones(save_to_json=save_to_json)
                return result
            raise requests.exceptions.RequestException(f"Failed to request zones: {e}") from e

    def zone_types(self, save_to_json=True, fallback=True):
        url = _url(self.url, self.endpoints.Zones.get_types)
        try:
            response = requests.get(url, headers=self.headers, timeout=(5, 10))
            response.raise_for_status()
            result = _extract_data_from_response_json(response.json())
            if save_to_json:
                File.Save.to_json(data=result, folder=self.data_folder, filename='zone_types.json')
            return result
        except requests.exceptions.RequestException as e:
            if fallback:
                result = Fallback.zone_types(save_to_json=save_to_json)
                return result
            raise requests.exceptions.RequestException(f"Failed to request zone types: {e}") from e
