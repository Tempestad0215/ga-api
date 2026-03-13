from contextlib import asynccontextmanager

import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI
import datetime as dt


from src.routes.sap_route import sap_router
from src.services.check_stok_warehouse import check_stok_warehouse

scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    trigger = CronTrigger(
        day_of_week="mon",
        hour="3",
        minute="0",
        timezone=pytz.timezone("America/Santo_Domingo")
    )

    scheduler.add_job(
        check_stok_warehouse,
        trigger=trigger,
        args=["ALM1"],
        id="check_stok_warehouse_ALM1",

    )
    # Para iniciar el job
    scheduler.start()

    yield
    # Para apagar el cron al finalizar
    scheduler.shutdown()


app = FastAPI(
    version="0.0.1:Betas",
    title="Service Layer Grupo Atlantico",
    description="Service Layer Grupo Atlantico",
    lifespan=lifespan,
)
@app.get("/")
def read_root():
    return {"Hello": "World"}



app.include_router(sap_router)