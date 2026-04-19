import requests

print("=== TEST DES PAGES PRODUITS ===")

routes = ['/page5', '/page7', '/page8']

for route in routes:
    try:
        print(f"\nTest de {route}:")
        r = requests.get(f'http://127.0.0.1:5000{route}')
        print(f"  Status: {r.status_code}")
        if r.status_code == 200:
            print(f"  Content length: {len(r.text)}")
            # Chercher des signes de produits dans le HTML
            if 'product-card' in r.text:
                print("  ✓ Produits trouvés dans le HTML")
            else:
                print("  ✗ Aucun produit trouvé dans le HTML")
        else:
            print(f"  Erreur HTTP: {r.status_code}")
    except Exception as e:
        print(f"  Erreur: {e}")