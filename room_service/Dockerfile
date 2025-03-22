# Utiliser une image de base Python
FROM python:3.12-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de configuration et le code
COPY requirements.txt /app/
COPY . /app/

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port utilisé par l'application
EXPOSE 5002

# Commande pour démarrer l'application
CMD ["python", "run.py"]

