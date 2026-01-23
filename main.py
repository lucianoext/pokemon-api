from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.database.connection import engine, Base
from src.presentation.api.trainers import router as trainers_router
from src.presentation.api.pokemon import router as pokemon_router  # ← Agregar esta línea

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Pokemon API",
    description="API REST for Trainers and Pokemons",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/version")
def version():
    return {"version": "1.0.0"}

app.include_router(trainers_router, prefix="/api/v1")
app.include_router(pokemon_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)