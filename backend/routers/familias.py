from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.familia import FamiliaCreate, FamiliaPublic
from backend.models.familia import Familia

router = APIRouter()

@router.post("/", response_model=FamiliaPublic, status_code=201)
def create_familia(familia: FamiliaCreate, db: Session = Depends(get_db)):
    db_familia = db.query(Familia).filter(Familia.nome_familia == familia.nome_familia).first()
    if db_familia:
        raise HTTPException(status_code=400, detail="Family name already registered")
    new_familia = Familia(**familia.model_dump())
    db.add(new_familia)
    db.commit()
    db.refresh(new_familia)
    return new_familia