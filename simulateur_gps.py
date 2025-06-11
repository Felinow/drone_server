import requests
import time

url = "https://drone-server-m3nw.onrender.com/receive"

# Liste de points GPS simulés (comme si tu te déplaçais)
donnees = [
    {"latitude": -4.3210, "longitude": 15.3120},
    {"latitude": -4.3212, "longitude": 15.3123},
    {"latitude": -4.3215, "longitude": 15.3125},
    {"latitude": -4.3217, "longitude": 15.3129},
    {"latitude": -4.3220, "longitude": 15.3132},
]

# Envoi de chaque point avec 2 secondes d'intervalle
for point in donnees:
    data = {
        "latitude": point["latitude"],
        "longitude": point["longitude"],
        "altitude": 45.0,
        "speed": 8.5,
        "mode": "GUIDED"
    }
    response = requests.post(url, json=data)
    print("Envoyé :", data, "| Réponse :", response.json())
    time.sleep(2)
