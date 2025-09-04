from fastapi import FastAPI
from .routers import transactions

app = FastAPI(
    title="Projet API Data",
    version="0.1.0",
    description="API d'exposition de données (transactions & événements ferroviaires)."
)

app.include_router(transactions.router)

@app.get("/health")
def health():
    return {"status": "ok"}

