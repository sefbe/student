from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms import SignupForm, LoginForm, RoomForm
from app.utils import forward_request
from flask_login import current_user, login_required
import requests
app_bp = Blueprint('app_bp', __name__)



# URL du microservice room_service (l'adresse peut être différente selon votre environnement Docker ou local)
ROOM_SERVICE_URL = "http://127.0.0.1:5002"  # Adaptez l'URL en fonction de l'environnement

USER_SERVICE_URL = "http://127.0.0.1:5001"  # URL du microservice user_service


@app_bp.route('/')
def index():
    # Récupération des chambres aléatoires depuis le room_service
    try:
        response = requests.get(f"{ROOM_SERVICE_URL}/api/rooms/random")
        if response.status_code == 200:
            rooms = response.json()  # Liste de chambres
        else:
            rooms = []
            flash("Impossible de récupérer les chambres.", "danger")
    except requests.RequestException:
        rooms = []
        flash("Erreur de connexion au service des chambres.", "danger")

    # Vérifiez si l'utilisateur est connecté et récupérez son statut
    show_add_room_button = False
    if current_user.is_authenticated:
        try:
            # Appel au user_service pour obtenir des détails supplémentaires
            user_response = requests.get(f"{USER_SERVICE_URL}/api/users/{current_user.id}")
            if user_response.status_code == 200:
                user_data = user_response.json()
                if user_data.get('status') == 'proprietaire':
                    show_add_room_button = True
            else:
                flash("Impossible de vérifier le statut de l'utilisateur.", "warning")
        except requests.RequestException:
            flash("Erreur de connexion au service utilisateur.", "danger")

    # Rendre la page avec les chambres et l'état du bouton
    return render_template('index.html', rooms=rooms, show_add_room_button=show_add_room_button)

# Route pour afficher les détails d'une chambre
@app_bp.route('/room/<int:room_id>')
def room_details(room_id):
    response = requests.get(f"{ROOM_SERVICE_URL}/api/rooms/{room_id}")
    if response.status_code == 200:
        room = response.json()
    else:
        flash("Chambre non trouvée", "danger")
        return redirect(url_for('room_bp.index'))
    return render_template('room_details.html', room=room)

# Route pour ajouter une chambre (seulement pour les propriétaires)
@app_bp.route('/add_room', methods=['GET', 'POST'])
def add_room():
    form = RoomForm()
    if form.validate_on_submit():
        # Créer un dictionnaire avec les données du formulaire
        data = {
            'title': form.title.data,
            'description': form.description.data,
            'price': form.price.data,
            'location': form.location.data,
            'distance': form.distance.data,
            'images': ','.join(form.images.data),  # Stockage des images sous forme de chaîne
            'owner_id': current_user.id  # Utilisation de l'ID du propriétaire authentifié
        }
        # Envoi des données au microservice `room_service`
        response = requests.post(f"{ROOM_SERVICE_URL}/api/rooms", json=data)
        if response.status_code == 201:
            flash('Chambre ajoutée avec succès!', 'success')
            return redirect(url_for('room_bp.index'))
        else:
            flash('Erreur lors de l\'ajout de la chambre.', 'danger')
    return render_template('add_room.html', form=form)

# Route pour supprimer une chambre (seulement pour le propriétaire)
@app_bp.route('/delete_room/<int:room_id>', methods=['POST'])
def delete_room(room_id):
    # Vous pouvez vérifier que l'utilisateur est bien le propriétaire de la chambre ici
    response = requests.delete(f"{ROOM_SERVICE_URL}/api/rooms/{room_id}")
    if response.status_code == 200:
        flash('Chambre supprimée avec succès', 'success')
    else:
        flash('Erreur lors de la suppression de la chambre', 'danger')
    return redirect(url_for('room_bp.index'))


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
            flash('Connexion réussie !', 'success')
            return redirect(url_for('.index'))
        else:
            flash('Erreur de connexion. Veuillez vérifier vos identifiants.', 'danger')
    return render_template('login.html', form=form)

@app_bp.route('/logout')
def logout():
    response = forward_request("http://user_service:5001", "/api/users/logout", method="POST")
    flash('Déconnexion réussie.', 'info')
    return redirect(url_for('.index'))

@app_bp.route('/contact')
def contact():
    pass

@app_bp.route('/about')
def about():
    pass
