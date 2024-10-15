from src.database import get_db
from src.schemas.requests import CompanyUnitCreate
from src.domain.company_hierarchy.manager import CompanyManager


def add_sample_data():
    """Generates the following tree structure:
    Company
    ├── Division 1
    │   └── Department 1
    │       ├── Team 1
    │       └── Team 2
    ├── Division 2
    └── Division 3
    """
    db = next(get_db())
    company_manager = CompanyManager(db)

    # root node
    root = company_manager.add_root_node(
        CompanyUnitCreate(
            parent_id=None,
            name="Company",
        )
    )

    div1 = company_manager.add_node(
        CompanyUnitCreate(
            parent_id=root.id,
            name="Division 1",
        )
    )

    company_manager.add_node(
        CompanyUnitCreate(
            parent_id=root.id,
            name="Division 2",
        )
    )

    company_manager.add_node(
        CompanyUnitCreate(
            parent_id=root.id,
            name="Division 3",
        )
    )

    dep1 = company_manager.add_node(
        CompanyUnitCreate(
            parent_id=div1.id,
            name="Department 1",
        )
    )

    company_manager.add_node(
        CompanyUnitCreate(
            parent_id=dep1.id,
            name="Team 1",
        )
    )

    company_manager.add_node(
        CompanyUnitCreate(
            parent_id=dep1.id,
            name="Team 2",
        )
    )
