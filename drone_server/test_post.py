import requests

url = "https://drone-server-m3nw.onrender.com/receive"

data = {
    "latitude": -4.454544677730422,
    "longitude": 15.289145579054477,
    "altitude": 45.2,
    "speed": 10.5,
    "mode": "GUIDED"
}

response = requests.post(url, json=data)

print("Réponse du serveur :", response.json())
