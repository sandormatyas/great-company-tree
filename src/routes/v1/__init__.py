from fastapi import APIRouter

router = APIRouter(
    prefix="/v1/company_units",
)

from src.routes.v1.company_units import *
