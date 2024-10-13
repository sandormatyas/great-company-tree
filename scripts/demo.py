from src.database import get_db
from src.schemas.requests import CompanyUnitCreate
from src.domain.company_hierarchy.manager import CompanyManager


def add_sample_data():
    db = next(get_db())
    company_manager = CompanyManager(db)

    # root node
    company_unit = CompanyUnitCreate(
        parent_id=None,
        name="Company",
    )
    root = company_manager.add_root_node(company_unit)

    company_unit = CompanyUnitCreate(
        parent_id=root.id,
        name="Division 1",
    )
    div1 = company_manager.add_node(company_unit)

    company_unit = CompanyUnitCreate(
        parent_id=root.id,
        name="Division 2",
    )
    company_manager.add_node(company_unit)

    company_unit = CompanyUnitCreate(
        parent_id=root.id,
        name="Division 3",
    )
    company_manager.add_node(company_unit)

    company_unit = CompanyUnitCreate(
        parent_id=div1.id,
        name="Department 1",
    )
    company_manager.add_node(company_unit)
