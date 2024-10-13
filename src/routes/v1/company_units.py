from src.routes.v1 import router
from src import crud
from src.database import get_db
from src.schemas.responses import CompanyUnit
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from src.domain.company_hierarchy.manager import CompanyManager


@router.get("/root", response_model=CompanyUnit)
def read_company_units(db: Session = Depends(get_db)):
    company_manager = CompanyManager(db)
    root_node = company_manager.get_root_node()
    root_company_unit_tree = company_manager.get_tree(root_node.id)

    return root_company_unit_tree


@router.get("/{company_unit_id}", response_model=CompanyUnit)
def read_company_unit(company_unit_id: str, db: Session = Depends(get_db)):
    if not company_unit_id:
        raise HTTPException(status_code=404, detail="Company unit not found")
    company_manager = CompanyManager(db)
    company_unit_tree = company_manager.get_tree(company_unit_id)

    return company_unit_tree
