from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from app.forms import SignupForm, LoginForm, RoomForm
from app.utils import forward_request
from flask_login import current_user, login_required, login_user, logout_user
import requests
from app import load_user
from app.models import User
import base64  # Pour encoder/décoder les images en base64
from datetime import datetime, timedelta

app_bp = Blueprint('app_bp', __name__)





# URL de base du microservice réservation
RESERVATION_SERVICE_URL = "http://127.0.0.1:5003/reservations"
# URL du microservice room_service (l'adresse peut être différente selon votre environnement Docker ou local)
ROOM_SERVICE_URL = "http://127.0.0.1:5002"  # Adaptez l'URL en fonction de l'environnement

USER_SERVICE_URL = "http://127.0.0.1:5001"  # URL du microservice user_service
##@app_bp.route('/')
##def index():
##    # Affiche la page d'accueil
##    return render_template('index.html')

##@app_bp.route('/')
##def index():
##    rooms = []
##    show_add_room_button = False
##
##    # Récupération des chambres depuis le room_service
##    try:
##        response = requests.get(f"{ROOM_SERVICE_URL}/api/rooms/random")
##        if response.status_code == 200:
##            rooms = response.json()
##    except requests.RequestException:
##        flash("Erreur de connexion au service des chambres.", "danger")
##
##    # Récupérer le token depuis les en-têtes de la requête
##    token = request.headers.get("Authorization")
##    print(f"le token est: {token}")
##
##    if not token:
##        try:
##            user_status_response = requests.get(
##                f"{USER_SERVICE_URL}/api/users/status",
##                headers={"Authorization": token}
##            )
##            if user_status_response.status_code == 200:
##                user_data = user_status_response.json()
##                show_add_room_button = user_data.get('status') == 'propriétaire'
##            else:
##                flash("Erreur lors de la récupération du statut utilisateur.", "danger")
##        except requests.RequestException:
##            flash("Erreur de connexion au service utilisateur.", "danger")
##
##    return render_template('index.html', rooms=rooms, show_add_room_button=show_add_room_button)

# Route pour afficher les chambres aléatoires sur la page d'accueil






@app_bp.route('/')
def index():
    response = requests.get(f"{ROOM_SERVICE_URL}/api/rooms/random")
    if response.status_code == 200:
        rooms = response.json()  # Supposons que le microservice renvoie un tableau de chambres
    else:
        rooms = []
    
    # Vérifiez si l'utilisateur est connecté et s'il est un propriétaire
    if current_user.is_authenticated and current_user.status == 'proprietaire':  # Supposons que le rôle de l'utilisateur est 'owner'
        show_add_room_button = True
    else:
        show_add_room_button = False

    return render_template('index.html', rooms=rooms, show_add_room_button=show_add_room_button)


# Route pour afficher les détails d'une chambre
@app_bp.route('/room/<int:room_id>')
@login_required
def room_details(room_id):
    response = requests.get(f"{ROOM_SERVICE_URL}/api/rooms/{room_id}")
    if response.status_code == 200:
        room = response.json()
    else:
        flash("Chambre non trouvée", "danger")
        return redirect(url_for('app_bp.index'))
    return render_template('room_details.html', room=room)


# Route pour ajouter une chambre (seulement pour les propriétaires)
@app_bp.route('/add_room', methods=['GET', 'POST'])
@login_required
def add_room():
    form = RoomForm()
    if form.validate_on_submit():
        # Données pour la chambre (avec les images)
        room_data = {
            'title': form.title.data,
            'description': form.description.data,
            'price': form.price.data,
            'location': form.location.data,
            'distance': form.distance.data,
            'status': 'disponible',
            'owner_id': current_user.id,
            'images': []  # Liste pour stocker les images encodées
        }

        # Ajouter les images encodées en base64
        for file in form.images.data:
            if file:
                # Si file est un objet bytes, pas besoin de .read()
                if isinstance(file, bytes):
                    file_data = file  # Déjà sous forme de bytes
                    file_name = "image_bytes"  # Utilisez un nom générique pour les images en bytes
                else:
                    file_data = file.read()  # Si c'est un objet FileStorage, lire le contenu
                    file_name = file.filename  # Récupérer le nom du fichier si c'est un FileStorage

                # Encodage en base64
                encoded_image = base64.b64encode(file_data).decode('utf-8')
                room_data['images'].append({
                    "name": file_name,
                    "data": encoded_image
                })

        # Envoi de la chambre et des images au microservice
        response = requests.post(f"{ROOM_SERVICE_URL}/api/rooms", json=room_data)

        if response.status_code == 201:
            flash("Chambre ajoutée avec succès!", "success")
            return redirect(url_for('app_bp.index'))
        else:
            flash("Erreur lors de l'ajout de la chambre.", "danger")
    return render_template('add_room.html', form=form)



