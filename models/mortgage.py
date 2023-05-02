from models.loan import Loan
import pandas as pd

class Mortgage:
    def __init__(self, 
                 property_value, down_payment_pct, interest_rate, loan_term, 
                 monthly_rent, operating_expenses,
                 vacancy_rate, investment_length, 
                 capital_growth = 0.03, inflation=0.03):
        self.property_value = property_value
        self.down_payment_pct = down_payment_pct
        self.loan_amount = property_value * (1-down_payment_pct/100)
        self.loan = Loan(self.loan_amount, interest_rate/100, loan_term * 12)
        self.monthly_rent = monthly_rent
        self.operating_expenses = operating_expenses / 100
        self.vacancy_rate = vacancy_rate / 100
        self.investment_length = investment_length # Length of investment in years
        self.capital_growth = capital_growth
        self.inflation = inflation
        self.mortgage_df = self.loan.loan_df.copy().head(investment_length*12)
        # add new columns to loan_df for net cash flow
        self._create_mortgage_df()



    def _rent(self):
        rent = pd.Series([self.monthly_rent * (1-self.vacancy_rate) * (1 + self.inflation)**(i//12) for i in range(1, self.investment_length*12+1)])
        return rent

    def _value(self):
        value = pd.Series(self.property_value * (1+self.capital_growth)**(i/12) for i in range(1, self.investment_length*12+1))
        return value

    def _create_mortgage_df(self):
        self.mortgage_df['rent'] = self._rent()
        self.mortgage_df['expenses'] = self.mortgage_df['rent'] * self.operating_expenses
        self.mortgage_df['profit'] = self.mortgage_df['rent'] - self.mortgage_df['expenses'] - self.mortgage_df['interest']
        self.mortgage_df['net cash flow'] = self.mortgage_df['rent'] - self.mortgage_df['expenses'] - self.mortgage_df['payment']
        self.mortgage_df['value'] = self._value()
        self.mortgage_df['equity (%)'] = (self.mortgage_df['value'] - self.mortgage_df['balance'])*100/self.mortgage_df['value'] 
        self.mortgage_df = self.mortgage_df.set_index("month").round(2)
# property_value = 700000
# down_payment_pct = 30
# interest_rate = 5.5
# loan_term = 30
# monthly_rent = 3000
# operating_expenses = 20
# vacancy_rate = 5
# investment_length = 10

# mortgage = Mortgage(property_value, down_payment_pct, interest_rate, loan_term, monthly_rent, operating_expenses, vacancy_rate, investment_length)
# print(mortgage.mortgage_df)