from fastapi import FastAPI, Path
from enum import IntEnum

from functions import plan_lookup, fee_calculator


class RepaymentOptions(IntEnum):
    """Valid options for repayment periods (months)"""
    plan_1 = 12
    plan_2 = 24
    

app = FastAPI()


@app.get("/{repay_period}/{amount}")
async def fee_finder(
    repay_period: RepaymentOptions = Path(..., title="Chosen repayment period (months)"), 
    amount: float = Path(..., title="Monetary amount requested (£)", ge=1000, le=20000),
):
    """API to eturn a fee for a given repayment period and loan amount"""
    plan = plan_lookup(repay_period)
    fee = fee_calculator(plan, amount)
    return {"months": repay_period, "amount": amount, "fee": fee}
