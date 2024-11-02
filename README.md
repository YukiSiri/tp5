# TP 5 : Création d'une API avec FastAPI

## Objectif

Dans ce TP, vous allez concevoir une API basique avec FastAPI qui comporte des fonctionnalités pour réaliser des calculs simples et pour gérer des listes TODO associées à des utilisateurs.

**Voici les fonctionnalités à développer** :

1. **Calcul basique** : Une route permettant d'effectuer une addition avec des paramètres fournis dans l'URL.
2. **Gestion de listes TODO par utilisateur** :
    - Création d'utilisateurs avec gestion d'authentification.
    - Chaque utilisateur peut gérer ses propres listes TODO (ajout, suppression, modification).

Vous êtes libres d’utiliser une base de données (comme SQLite ou Postgres) ou de stocker les données en mémoire. Assurez-vous que l’application est fonctionnelle dès son démarrage en initialisant la base de données si nécessaire.

---

## Étapes et Routes à Implémenter

### Partie 1 : Routes de Calcul Simple

- **Route** : `GET /`
    - **Description** : Retourne un code 200 et un objet JSON vide.
    - **Objectif** : Testez l'installation et le fonctionnement de votre serveur FastAPI.
    - Ce code est fourni.

- **Route** : `GET /miscellaneous/addition`
    - **Description** : Prend deux paramètres `a` et `b` via des [query parameters](https://fastapi.tiangolo.com/tutorial/query-params/#query-parameters) et retourne leur somme.
    - **Exigences** : `a` et `b` doivent être des nombres, et la route doit gérer les erreurs de type si les paramètres fournis ne sont pas valides.

### Partie 2 : Gestion des Utilisateurs et Authentification

Une fois la première partie terminée, vous allez étendre l'API pour gérer une liste de tâches (TODO) par utilisateur, avec authentification.

#### Routes Utilisateur

- **Route** : `POST /users`
    - **Description** : Permet de créer un utilisateur avec les informations suivantes dans le body de la requête [(voir ici pour les détails)](https://fastapi.tiangolo.com/tutorial/body/).
    - **Exemple de payload** :
      ```json
      {
        "username": "user1",
        "password": "password123"
      }
      ```
    - **Exigences** : Vérifier l'unicité du nom d'utilisateur pour éviter les doublons.

- **Route** : `POST /token` et `GET /users/me`
    - **Description** : Utiliser [OAuth2 et JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt) pour sécuriser les routes utilisateur. Consultez aussi [ce guide d'introduction](https://fastapi.tiangolo.com/tutorial/security/) pour une vue d'ensemble.
    - **Exigences** :
        - `POST /token` doit gérer l'authentification via JWT.
        - `GET /users/me` doit retourner uniquement le nom de l'utilisateur et le nombre de TODO enregistrés.
        - Les routes TODO doivent être accessibles uniquement aux utilisateurs authentifiés ; sinon, une réponse 401 doit être renvoyée.

#### Routes de Gestion des TODO

Les routes suivantes doivent permettre aux utilisateurs de gérer leurs listes TODO :

- **Route** : `POST /users/me/todo`
    - **Description** : Permet de créer un nouvel élément TODO pour l'utilisateur authentifié.
    - **Exemple de payload** :
      ```json
      {
        "name": "Acheter du lait",
        "description": "Aller au supermarché pour acheter du lait",
        "priority": 1
      }
      ```
    - **Exigences** :
        - Chaque TODO doit être attribué à un ID unique.
        - La priorité doit permettre de trier les TODO dans les requêtes de récupération.

- **Route** : `GET /users/me/todo`
    - **Description** : Retourne tous les TODO de l'utilisateur, triés par priorité (de la plus petite à la plus grande).

- **Route** : `PATCH /users/me/todo/:id/`
    - **Description** : Permet de modifier un TODO existant.
    - **Exigences** : Retourne une erreur 404 si le TODO n'existe pas.

- **Route** : `DELETE /users/me/todo/:id`
    - **Description** : Permet de supprimer un TODO.
    - **Exigences** : Retourne une erreur 404 si le TODO n'existe pas.

---

## Structure de Dossier Recommandée

Organisez votre projet avec la structure suivante :

```
├── api
│   ├── __init__.py
│   ├── business         # Contient la logique métier, ex: création utilisateur, gestion des TODO
│   │   └── __init__.py
│   └── model            # Contient les modèles de données (ex: User, TODO)
│       └── __init__.py
```

---

## Tests et Dépendances

Installez les packages nécessaires pour les tests avec :

```bash
pip install pytest httpx
```

Le fichier de test sera disponible le jour du TP.
Néanmoins, vous pouvez tester votre projet avec le fichier test.http (utilisable via PyCharm/Intellij).

## Avant de commencer

Le projet se base énormément sur la documentation de FastAPI, prenez le temps de bien lire celle-ci.
Commencez simple, gardez l'authentification pour la fin si vous n'êtes pas à l'aise.