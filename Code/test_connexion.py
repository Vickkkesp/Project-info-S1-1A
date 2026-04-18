import sqlite3

def test_connexion(email, password):
    conn = sqlite3.connect('ProjetBdd1.db')
    cursor = conn.cursor()

    # Test de la requête de connexion
    cursor.execute(
        "SELECT * FROM utilisateurs WHERE email=? AND password=?",
        (email, password)
    )
    user = cursor.fetchone()

    print(f"Test connexion pour {email}")
    print(f"Résultat: {user}")

    if user:
        print("✅ Connexion réussie!")
        print(f"ID utilisateur: {user[0]}")
    else:
        print("❌ Identifiants incorrects")

        # Vérifier si l'email existe
        cursor.execute("SELECT * FROM utilisateurs WHERE email=?", (email,))
        user_by_email = cursor.fetchone()
        if user_by_email:
            print(f"Email trouvé: {user_by_email}")
            print(f"Password stocké: '{user_by_email[4]}'")
            print(f"Password saisi: '{password}'")
            print(f"Match: {user_by_email[4] == password}")
        else:
            print("Email non trouvé dans la base")

    conn.close()

if __name__ == "__main__":
    # Test avec les identifiants de l'utilisateur
    test_connexion("anais.tobaty@gmail.com", "123")