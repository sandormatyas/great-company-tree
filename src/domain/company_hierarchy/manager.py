import src.crud as crud
import src.models as models
from src.schemas.requests import CompanyUnitCreate
from src.schemas.responses import CompanyUnit
from pydantic import UUID4


class CompanyManager:
    def __init__(self, company_database):
        self.__db = company_database
        self.__root = self.get_root_node()

    def add_root_node(self, company_unit_create: CompanyUnitCreate) -> models.Node:
        new_node = crud.add_node(self.__db, models.Node(name=company_unit_create.name))
        edge = models.Edge(parent_id=None, child_id=new_node.id, weight=0)
        crud.add_edge(self.__db, edge)

        self.__root = new_node

        return new_node

    def add_node(self, company_unit_create: CompanyUnitCreate) -> models.Node:
        new_node = crud.add_node(self.__db, models.Node(name=company_unit_create.name))

        parent_edges = crud.get_edges_by_child_id(
            self.__db, child_id=company_unit_create.parent_id
        )
        for edge in parent_edges:
            extended_edge = models.Edge(
                parent_id=edge.parent_id, child_id=new_node.id, weight=edge.weight + 1
            )
            crud.add_edge(
                self.__db, extended_edge
            )  # TODO: add multilple edges in one transaction
        new_edge = models.Edge(
            parent_id=company_unit_create.parent_id, child_id=new_node.id, weight=1
        )
        crud.add_edge(self.__db, new_edge)

        return new_node

    def get_node(self, node_id: UUID4) -> models.Node:
        return crud.get_node(self.__db, node_id)

    def get_root_node(self) -> models.Node:
        return crud.get_root_node(self.__db)

    def get_tree(self, node_id: UUID4) -> CompanyUnit:
        company_unit = self.get_company_unit(node_id)
        edges_from_unit = crud.get_edges_by_parent_id(self.__db, parent_id=node_id)
        children = [self.get_company_unit(edge.child_id) for edge in edges_from_unit]
        company_unit.children = self.__build_tree(children, node_id)

        return company_unit

    def get_company_unit(self, node_id: UUID4) -> CompanyUnit:
        node = crud.get_node(self.__db, node_id)
        return CompanyUnit(
            id=node.id,
            root_id=self.__root.id,
            name=node.name,
            parent_id=self._get_parent_id(node_id),
            height=self._get_height(node_id),
        )

    def __build_tree(
        self, company_units: list[CompanyUnit], parent_id: UUID4
    ) -> list[CompanyUnit]:
        children = []
        for company_unit in company_units:
            if company_unit.parent_id == parent_id:
                company_unit.children = self.__build_tree(
                    company_units, company_unit.id
                )
                children.append(company_unit)
        return children

    def _get_parent_id(self, node_id: UUID4) -> UUID4 | None:
        edge = crud.get_edge_by_clild_id_and_weight(self.__db, node_id, 1)
        return edge.parent_id if edge else None

    def _get_height(self, node_id: UUID4) -> int:
        if node_id == self.__root.id:
            return 0
        root_parent_edge = crud.get_edge(
            self.__db, parent_id=self.__root.id, child_id=node_id
        )
        return root_parent_edge.weight