# Route pour supprimer une chambre (seulement pour le propriétaire)
@app_bp.route('/delete_room/<int:room_id>', methods=['POST'])
@login_required
def delete_room(room_id):
    response = requests.delete(f"{ROOM_SERVICE_URL}/api/rooms/{room_id}")
    if response.status_code == 200:
        flash('Chambre supprimée avec succès', 'success')
    else:
        flash('Erreur lors de la suppression de la chambre', 'danger')
    return redirect(url_for('app_bp.index'))



@app_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        data = {
            "username": form.username.data,
            "email": form.email.data,
            "password": form.password.data,
            "first_name": form.first_name.data,
            "last_name": form.last_name.data,
            "status": form.status.data
        }
        response = forward_request("http://127.0.0.1:5001", "/api/users/signup", method="POST", data=data)

        if response and response.status_code == 201:
            flash('Compte créé avec succès !', 'success')
            return redirect(url_for('.login'))
        else:
            flash('Erreur lors de la création du compte.', 'danger')
    return render_template('register.html', form=form)

from flask_login import login_user

@app_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = {
            "email": form.email.data,
            "password": form.password.data
        }
        response = forward_request("http://127.0.0.1:5001", "/api/users/login", method="POST", data=data)
        
        if response and response.status_code == 200:
            token = response.json().get("token")
            if token:
                session['token'] = token  # Stockez le token
                flash('Connexion réussie !', 'success')
                print(f"{token}")
                
                # Utilisez Flask-Login pour gérer l'authentification
                user_id = response.json().get("user_id")  # Assurez-vous que l'ID de l'utilisateur est dans la réponse
                
                user = load_user(user_id)  # Récupérer l'utilisateur via votre méthode
##                user = User(user_dic['id'], user_dic['username'], user_dic['email'], user_dic['first_name'], user_dic['last_name'], user_dic['status'])
                login_user(user)  # Connecter l'utilisateur
                clean_expired_reservations()
                check_user_reservation(current_user.id)
                return redirect(url_for('app_bp.index'))
        else:
            flash('Erreur de connexion. Veuillez vérifier vos identifiants.', 'danger')
    return render_template('login.html', form=form)

@app_bp.route('/logout')
def logout():
    logout_user()
    try:
        # Forward the request to the user_service for logout
        response = forward_request("http://user_service:5001", "/api/users/logout", method="POST")
        
        if response and response.status_code == 200:
            # Log out the user from Flask-Login
            logout_user()
            flash('Déconnexion réussie.', 'info')
        else:
            flash("Erreur lors de la déconnexion. Veuillez réessayer.", "danger")
    except Exception as e:
        # Handle any unexpected errors
        flash(f"Erreur de connexion au service utilisateur : {str(e)}", "danger")
    
    # Redirect the user to the index page
    return redirect(url_for('.index'))
# 1. Fonction pour réserver une chambre
@app_bp.route('/reserve/<int:room_id>', methods=['GET', 'POST'])
def reserve_room(room_id):
    user_id = current_user.id # Utilisateur connecté (hypothèse)
    if not user_id:
        flash("User ID is required to reserve a room.", "error")
        return redirect(url_for('.index'))

    # Changer le statut de la chambre à "réservée"
    room_response = requests.put(f"{ROOM_SERVICE_URL}/api/rooms/update_status/{room_id}", json={"status": "réservée"})
    if room_response.status_code != 200:
        flash("Failed to reserve the room.", "error")
        return redirect(url_for('.index'))

    # Ajouter la réservation dans le service réservation
    reservation_response = requests.post(f"{RESERVATION_SERVICE_URL}/add", json={"user_id": user_id, "room_id": room_id})
    if reservation_response.status_code == 201:
        flash("Room reserved successfully!", "success")
    else:
        flash("Failed to create reservation.", "error")

    return redirect(url_for('.index'))

