from fastapi import FastAPI, Depends
import json
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session

SQLALCHEMY_DB_URL = 'sqlite:///./data.db'
engine = create_engine(SQLALCHEMY_DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class NitroBooster(Base):
    __tablename__ = "nitro_boosters_for_wheelchair"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Integer, index=True)
    power = Column(Integer, index=True)
    boost_color = Column(String, index=True)

Base.metadata.create_all(bind=engine)

# Pydantic schemas
class NitroBoosterBase(BaseModel):
    name: str
    price: int
    power: int
    boost_color: str

class NitroBoosterCreate(NitroBoosterBase):
    pass

class NitroBoosterUpdate(NitroBoosterBase):
    pass

class NitroBoosterOut(NitroBoosterBase):
    id: int
    class Config:
        orm_mode = True    
#POSTGRESQL MySQL SQLite Microsoft SQL Server
#MongoDB Firebase Cassandra

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  

@app.post("/nitro_boosters/", response_model=NitroBoosterOut)
def create_item(booster: NitroBoosterCreate, db: Session = Depends(get_db)):

    db_booster = NitroBooster(**booster.dict())
    db.add(db_booster)
    db.commit()
    db.refresh(db_booster)
    return db_booster

