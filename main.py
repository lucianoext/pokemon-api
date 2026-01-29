from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.persistence.database.connection import engine, Base
from src.presentation.api.trainers import router as trainers_router
from src.presentation.api.pokemon import router as pokemon_router
from src.presentation.api.items import router as items_router
from src.presentation.api.teams import router as teams_router
from src.presentation.api.backpacks import router as backpacks_router

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
app.include_router(teams_router, prefix="/api/v1") 
app.include_router(items_router, prefix="/api/v1")
app.include_router(backpacks_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0",
        port=8000
    )