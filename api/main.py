from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from controllers import sandwiches
from models.schemas import Sandwich, SandwichCreate, SandwichUpdate
from fastapi.middleware.cors import CORSMiddleware

from .models import models, schemas
from .controllers import orders
from .dependencies.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/sandwiches/", response_model=Sandwich, tags=["Sandwiches"])
def create_sandwich(sandwich: SandwichCreate, db: Session = Depends(get_db)):
    return sandwiches.create(db=db, sandwich=sandwich)


@app.get("/sandwiches/", response_model=list[Sandwich], tags=["Sandwiches"])
def read_sandwiches(db: Session = Depends(get_db)):
    return sandwiches.read_all(db)


@app.get("/sandwiches/{sandwich_id}", response_model=Sandwich, tags=["Sandwiches"])
def read_one_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    sandwich = sandwiches.read_one(db, sandwich_id=sandwich_id)
    if sandwich is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    return sandwich


@app.put("/sandwiches/{sandwich_id}", response_model=Sandwich, tags=["Sandwiches"])
def update_one_sandwich(sandwich_id: int, sandwich: SandwichUpdate, db: Session = Depends(get_db)):
    sandwich_db = sandwiches.read_one(db, sandwich_id=sandwich_id)
    if sandwich_db is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    return sandwiches.update(db=db, sandwich=sandwich, sandwich_id=sandwich_id)


@app.delete("/sandwiches/{sandwich_id}", tags=["Sandwiches"])
def delete_one_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    sandwich = sandwiches.read_one(db, sandwich_id=sandwich_id)
    if sandwich is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    return sandwiches.delete(db=db, sandwich_id=sandwich_id)
