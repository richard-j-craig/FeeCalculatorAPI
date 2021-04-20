
def plan_lookup(months):
    """Function to loop up plan corresponding to given 
    repayment period in months"""
    if months == 12:
        return [
            [1000, 50],
            [2000, 90],
            [3000, 90],
            [4000, 115],
            [5000, 100],
            [20000, 400]
        ]
    if months == 24:
        return [
            [1000, 70],
            [2000, 100],
            [3000, 120],
            [20000, 800]
        ]

def fee_calculator(plan, amount):
    """Function to calculate fee for chosen loan amount and repayment plan"""
    amount = round(amount, 2)
    for i in range(1, len(plan)):
        amount_top = plan[i][0]
        amount_bottom = plan[i-1][0]
        fee_top = plan[i][1]
        fee_bottom = plan[i-1][1]
        if amount_bottom <= amount <= amount_top:
            ratio = (amount - amount_bottom)/(amount_top - amount_bottom)
            unaltered_fee = ratio*(fee_top - fee_bottom) + fee_bottom
            # alter fee so that fee + loan amount is a multiple of 5
            rounded_total = round((amount + unaltered_fee)/5) * 5
            fee = round(rounded_total - amount, 2)
            return fee
            