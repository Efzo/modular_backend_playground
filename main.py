from fastapi import FastAPI
from core.database import engine, Base
from modules.items.models import ItemModel
from modules.items.router import router as items_router


Base.metadata.create_all(bind=engine) #physically create tables if they don't exist


app =  FastAPI(
    title  = "Modular System PlayGround",
    description =  "Production-grade  evolving architecture foundation",
    version= "1.0.0"
)


app.include_router(items_router)


@app.get("/", tags=["Root"])
def root_check():
    return {
        "status": "Healthy",
        "system": "Modular_Backend_Playground"
    }