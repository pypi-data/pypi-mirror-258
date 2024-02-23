import requests
import tldextract


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
        url = f"{self.base_url}{domain}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return self.parse_response(response.json())
        elif response.status_code == 403:
            return f"Invalid username, password or API key: {response.status_code}"
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

    def read_domains_from_file(self, file_path):
        self.results = []
        with open(file_path, 'r') as file:
            for line in file:
                domain, *category = line.strip().split()
                category = ' '.join(category)
                extracted = tldextract.extract(domain)
                if not extracted.subdomain and extracted.suffix:
                    self.domain, self.prediction = self.get(domain)
                    self.results.append((self.domain, self.prediction))
                else:
                    print(f"'{domain}' is not a valid domain.")