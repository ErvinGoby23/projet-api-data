FROM python:3.11-slim

# Dossier de travail dans le container
WORKDIR /app

# Installer dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier ton code
COPY app app
COPY scripts scripts   

# Bonnes pratiques
ENV PYTHONUNBUFFERED=1

# Commande par défaut : lancer l'API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
