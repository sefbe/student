import requests

def forward_request(service_url, endpoint, method="GET", data=None):
    try:
        url = f"{service_url}{endpoint}"
        if method == "POST":
            response = requests.post(url, json=data)
        else:
            response = requests.get(url, params=data)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la communication avec {service_url}{endpoint}: {e}")
        return None

