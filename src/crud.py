import src.models as models
from sqlalchemy.orm import Session
from src.schemas.db_schemas import EdgeUpdate
from pydantic import UUID4


def add_node(db: Session, node: models.Node):
    db.add(node)
    db.commit()
    db.refresh(node)
    return node


def add_edge(db: Session, edge: models.Edge):
    db.add(edge)
    db.commit()
    db.refresh(edge)
    return edge


def remove_edge(db: Session, edge: models.Edge):
    db.delete(edge)
    db.commit()
    return edge


def update_edge(db: Session, edge: models.Edge, edge_update: EdgeUpdate):
    for key, value in edge_update.dict(exclude_unset=True).items():
        setattr(edge, key, value)
    db.commit()
    db.refresh(edge)
    return edge


def get_edge_by_parent_and_child(db: Session, parent_id: UUID4, child_id: UUID4):
    return (
        db.query(models.Edge)
        .filter(models.Edge.parent_id == parent_id, models.Edge.child_id == child_id)
        .first()
    )


def get_edge_by_clild_and_weight(db: Session, child_id: UUID4, weight: int):
    return (
        db.query(models.Edge)
        .filter(models.Edge.child_id == child_id, models.Edge.weight == weight)
        .first()
    )


def get_edges_by_child(db: Session, child_id: UUID4):
    return (
        db.query(models.Edge)
        .filter(models.Edge.child_id == child_id, models.Edge.parent_id.is_not(None))
        .all()
    )


def get_edges_by_parent(db: Session, parent_id: UUID4):
    return db.query(models.Edge).filter(models.Edge.parent_id == parent_id).all()


def get_node(db: Session, node_id: UUID4):
    return db.query(models.Node).filter(models.Node.id == node_id).first()


def get_root_node(db: Session):
    root_node = db.query(models.Edge).filter(models.Edge.weight == 0).first()
    if root_node:
        return (
            db.query(models.Node).filter(models.Node.id == root_node.child_id).first()
        )
    return None
