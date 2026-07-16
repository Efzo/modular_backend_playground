from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.database import engine, Base
from modules.items.models import ItemModel
from modules.items.router import router as items_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Base.metadata.create_all is natively synchronous -  run it through the async engine's runner
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # shutdown routines would go here    


app =  FastAPI(
    title  = "Modular System PlayGround",
    description =  "Production-grade  evolving architecture foundation",
    version= "1.0.0",
    lifespan=lifespan
)


app.include_router(items_router)


@app.get("/", tags=["Root"])
def root_check():
    return {
        "status": "Healthy",
        "system": "Modular_Backend_Playground"
    }