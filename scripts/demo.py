from src.database import get_db
from src.crud import add_company_unit
from src.schemas.requests import CompanyUnitCreate


def add_sample_data():
    db = next(get_db())
    # root node
    company_unit = CompanyUnitCreate(
        parent_id=None,
        name="Company",
    )
    root = add_company_unit(db, company_unit)

    company_unit = CompanyUnitCreate(
        parent_id=root.id,
        name="Division 1",
    )
    div1 = add_company_unit(db, company_unit)

    company_unit = CompanyUnitCreate(
        parent_id=root.id,
        name="Division 2",
    )
    add_company_unit(db, company_unit)

    company_unit = CompanyUnitCreate(
        parent_id=root.id,
        name="Division 3",
    )
    add_company_unit(db, company_unit)

    company_unit = CompanyUnitCreate(
        parent_id=div1.id,
        name="Department 1",
    )
    add_company_unit(db, company_unit)
