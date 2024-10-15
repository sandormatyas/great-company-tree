from src.routes.v1 import router
from src.database import get_db
from src.schemas.responses import CompanyUnit
from src.schemas.requests import CompanyUnitUpdate
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from src.domain.company_hierarchy.manager import CompanyManager
from pydantic import UUID4


@router.get("/root", response_model=CompanyUnit)
def get_company_hierarchy(db: Session = Depends(get_db)):
    company_manager = CompanyManager(db)
    root_node = company_manager.get_root_node()
    root_company_unit_tree = company_manager.get_tree(root_node.id)

    return root_company_unit_tree


@router.get("/{company_unit_id}", response_model=CompanyUnit)
def get_company_unit(company_unit_id: UUID4, db: Session = Depends(get_db)):
    company_manager = CompanyManager(db)
    node = company_manager.get_node(company_unit_id)
    if node is None:
        raise HTTPException(status_code=404, detail="Company unit not found")

    company_unit_tree = company_manager.get_tree(company_unit_id)
    return company_unit_tree


@router.patch("/{company_unit_id}", response_model=CompanyUnit)
def update_company_unit(
    company_unit_id: UUID4,
    payload: CompanyUnitUpdate,
    db: Session = Depends(get_db),
):
    company_manager = CompanyManager(db)
    node = company_manager.get_node(company_unit_id)
    if node is None:
        raise HTTPException(status_code=404, detail="Company unit not found")

    updated_company_unit_tree = company_manager.update_parent(company_unit_id, payload)
    return updated_company_unit_tree
