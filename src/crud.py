import src.models as models
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import union_all, insert, literal, and_
from src.schemas.db_schemas import EdgeUpdate
from pydantic import UUID4


def add_node(db: Session, node: models.Node):
    """Add a new node to the database."""
    db.add(node)
    db.commit()
    db.refresh(node)
    return node


def get_node(db: Session, node_id: UUID4):
    """Gets a node from the database by its id."""
    return db.query(models.Node).filter(models.Node.id == node_id).first()


def get_root_node(db: Session) -> models.Node:
    """Get the root node of the tree. Looks for the only edge where the child id is not a child of any other edge."""
    subquery = db.query(models.Edge.child_id).filter(models.Edge.depth > 0).subquery()
    root_edge = (
        db.query(models.Edge).filter(~models.Edge.child_id.in_(subquery)).first()
    )
    if root_edge:
        return (
            db.query(models.Node).filter(models.Node.id == root_edge.child_id).first()
        )

    return None


def add_edges_on_node_creation(db: Session, node: models.Node, parent_id: UUID4):
    """Creates the necessary edges when a new node is added to the tree."""
    self_edge = db.query(
        literal(node.id).label("parent_id"),
        literal(node.id).label("child_id"),
        literal(0).label("depth"),
    )
    edge = db.query(
        models.Edge.parent_id,
        literal(node.id).label("child_id"),
        models.Edge.depth + 1,
    ).filter(models.Edge.child_id == parent_id)

    insert_stmt = insert(models.Edge).from_select(
        ["parent_id", "child_id", "depth"], union_all(self_edge, edge)
    )
    db.execute(insert_stmt)
    db.commit()
    return node


def update_edges(db: Session, edge_update: EdgeUpdate):
    """Updates the edges when a node changes its parent."""
    new_parent_id = edge_update.parent_id
    node_id = edge_update.child_id

    internal_trees = (
        db.query(models.Edge.child_id)
        .filter(models.Edge.parent_id == node_id)
        .subquery()
    )
    db.query(models.Edge).filter(
        and_(
            models.Edge.child_id.in_(internal_trees),
            models.Edge.parent_id.not_in(internal_trees),
        )
    ).delete()
    db.commit()

    supertree = db.query(models.Edge).subquery()
    subtree = db.query(models.Edge).subquery()

    edge_updates = db.query(
        supertree.c.parent_id.label("parent_id"),
        subtree.c.child_id.label("child_id"),
        (supertree.c.depth + subtree.c.depth + 1).label("depth"),
    ).filter(
        and_(
            subtree.c.parent_id == node_id,
            supertree.c.child_id == new_parent_id,
        )
    )

    insert_stmt = insert(models.Edge).from_select(
        ["parent_id", "child_id", "depth"], edge_updates
    )
    db.execute(insert_stmt)
    db.commit()
    return


def get_all_child_edges(db: Session, parent_id: UUID4):
    """Returns all the edges where the parent id is the given parent"""
    return db.query(models.Edge).filter(models.Edge.parent_id == parent_id).all()


def get_edge_by_clild_and_depth(db: Session, child_id: UUID4, depth: int):
    """Returns the edge where the child id is the given child and the depth is the given depth"""
    return (
        db.query(models.Edge)
        .filter(models.Edge.child_id == child_id)
        .filter(models.Edge.depth == depth)
        .first()
    )


def get_edge_by_parent_and_child(db: Session, parent_id: UUID4, child_id: UUID4):
    """Returns the edge where the parent id is the given parent and the child id is the given child"""
    return (
        db.query(models.Edge)
        .filter(models.Edge.parent_id == parent_id)
        .filter(models.Edge.child_id == child_id)
        .first()
    )
