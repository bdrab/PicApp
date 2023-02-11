import requests
from getpass import getpass

auth_endpoint = "http://192.168.0.136/api/v1/auth/"
password = getpass()

auth_response = requests.post(auth_endpoint, json={"username": "bartek", "password": password})

token = auth_response.json()["token"]
print(token)

endpoint = "http://192.168.0.136/api/v1/"
get_response = requests.get(endpoint, headers = {"Authorization": f"Bearer {token}"})
print(get_response)

