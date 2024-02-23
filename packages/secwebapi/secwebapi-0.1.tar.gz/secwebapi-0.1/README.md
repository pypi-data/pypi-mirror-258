# secwebapi

## Description

`secwebapi` is a Python package designed to interact with the Secweb API. It provides a simple and intuitive interface for sending requests and processing responses from the API.

## Installation

To install `secwebapi`, you need to have Python installed on your system. If you don't have Python installed, you can download it from the official website.

Once Python is installed, you can install `secwebapi` by cloning the repository and running the setup script:

```bash
git clone https://github.com/sametazaboglu/secwebapi.git
cd secwebapi
pip install .
```
## Example Usage
Here is a basic example of how to use `secwebapi`:
```python
import secwebapi

# Initialize the API with your credentials
secweb_client = secwebapi.Secweb(username='your_username',
                       password='your_password',
                       api_key='your_api_key')

# Send a GET request to the API
data = secweb_client.get("example.com")

# Print the response
print(data)