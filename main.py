from fastapi import FastAPI, Path, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

import models
from models import LoanApplication
from database import SessionLocal, engine


app = FastAPI()

origins = ["*"]

# Create all tables
models.Base.metadata.create_all(bind=engine)

# Get  database session
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close

@app.get("/{repay_period}/{amount}")
async def fee_finder(repay_period: int, amount: float, db: Session = Depends(get_db)):
    """Return a fee for a given repayment period and loan amount"""
    loan_app = LoanApplication(int(repay_period), amount)
    db.add(loan_app)
    db.commit()
    return {"fee": loan_app.fee}

@app.post("/loan_app")
async def fee_calc(repay_period: int, amount: float, db: Session = Depends(get_db)):
    """submit loan application"""
    loan_app = LoanApplication(int(repay_period), amount)
    db.add(loan_app)
    db.commit()
    return {"message": "Loan application received."}

@app.get("/all_loan_apps")
async def show_all_loan_apps():
        db = SessionLocal()
        loan_apps = db.query(LoanApplication).all()
        return loan_apps
