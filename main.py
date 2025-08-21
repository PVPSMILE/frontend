from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session

SQLALCHEMY_DB_URL = 'sqlite:///./data.db'
engine = create_engine(SQLALCHEMY_DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# class NitroBooster(Base):=
#     __tablename__ = "nitro_boosters_for_wheelchair"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     price = Column(Integer, index=True)
#     power = Column(Integer, index=True)
#     boost_color = Column(String, index=True)

# Pydantic schemas
# class NitroBoosterBase(BaseModel):
#     name: str
#     price: int
#     power: int
#     boost_color: str


class ContactMessage(Base):
    __tablename__ = "contact_us"
    
    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, index=True)
    email = Column(String, index=True)
    message = Column(String, index=True)
    
class ContactBase(BaseModel):
    fullname: str
    email: str
    message: str
    
class ContactCreate(ContactBase):
    pass

class ContactOut(ContactBase):
    id: int
    class Config:
        orm_mode = True    

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/contact/", response_model=ContactOut)
def create_contact_message(contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = ContactMessage(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

# class NitroBoosterCreate(NitroBoosterBase):
#     pass

# class NitroBoosterUpdate(NitroBoosterBase):
#     pass

# class NitroBoosterOut(NitroBoosterBase):
#     id: int
#     class Config:
#         orm_mode = True    
#POSTGRESQL MySQL SQLite Microsoft SQL Server
#MongoDB Firebase Cassandra



# @app.post("/nitro_boosters/", response_model=NitroBoosterOut)
# def create_item(booster: NitroBoosterCreate, db: Session = Depends(get_db)):

#     db_booster = NitroBooster(**booster.dict())
#     db.add(db_booster)
#     db.commit()
#     db.refresh(db_booster)
#     return db_booster

