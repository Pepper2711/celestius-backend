from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .models import Registration
from .schemas import RegistrationCreate, RegistrationResponse, RegistrationListResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Celestius Event Registration API")

EVENT_CAPACITY = 50

@app.post("/register", response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED)
def register_participant(payload: RegistrationCreate, db: Session = Depends(get_db)):
    clean_name = payload.name.strip()
    clean_email = payload.email.strip().lower()
    clean_college = payload.college_department.strip() if payload.college_department else None

    if not clean_name:
        raise HTTPException(status_code=400, detail="Name cannot be empty.")

    current_count = db.query(Registration).count()
    if current_count >= EVENT_CAPACITY:
        raise HTTPException(status_code=400, detail="Event is full. Maximum capacity reached.")

    existing = db.query(Registration).filter(Registration.email == clean_email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email is already registered.")

    new_registration = Registration(
        name=clean_name,
        email=clean_email,
        college_department=clean_college
    )
    db.add(new_registration)
    db.commit()
    db.refresh(new_registration)
    return new_registration

@app.get("/registrations", response_model=RegistrationListResponse)
def get_all_registrations(db: Session = Depends(get_db)):
    registrations = db.query(Registration).order_by(Registration.registered_at.asc()).all()
    return {
        "capacity": EVENT_CAPACITY,
        "total_registered": len(registrations),
        "seats_remaining": EVENT_CAPACITY - len(registrations),
        "data": registrations
    }

@app.get("/registrations/{identifier}", response_model=RegistrationResponse)
def get_single_registration(identifier: str, db: Session = Depends(get_db)):
    if identifier.isdigit():
        registration = db.query(Registration).filter(Registration.id == int(identifier)).first()
    else:
        registration = db.query(Registration).filter(Registration.email == identifier.lower()).first()

    if not registration:
        raise HTTPException(status_code=404, detail="Registration record not found.")

    return registration
