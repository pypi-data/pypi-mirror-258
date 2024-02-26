import requests
from typing import Optional, Dict, Any

class ChannelAdvisorClient:
    def __init__(self, access_token, default_profile_id, secondary_profile_id=None, base_url="https://api.channeladvisor.com"):
        self.base_url = base_url
        self.access_token = access_token
        self.default_profile_id = default_profile_id
        self.secondary_profile_id = secondary_profile_id
    
    def make_request(self, endpoint: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, Any]] = None, method: str = "GET", data: Optional[Dict[str, Any]] = None) -> requests.Response:
        headers = headers or {"Content-Type": "application/json"}
        headers.update({"Authorization": f"Bearer {self.access_token}"})

        url = f"{self.base_url}/{endpoint}"
        response = requests.request(method, url, params=params, headers=headers, data=data)
        return response