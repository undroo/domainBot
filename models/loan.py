import pandas as pd
import numpy as np

class Loan:
    def __init__(self, amount, rate, months, additional_repayments=0):
        self.amount = amount
        self.rate = rate/12
        self.months = months
        self.additional_repayments = additional_repayments
        self.loan_df = self._create_loan_df()

    def monthly_payment(self):
        p = self.amount
        r = self.rate
        n = self.months
        m = p * r * (1 + r)**n / ((1 + r)**n - 1)
        return m

    def _create_loan_df(self):
        p = self.amount
        r = self.rate
        n = self.months
        a = self.additional_repayments
        payment = self.monthly_payment()
        balance = p
        # df = pd.DataFrame(columns=["month", "payment", "interest", "principal", "additional_repayment", "balance"])
        row = {"month": [], 
                   "payment": [], 
                   "interest": [], 
                   "principal": [], 
                   "additional_repayment": [], 
                   "balance": []
                   }
        for month in range(1, n+1):
            interest = balance * r
            principal = payment - interest + a
            if balance < principal:
                principal = balance
                a = 0
            balance -= principal

            row["month"].append(month)
            row["payment"].append(payment)
            row["interest"].append(interest)
            row["principal"].append(principal)
            row["additional_repayment"].append(a)
            row["balance"].append(balance)
            # needs to be changed, stop adding row by row to a dataframe
            if balance == 0:
                break
        
        df = pd.DataFrame(row)
        # df = df.append(row, ignore_index=True)
        return df
    

    # this function should be changed, maybe consider filtering values of months and then summing the interest
    def remaining_interest(self, months_in):
        remaining_df = self.loan_df[self.loan_df["month"] > months_in]
        remaining_interest = remaining_df["interest"].sum()
        return remaining_interest
    
# Testing stuff
# loan = Loan(amount=100000, rate=0.04, months=360, additional_repayments=0)
# print(loan.loan_df)
# print(loan.remaining_interest(358))