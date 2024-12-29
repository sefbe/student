# Utilisation d'une image Python officielle
FROM python:3.12-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires pour installer les dépendances
COPY requirements.txt /app/

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code dans le conteneur
COPY . /app/

# Définir la variable d'environnement pour Flask
ENV FLASK_APP=run.py

# Exposer le port 5000 pour accéder à l'application
EXPOSE 5000

# Commande pour démarrer l'application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

