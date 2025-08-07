import requests
import os

EMAIL_ADMIN = "qJ4jYO8m7DKsyxgMOBZL+b7qz+h6M9gPMd9Sfm9BMW2p+iEziyIHmBucyq3tXL74jHWeX8yNvCPE6A20w+TtUyvVofZ8trtGM5Z8hghTxJj4FogKc0d1BBHnH5KUdquEVhl/khC+u0TGvdhCXXnzQqhQsjZ7ZZX6OZzlczbGs4BF4aa9IX5p7r2F9D3m0PWSp1B4164FtoDBPbhVy6IhKXvsg6otwv+NdeAd8unZYnEscGc6wWWuaRWnOVElDlyOm20NepjgscJZLAlnRwzI98iwtEiaXc0HdbE+086gz7GO0NdYHjwuGOISTH9QgLq1+yzOL0jx1jO5iJvX010fpw=="
PWSD_ADMIN = "AYNBUxSqBSuGq30HFweieMz2Aw9sgbgG9Je3LmYA504jf8YFh4S5UuZlA7slFJzPkburxHlioxoexd9ePfz9nlQrsUv9+DDIIH+qJjIyeErpQqCb6aWJKif8DhX3YdDkoyqu/s42M6j42XDFKmyuTNGkOBMt9hdl1A8kgP0TR5DJ4LG4Spt43gaJKpq9Eyi7Rj01d8VSENvi1Is0WT2X1U/SrX1hHfyKZNhAp3avxVCwIlBkjWl1ZqenZcqolxVJZp1CW/mrPDY8lUs+UHrGdTaKxRHPbH/4AYJydDe3grR970EqToK7aAXi8o2ivaiZrf6vjYWvRi/nUlcOhzGJgQ==" #os.environ["PWSD_ADMIN"]
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


