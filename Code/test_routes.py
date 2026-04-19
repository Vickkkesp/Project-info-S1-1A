import requests

# Tester les routes
routes = ['/page5', '/page7', '/page8']

for route in routes:
    try:
        r = requests.get(f'http://127.0.0.1:5000{route}')
        print(f'{route}: Status {r.status_code}')
    except Exception as e:
        print(f'{route}: Error {e}')