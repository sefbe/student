#  Housing Platform - README

## **Introduction**
Ce projet est une plateforme de gestion de logements étudiants développée en utilisant 
une architecture basée sur des microservices. Elle permet aux utilisateurs (propriétaires
et locataires) de publier et de réserver des logements, de gérer les paiements, et d'effectuer
des recherches avancées.

---

## **Fonctionnalités**
1. **Gestion des utilisateurs :**
   - Inscription et connexion des utilisateurs (propriétaires et locataires).
   - Gestion des profils utilisateurs.
   - Authentification sécurisée avec gestion des rôles (JWT).

2. **Gestion des logements :**
   - Publication des annonces par les propriétaires.
   - Ajout des chambres aux annonces (images principales et secondaires).

3. **Gestion des réservations :**
   - Réservation des logements par les locataires.
   - Gestion des statuts des logements (disponible, réservé, loué).

4. **Paiements :**
   - Simulation d'intégration avec des solutions de paiement telles qu'Orange Money et MTN MoMo.

5. **API Gateway :**
   - Orchestration des services et présentation d'une interface utilisateur centralisée.

---

## **Structure du Projet**
```plaintext

housing/
├── apigateway/
│   ├── app/
│   │   ├── templates/                     # Contient les fichiers HTML
│   │   ├── static/                        # Contient les assets (CSS, JS, images)
│   │   │   ├── css/
│   │   │   │   ├── style.css              # Fichier de styles global
│   │   │   │   └── bootstrap.min.css      # Bootstrap
│   │   │   ├── js/
│   │   │   │   ├── script.js              # Scripts personnalisés
│   │   │   │   └── bootstrap.bundle.min.js # Bootstrap JS
│   │   │   ├── images/
│   │   │   │   ├── logo.png               # Logo du site
│   │   │   │   └── room1.jpg              # Exemples d'images de chambres
│   │   ├── __init__.py
│   │   ├── routes.py                      # Routes gérant les requêtes et les pages
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   └── gateway_utils.py           # Utilitaires pour le Gateway
│   │   └── config.py                      # Configuration de l'API Gateway
│   ├── run.py                             # Point d'entrée pour l'API Gateway
│   ├── requirements.txt                   # Dépendances pour l'API Gateway
│   └── Dockerfile                         # Fichier Docker pour l'API Gateway
├── user_service/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models.py                      # Modèle des utilisateurs (Users)
│   │   ├── routes.py                      # Routes pour la gestion des utilisateurs
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   └── token_utils.py             # Gestion des tokens JWT
│   ├── config.py
│   ├── run.py
│   ├── requirements.txt
│   ├── migrations/                        # Gestion des migrations avec Flask-Migrate
│   └── Dockerfile
├── room_service/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models.py                      # Modèle des chambres (Rooms)
│   │   ├── routes.py                      # Routes pour la gestion des chambres
│   │   ├── utils/
│   │       ├── __init__.py
│   │       └── image_utils.py             # Gestion des images
│   ├── config.py
│   ├── run.py
│   ├── requirements.txt
│   ├── migrations/
│   └── Dockerfile
├── reservation_service/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models.py                      # Modèle des réservations (Reservations)
│   │   ├── routes.py                      # Routes pour la gestion des réservations
│   ├── config.py
│   ├── run.py
│   ├── requirements.txt
│   ├── migrations/
│   └── Dockerfile
├── payment_service/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models.py                      # Modèle des paiements (Payments)
│   │   ├── routes.py                      # Routes pour la gestion des paiements
│   ├── config.py
│   ├── run.py
│   ├── requirements.txt
│   ├── migrations/
│   └── Dockerfile
├── docker-compose.yml                     # Fichier Docker Compose pour orchestrer les services
└── README.md                              # Documentation du projet

```

---

## **PRÉREQUIS**
- **SYSTÈME D'EXPLOITATION :** Linux, macOS, ou Windows.
- **Docker :** Version 20.10+ 
- **Docker Compose :** Version 2.0+ 

---

## **Installation et Lancement**
1. Dézipper :
 - décompressé le dossier zipper.
 - Ouvrez un terminal et exécutez la commandes suivante :
       cd housing

2. **Lancez le projet avec Docker Compose :**
   une fois dans /housing lancer le projet en executant cette commande:
   
        docker-compose up --build
   

3. **Accédez à l'application :**
   - Une fois que Docker Compose a démarré tous les services, accédez à l'application
    via un navigateur web en utilisant l'URL et le port configurés dans docker-compose.yml
    (http://localhost:5000).
   - API Gateway : [http://localhost:5000] ou (http://127.0.0.1:5000)



## **Fonctionnement**
### **Services**
1. **API Gateway :**
   - Point d'entrée principal de l'application.
   - Présente l'interface utilisateur pour accéder aux fonctionnalités.

2. **User Service :**
   - Gère les utilisateurs, l'inscription, et l'authentification.

3. **Room Service :**
  - Gère l'ajout, la suppression et la mise à jour des chambres libérées.
  - Permet aux locataires de suivre le statut de leurs chambres dans la section "Mes Chambres".
  - Le bouton "Supprimer" n'apparaît que si l'utilisateur est à la fois locataire et propriétaire de la chambre.
  - seuls jpg et png formats des images sont acceptés

4. **Reservation Service :**
 - Gère les réservations et les statuts des logements (disponible, réservé, loué).
 - Permet le suivi des chambres réservées.
 - Remet automatiquement à disposition les chambres réservées depuis plus de 72 heures sans location.

5. **Payment Service :**
 - Gère uniquement l'assimilation des paiements via Orange Money et MTN MoMo.
 - Prend en compte Visa et MasterCard, mais ces options ne sont pas encore gérées.


### **Base de Données**
Les services utilisent des bases de données MySQL distinctes :
- `user_service_db` : Stocke les données des utilisateurs.
- `rooms_db` : Stocke les informations des logements.
- `reservation_db` : Stocke les réservations.
- `payment_db` : Stocke les paiements.


## Arrêter les services sans supprimer les conteneurs
 Dans le même terminal où docker-compose up est en cours d'exécution :
 - Appuyez sur Ctrl + C pour arrêter les services en cours.
 - Pour arrêter les conteneurs si le terminal a été fermé :
 - Exécutez la commande suivante dans le répertoire contenant le fichier docker-compose.yml :
        docker-compose stop
 - Relancez:
        docker-compose up
## LE DOSSIER :SCREENSHOTS_WEBSITE
Contient quelques captures d'écran du site web.
---




