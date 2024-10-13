from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from src import crud, models, schemas
from src.database import engine, get_db
from scripts.demo import add_sample_data
from src.routes.v1 import router as v1_router
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def lifespan(app: FastAPI):
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    add_sample_data()
    logger.info("Database initialized")
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(v1_router)


@app.get("/health")
def read_health():
    return {"status": "ok"}
