from fastapi import FastAPI
from modules.items.router import router as items_router


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