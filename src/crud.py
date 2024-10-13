import src.models as models
from src.schemas.requests import CompanyUnitCreate, CompanyUnitUpdate
from sqlalchemy.orm import Session


def get_edges_by_parent_id(db: Session, parent_id: str):
    return db.query(models.Edge).filter(models.Edge.parent_id == parent_id).all()


def add_edge(db: Session, parent_id: str, child_id: str, weight: int):
    db_edge = models.Edge(parent_id=parent_id, child_id=child_id, weight=weight)
    db.add(db_edge)
    ancestor_edges = get_edges_by_parent_id(db, parent_id)
    for edge in ancestor_edges:
        anc_edge = models.Edge(
            parent_id=edge.parent_id, child_id=child_id, weight=edge.weight + 1
        )
        db.add(anc_edge)
    db.commit()
    db.refresh(db_edge)
    return db_edge


def get_company_unit_parent_id(db: Session, company_unit_id: str):
    db_edge = (
        db.query(models.Edge)
        .filter(models.Edge.child_id == company_unit_id, models.Edge.weight == 1)
        .first()
    )
    return db_edge.parent_id if db_edge else None


def add_root_company_unit(db: Session, company_unit: CompanyUnitCreate):
    db_company_unit = models.CompanyUnit(name=company_unit.name, height=0)
    db.add(db_company_unit)
    db.commit()
    db.refresh(db_company_unit)
    return db_company_unit


def get_root_company_unit(db: Session):
    return db.query(models.CompanyUnit).filter(models.CompanyUnit.height == 0).first()


def get_company_unit(db: Session, company_unit_id: str):
    db_company_unit = (
        db.query(models.CompanyUnit)
        .filter(models.CompanyUnit.id == company_unit_id)
        .first()
    )
    return db_company_unit


def add_company_unit(db: Session, company_unit: CompanyUnitCreate):
    if company_unit.parent_id is None:
        if get_root_company_unit(db) is None:
            return add_root_company_unit(db, company_unit)
        else:
            raise ValueError("Parent ID is None but root already exists")

    parent_unit = get_company_unit(db, company_unit.parent_id)
    if parent_unit is None:
        raise ValueError("Parent ID not found")

    db_company_unit = models.CompanyUnit(
        name=company_unit.name, height=parent_unit.height + 1
    )

    db.add(db_company_unit)
    db.commit()
    db.refresh(db_company_unit)

    if parent_unit:
        add_edge(
            db,
            parent_id=parent_unit.id,
            child_id=db_company_unit.id,
            weight=1,
        )

    return db_company_unit


def update_company_unit(
    db: Session, company_unit_id: str, company_unit: CompanyUnitUpdate
):
    db.query(models.CompanyUnit).filter(
        models.CompanyUnit.id == company_unit_id
    ).update(company_unit.model_dump())
    db.commit()
    return (
        db.query(models.CompanyUnit)
        .filter(models.CompanyUnit.id == company_unit_id)
        .first()
    )
