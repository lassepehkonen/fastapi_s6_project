from fastapi import HTTPException
from sqlalchemy.orm import Session

import models
from dtos.schemas import ViewingCreate


# Get all viewings

def get_viewings_controller(db: Session):
    viewings = get_viewings(db)

    if viewings is None:
        raise HTTPException(status_code=404, detail="Viewing not found")

    return viewings


def get_viewings(db: Session):
    viewings = db.query(models.Viewing).all()
    return {'items': viewings}


# Get single viewing

def get_viewing_by_id_controller(viewing_id: int, db: Session):
    viewing = get_viewing_by_id(viewing_id, db)

    if viewing is None:
        raise HTTPException(status_code=404, detail="Viewing not found")

    return viewing


def get_viewing_by_id(viewing_id: int, db: Session):
    return db.query(models.Viewing).get(viewing_id)


# Create new

def create_new_viewing_controller(current_user: dict, viewing_data: ViewingCreate, db: Session):
    if current_user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    try:
        db_viewing = create_new_viewing(db, viewing_data.model_dump())
        return db_viewing
    except Exception as e:
        raise HTTPException(status_code=400, detail="Bad Request")


def create_new_viewing(db: Session, viewing_data: dict):
    db_viewing = models.Viewing(**viewing_data)
    db.add(db_viewing)
    db.commit()
    db.refresh(db_viewing)
    return db_viewing


def accept_viewing_controller(viewing_id: int, current_user: dict, db: Session):
    # Tarkista, onko käyttäjä opettaja-roolissa
    if current_user.get("role") != "teacher":
        raise HTTPException(status_code=403, detail="Access denied. User is not a teacher.")

    # Get filtered viewing from database
    viewing = db.query(models.Viewing).filter(id=viewing_id).first()

    if not viewing:
        raise HTTPException(status_code=404, detail="Viewing not found")

    # The inspection is accepted by changing 'accepted' to 'true'.
    viewing.accepted = True
    db.commit()

    return {"accepted": True}

