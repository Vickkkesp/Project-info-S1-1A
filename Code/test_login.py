#!/usr/bin/env python3
# Test de la fonction login
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app

def test_login():
    with app.test_client() as client:
        # Test avec les identifiants admin
        print("Test de connexion admin...")
        response = client.post('/login', data={'email': 'nathan.assens@gmail.com', 'password': 'kk'})
        print(f'Status code: {response.status_code}')
        print(f'Location: {response.headers.get("Location", "None")}')
        if response.status_code == 302 and '/admin' in response.headers.get('Location', ''):
            print('✓ Test admin réussi')
        else:
            print('✗ Test admin échoué')

        # Test avec un utilisateur normal
        print("\nTest de connexion utilisateur...")
        response = client.post('/login', data={'email': 'jean.martin1@mail.com', 'password': 'mdp1'})
        print(f'Status code: {response.status_code}')
        print(f'Location: {response.headers.get("Location", "None")}')
        if response.status_code == 302 and '/dashboard' in response.headers.get('Location', ''):
            print('✓ Test utilisateur réussi')
        else:
            print('✗ Test utilisateur échoué')

if __name__ == '__main__':
    test_login()