# 2. Fonction pour annuler une réservation
@app_bp.route('/cancel/<int:reservation_id>', methods=['POST'])
def cancel(reservation_id):
    # Récupérer les détails de la réservation
    reservation_response = requests.get(f"{RESERVATION_SERVICE_URL}/get/{reservation_id}")
    if reservation_response.status_code != 200:
        flash("Reservation not found.", "error")
        return redirect(url_for('.index'))

    reservation = reservation_response.json()
    room_id = reservation['room_id']

    # Changer le statut de la chambre à "disponible"
    room_response = requests.put(f"{ROOM_SERVICE_URL}/api/rooms/update_status/{room_id}", json={"status": "disponible"})
    if room_response.status_code != 200:
        flash("Failed to update room status.", "error")
        return redirect(url_for('.index'))

    # Supprimer la réservation dans le service réservation
    delete_response = requests.delete(f"{RESERVATION_SERVICE_URL}/delete/{reservation_id}")
    if delete_response.status_code == 200:
        flash("Reservation canceled successfully.", "success")
    else:
        flash("Failed to cancel reservation.", "error")

    return redirect(url_for('.index'))

# 3. Fonction pour vérifier et supprimer les réservations expirées (plus de 72 heures)
@app_bp.route('/clean_expired', methods=['POST'])
def clean_expired_reservations():
    # Récupérer toutes les réservations
    response = requests.get(f"{RESERVATION_SERVICE_URL}/all")
    if response.status_code != 200:
        flash("Failed to fetch reservations.", "error")
        return redirect(url_for('.index'))

    reservations = response.json()
    now = datetime.utcnow()

    for reservation in reservations:
        reservation_date = datetime.strptime(reservation['reservation_date'], '%Y-%m-%d %H:%M:%S')
        if (now - reservation_date) > timedelta(hours=72):
            # Supprimer la réservation expirée
            delete_response = requests.delete(f"{RESERVATION_SERVICE_URL}/delete/{reservation['id']}")
            if delete_response.status_code == 200:
                # Mettre à jour le statut de la chambre
                room_id = reservation['room_id']
                requests.put(f"{ROOM_SERVICE_URL}/api/rooms/update_status/{room_id}", json={"status": "disponible"})

    flash("Expired reservations cleaned successfully.", "success")
    return redirect(url_for('.index'))

@app_bp.route('/my_reservations', methods=['GET'])
def my_reservations():
    try:
        # Appel au service de réservation pour récupérer toutes les réservations
        response = requests.get(f"{RESERVATION_SERVICE_URL}/all")
        response.raise_for_status()
        all_reservations = response.json()

        # Filtrer les réservations pour l'utilisateur connecté
        user_reservations = [
            reservation for reservation in all_reservations if reservation["user_id"] == current_user.id
        ]

        # Afficher les réservations dans un template
        return render_template(
            "my_reservations.html",
            reservations=user_reservations
        )

    except requests.exceptions.RequestException as e:
        # Gestion des erreurs d'appel au service de réservation
        flash(f"Erreur lors de la récupération des réservations : {e}", "danger")
        return redirect(url_for('.index'))


# 4. Fonction pour rappeler à un utilisateur sa réservation
@app_bp.route('/check_reservation/<int:user_id>', methods=['GET'])
def check_user_reservation(user_id):
    # Récupérer toutes les réservations de l'utilisateur
    response = requests.get(f"{RESERVATION_SERVICE_URL}/all")
    if response.status_code != 200:
        flash("Failed to fetch reservations.", "error")
        return redirect(url_for('.index'))

    reservations = response.json()
    now = datetime.utcnow()

    for reservation in reservations:
        if reservation['user_id'] == user_id:
            reservation_date = datetime.strptime(reservation['reservation_date'], '%Y-%m-%d %H:%M:%S')
            remaining_time = timedelta(hours=72) - (now - reservation_date)
            if remaining_time.total_seconds() > 0:
                flash(f"You have an active reservation! Time remaining: {remaining_time}.", "info")
            else:
                flash("Your reservation has expired.", "warning")

    return redirect(url_for('.index'))

@app_bp.route('/contact')
def contact():
    return render_template('contact.html')

@app_bp.route('/about')
def about():
    return render_template('about.html')


@app_bp.route('/pay/<int:room_id>')
def pay_room():
    pass

@app_bp.route('/informations')
def informations():
    return render_template('informations.html')

@app_bp.route('/settings')
def settings():
    pass

@app_bp.route('/actualites')
def actualites():
    return render_template('actualites.html')

@app_bp.route('/services')
def services():
    return render_template('services.html')

@app_bp.route('/payment')
def payment():
    pass
