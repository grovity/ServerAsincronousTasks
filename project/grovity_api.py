import requests
import os

EMAIL_ADMIN = os.environ["EMAIL_ADMIN"]
PWSD_ADMIN = os.environ["PWSD_ADMIN"] 
class ApiClient:
    def __init__(self, host, token):
        self.host = host
        self.token = token

    def handle_response(self, response):
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"Request Exception: {err}")

    def login(self):
        url = f"{self.host}/usuario/login"

        payload = {
            "email": EMAIL_ADMIN,
            "password": PWSD_ADMIN
        }

        response = requests.post(url, json=payload)

        return self.handle_response(response)

    def get_video_update_url(self,meeting_id):
        url = f"{self.host}/calendario/url_video_update/{meeting_id}/"

        headers = {
            "Authorization": f"Token {self.token}"
        }

        response = requests.get(url, headers=headers)

        return self.handle_response(response)

    def get_transcrip_status(self,meeting_id):
        url = f"{self.host}/calendario/url_transcrip_status/{meeting_id}/"

        headers = {
            "Authorization": f"Token {self.token}"
        }

        response = requests.get(url, headers=headers)

        return self.handle_response(response)


