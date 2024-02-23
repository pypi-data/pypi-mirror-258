import requests


class Secweb:
    def __init__(self, username='', password='', api_key=''):
        self.api_key = api_key
        self.base_url = f"https://secwe.pythonanywhere.com/api/predict/"
        self.headers = {
            "X-User": username,
            "X-Pass": password,
            "Authorization": f"{self.api_key}",
        }

        self.domain = None
        self.prediction = None

        self.response = None

    def get(self, domain):
        self.base_url = f"{self.base_url}{domain}"
        response = requests.get(self.base_url, headers=self.headers)
        if response.status_code == 200:
            return self.parse_response(response.json())
        elif response.status_code == 403:
            return f"Invalid username, password or API key: {response.status_code}"
        else:
            return f"Request failed with status code {response.status_code}"

    def post(self, data):
        response = requests.post(self.base_url, headers=self.headers, json=data)
        if response.status_code == 201:
            return response.json()
        else:
            return f"Request failed with status code {response.status_code}"

    def put(self, data):
        response = requests.put(self.base_url, headers=self.headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Request failed with status code {response.status_code}"

    def delete(self):
        response = requests.delete(self.base_url, headers=self.headers)
        if response.status_code == 204:
            return "Successfully deleted"
        else:
            return f"Request failed with status code {response.status_code}"

    def parse_response(self, response):
        if isinstance(response, dict):
            try:
                self.domain = response['domain']
                self.prediction = response['prediction']
                return self.domain, self.prediction
            except KeyError:
                return "Invalid response format"
        else:
            return "Response is not a dictionary"