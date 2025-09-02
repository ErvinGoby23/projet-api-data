import random
from datetime import datetime, timedelta

from app.db import SessionLocal, engine, Base
from app.models import Transaction, RailEvent

# 🔹 Crée les tables si elles n'existent pas (utile pour SQLite/local dev)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# 🔹 Liste de marchands & catégories fictifs
merchants = ["SNCF", "Amazon", "McDonalds", "Carrefour", "Fnac"]
categories = ["ticket", "food", "shopping", "transport", "entertainment"]

# 🔹 Générer 50 transactions aléatoires
for i in range(50):
    tx = Transaction(
        timestamp=datetime.now() - timedelta(days=random.randint(0, 30)),
        amount=round(random.uniform(5, 200), 2),
        currency="EUR",
        merchant=random.choice(merchants),
        category=random.choice(categories),
        user_id=str(random.randint(1, 5)),  # 5 utilisateurs fictifs
        meta={"source": "seed-script"}
    )
    db.add(tx)

# 🔹 Générer 10 événements ferroviaires aléatoires
sites = ["Paris Gare de Lyon", "Marseille St-Charles", "Lyon Part-Dieu"]
events = ["ARRIVAL", "DEPARTURE", "DELAY", "CANCEL"]

for i in range(10):
    ev = RailEvent(
        event_time=datetime.now() - timedelta(hours=random.randint(0, 48)),
        site_name=random.choice(sites),
        train_no=f"TGV-{random.randint(100, 999)}",
        event_type=random.choice(events),
        delay_min=random.choice([None, 5, 10, 30, 60]),
        notes="Généré par seed"
    )
    db.add(ev)

db.commit()
db.close()

print("✅ Seed terminé : 50 transactions + 10 rail_events insérés")
