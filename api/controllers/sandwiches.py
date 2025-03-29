from sqlalchemy.orm import Session
from models import Sandwich
from schemas import SandwichCreate, SandwichUpdate

# CREATE
def create(db: Session, sandwich: SandwichCreate):
    db_sandwich = Sandwich(name=sandwich.name, ingredients=sandwich.ingredients)
    db.add(db_sandwich)
    db.commit()
    db.refresh(db_sandwich)
    return db_sandwich

# READ ALL
def read_all(db: Session):
    return db.query(Sandwich).all()

# READ ONE
def read_one(db: Session, sandwich_id: int):
    return db.query(Sandwich).filter(Sandwich.id == sandwich_id).first()

# UPDATE
def update(db: Session, sandwich_id: int, sandwich: SandwichUpdate):
    db_sandwich = db.query(Sandwich).filter(Sandwich.id == sandwich_id)
    if db_sandwich.first() is None:
        return None
    db_sandwich.update(sandwich.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return db_sandwich.first()

# DELETE
def delete(db: Session, sandwich_id: int):
    db_sandwich = db.query(Sandwich).filter(Sandwich.id == sandwich_id)
    db_sandwich.delete(synchronize_session=False)
    db.commit()
    return {"message": "Sandwich deleted successfully"}
