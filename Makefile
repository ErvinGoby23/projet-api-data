# === Raccourcis utiles ===

# Lancer l'API en local (hors Docker)
run:
	uvicorn app.main:app --reload --port 8000

# Lancer l'app avec Docker
up:
	docker compose up --build -d

# Arrêter tout
down:
	docker compose down

# Lancer migrations Alembic
migrate:
	alembic upgrade head

# Créer une nouvelle révision Alembic
revision:
	alembic revision --autogenerate -m "$(m)"

# Lancer les tests unitaires
test:
	pytest -q
