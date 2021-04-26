from sqlalchemy import Column, Integer, Float

from database import Base
from fee_sets import fee_sets


class LoanApplication(Base):
    __tablename__ = "loan_application"

    id = Column(Integer, primary_key=True, index=True)
    repay_period = Column(Integer)
    amount = Column(Float)
    fee = Column(Float, nullable=True)

    """Creates a loan application"""    
    def __init__(self, repay_period, amount):
        self.repay_period = repay_period
        self.amount = round(amount, 2)
        try:
            fee_set = fee_sets[str(repay_period)]
            for i in range(1, len(fee_set)):
                if fee_set[i-1]["amount"] <= amount <= fee_set[i]["amount"]:
                    # interpolate fee (linearly) from given interval
                    ratio = ((amount - fee_set[i-1]["amount"])
                            / (fee_set[i]["amount"] - fee_set[i-1]["amount"]))
                    unaltered_fee = (ratio 
                                    * (fee_set[i]["fee"] - fee_set[i-1]["fee"])
                                    + fee_set[i-1]["fee"])
                    # alter fee so that fee + loan amount is a multiple of 5
                    rounded_total = round((amount + unaltered_fee) / 5) * 5
                    fee = round(rounded_total - amount, 2)
                    self.fee = fee
        except:
            pass