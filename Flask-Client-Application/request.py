import requests

url = "http://127.0.0.1:8080/realms/master/protocol/openid-connect/token"
data = {
    "client_id": "FlaskClient",
    "client_secret": "9veEsbfCdrkTN1Mxx8bsqrkPkb8oWPwX",
    "grant_type": "password",
    "username": "user",
    "password": "user",
    "scope": "openid email profile compliance_high",
}

response = requests.post(url, data=data)

print(response.status_code)
print(response.json())
