from fastapi import FastAPI, Path

from loan_application import RepaymentOptions, LoanApplication   


app = FastAPI()


@app.get("/{repay_period}/{amount}")
async def fee_finder(
    repay_period: RepaymentOptions = Path(..., 
            title="Chosen repayment period (months)"), 
    amount: float = Path(..., 
            title="Monetary amount requested (£)", ge=1000, le=20000),
):
    """API to eturn a fee for a given repayment period and loan amount"""
    loan_app = LoanApplication(int(repay_period), amount)
    fee = loan_app.fee()
    return {"fee": fee}
