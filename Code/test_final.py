import requests
import time

print("=== TEST DES PAGES PRODUITS ===")

# Attendre que l'application démarre
time.sleep(2)

routes = [
    ('/page5', 'Bagues'),
    ('/page7', 'Colliers'),
    ('/page8', 'Montres'),
    ('/page6', 'Boucles')
]

for route, name in routes:
    try:
        print(f"\nTest de {route} ({name}):")
        r = requests.get(f'http://127.0.0.1:5000{route}')
        print(f"  Status: {r.status_code}")
        if r.status_code == 200:
            content = r.text
            print(f"  Content length: {len(content)}")
            # Chercher des signes de produits dans le HTML
            if 'product-card' in content:
                print("  ✓ Produits trouvés dans le HTML")
                # Compter le nombre de cartes produit
                card_count = content.count('product-card')
                print(f"  Nombre de cartes produit: {card_count}")
            else:
                print("  ✗ Aucun produit trouvé dans le HTML")
                # Montrer un extrait du HTML pour déboguer
                print(f"  Extrait HTML: {content[content.find('<div class=\"product-grid\">'):content.find('<div class=\"product-grid\">')+200]}...")
        else:
            print(f"  Erreur HTTP: {r.status_code}")
    except Exception as e:
        print(f"  Erreur: {e}")

print("\n=== FIN DES TESTS ===")