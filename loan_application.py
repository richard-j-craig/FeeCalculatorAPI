from enum import IntEnum

from fee_sets import fee_sets


class RepaymentOptions(IntEnum):
    """Valid options for repayment periods (months)"""
    plan_1 = 12
    plan_2 = 24


class LoanApplication:
    """Creates a loan application"""    
    def __init__(self, repay_period, amount):
        self.repay_period = repay_period
        self.amount = round(amount, 2)

    def fee(self):
        """Calculates the fee for a loan application, based off
        relevant fee set."""
        try:
            fee_set = fee_sets[str(self.repay_period)]
        except:
            return None
        for i in range(1, len(fee_set)):
            if fee_set[i-1]["amount"] <= self.amount <= fee_set[i]["amount"]:
                # interpolate fee (linearly) from given interval
                ratio = ((self.amount - fee_set[i-1]["amount"])
                         / (fee_set[i]["amount"] - fee_set[i-1]["amount"]))
                unaltered_fee = (ratio 
                                 * (fee_set[i]["fee"] - fee_set[i-1]["fee"])
                                 + fee_set[i-1]["fee"])
                # alter fee so that fee + loan amount is a multiple of 5
                rounded_total = round((self.amount + unaltered_fee) / 5) * 5
                fee = round(rounded_total - self.amount, 2)
                return fee
            