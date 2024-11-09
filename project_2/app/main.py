from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Date, Integer, Time, Double, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from datetime import date, time

DATABASE_URL = "mysql+mysqlconnector://root:Maka2024%2B@localhost/sales_insight"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Seller(Base):
    __tablename__ = "sellers"
    login = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    hiring_date = Column(Date)

class Outbound(Base):
    __tablename__ = "outbound"
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, index=True)
    contacts = Column(Integer)
    usefull_contacts = Column(Integer)
    sales = Column(Integer)
    login_time = Column(Time)

class Inbound(Base):
    __tablename__ = "inbound"
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, index=True)
    contacts = Column(Integer)
    usefull_contacts = Column(Integer)
    sales = Column(Integer)
    login_time = Column(Time)

class StatusTime(Base):
    __tablename__ = "status_time"
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, index=True)
    talk_time = Column(Time)
    acw_time = Column(Time)
    avalible_time = Column(Time)

class Commissions(Base):
    __tablename__ = "commissions"
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, index=True)
    sales = Column(Integer)
    insurance = Column(Integer)
    briefcase = Column(Integer)

class Prices(Base):
    __tablename__ = "prices"
    id = Column(Integer, primary_key=True, index=True)
    sales = Column(Double)
    insurance = Column(Double)
    briefcase = Column(Double)

class SellerCreate(BaseModel):
    login: str
    name: str
    hiring_date: date

class OutboundCreate(BaseModel):
    login: str
    contacts: int
    usefull_contacts: int
    sales: int
    login_time: time

class InboundCreate(BaseModel):
    login: str
    contacts: int
    usefull_contacts: int
    sales: int
    login_time: time

class StatusTimeCreate(BaseModel):
    login: str
    talk_time: time
    acw_time: time
    avalible_time: time

class CommissionsCreate(BaseModel):
    login: str
    sales: int
    insurance: int
    briefcase: int

class PricesCreate(BaseModel):
    sales: float
    insurance: float
    briefcase: float

class SQLQuery(BaseModel):
    query: str

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/sellers/")
def read_sellers(db: Session = Depends(get_db)):
    return db.query(Seller).all()

@app.post("/sellers/")
def create_seller(seller: SellerCreate, db: Session = Depends(get_db)):
    db_seller = Seller(**seller.dict())
    db.add(db_seller)
    db.commit()
    db.refresh(db_seller)
    return db_seller

@app.delete("/sellers/clear/")
def clear_sellers(db: Session = Depends(get_db)):
    db.query(Seller).delete()
    db.commit()
    return {"message": "Todos los registros de Sellers han sido eliminados"}

@app.get("/outbound/")
def read_outbound(db: Session = Depends(get_db)):
    return db.query(Outbound).all()

@app.post("/outbound/")
def create_outbound(outbound: OutboundCreate, db: Session = Depends(get_db)):
    db_outbound = Outbound(**outbound.dict())
    db.add(db_outbound)
    db.commit()
    db.refresh(db_outbound)
    return db_outbound

@app.delete("/outbound/clear/")
def clear_outbound(db: Session = Depends(get_db)):
    db.query(Outbound).delete()
    db.commit()
    return {"message": "Todos los registros de Outbound han sido eliminados"}

@app.get("/inbound/")
def read_inbound(db: Session = Depends(get_db)):
    return db.query(Inbound).all()

@app.post("/inbound/")
def create_inbound(inbound: InboundCreate, db: Session = Depends(get_db)):
    db_inbound = Inbound(**inbound.dict())
    db.add(db_inbound)
    db.commit()
    db.refresh(db_inbound)
    return db_inbound

@app.delete("/inbound/clear/")
def clear_inbound(db: Session = Depends(get_db)):
    db.query(Inbound).delete()
    db.commit()
    return {"message": "Todos los registros de Inbound han sido eliminados"}

@app.get("/status_time/")
def read_status_time(db: Session = Depends(get_db)):
    return db.query(StatusTime).all()

@app.post("/status_time/")
def create_status_time(status_time: StatusTimeCreate, db: Session = Depends(get_db)):
    db_status_time = StatusTime(**status_time.dict())
    db.add(db_status_time)
    db.commit()
    db.refresh(db_status_time)
    return db_status_time

@app.delete("/status_time/clear/")
def clear_status_time(db: Session = Depends(get_db)):
    db.query(StatusTime).delete()
    db.commit()
    return {"message": "Todos los registros de StatusTime han sido eliminados"}

@app.get("/commissions/")
def read_commissions(db: Session = Depends(get_db)):
    return db.query(Commissions).all()

@app.post("/commissions/")
def create_commissions(commissions: CommissionsCreate, db: Session = Depends(get_db)):
    db_commissions = Commissions(**commissions.dict())
    db.add(db_commissions)
    db.commit()
    db.refresh(db_commissions)
    return db_commissions

@app.delete("/commissions/clear/")
def clear_commissions(db: Session = Depends(get_db)):
    db.query(Commissions).delete()
    db.commit()
    return {"message": "Todos los registros de Commissions han sido eliminados"}

@app.get("/prices/")
def read_prices(db: Session = Depends(get_db)):
    return db.query(Prices).all()

@app.post("/prices/")
def create_prices(prices: PricesCreate, db: Session = Depends(get_db)):
    db_prices = Prices(**prices.dict())
    db.add(db_prices)
    db.commit()
    db.refresh(db_prices)
    return db_prices

@app.delete("/prices/clear/")
def clear_prices(db: Session = Depends(get_db)):
    db.query(Prices).delete()
    db.commit()
    return {"message": "Todos los registros de Prices han sido eliminados"}

@app.post("/execute_sql")
def execute_sql(sql_query: SQLQuery, db: Session = Depends(get_db)):
    if not sql_query.query.strip():  
        raise HTTPException(status_code=400, detail="La consulta SQL no puede estar vacía.")
    try:
        result = db.execute(text(sql_query.query))

        if result.returns_rows:  
            rows = result.fetchall()  
            columns = result.keys()  

            result_dict = [dict(zip(columns, row)) for row in rows]
            return {"result": result_dict}
        
        return {"message": "Consulta ejecutada exitosamente"}

    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error SQL: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error en la consulta SQL: {str(e)}")
    except Exception as e:
        print(f"Error desconocido: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor.")