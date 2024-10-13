from src.routes.v1 import router
from src import crud
from src.database import get_db
from src.schemas.responses import CompanyUnitResponse
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException


@router.get("/root", response_model=CompanyUnitResponse)
def read_company_units(db: Session = Depends(get_db)):
    root = crud.get_root_company_unit(db)
    company_unit_response = CompanyUnitResponse(
        id=root.id,
        parent_id=None,
        name=root.name,
        height=root.height,
        root_id=root.id,
    )
    return company_unit_response


@router.get("/{company_unit_id}", response_model=CompanyUnitResponse)
def read_company_unit(company_unit_id: str, db: Session = Depends(get_db)):
    root = crud.get_root_company_unit(db)
    db_item = crud.get_company_unit(db, company_unit_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Company Unit not found")

    parent_id = crud.get_company_unit_parent_id(db, company_unit_id)
    company_unit_response = CompanyUnitResponse(
        id=db_item.id,
        parent_id=parent_id,
        name=db_item.name,
        height=db_item.height,
        root_id=root.id,
    )
    return company_unit_response
