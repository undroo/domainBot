import sys
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from models.mortgage import Mortgage
from models.loan import Loan

# Define page title and icon
st.set_page_config(page_title="Investment Property Calculator", page_icon=":money_with_wings:")

# Define page header
st.header("Investment Property Calculator")

# Collect user inputs
with st.sidebar:
    property_value = st.number_input("Enter the property value ($)", min_value=0, value=700000)
    down_payment_pct = st.number_input("Enter the down payment percentage (%)", min_value=0, max_value=100, value=20)
    interest_rate = st.number_input("Enter the interest rate (%)", value=5.5, step=0.05)
    loan_term = st.number_input("Enter the loan term (years)", min_value=1, value=30)
    monthly_rent = st.number_input("Enter the monthly rent ($)", min_value=0, value=3000, step=50)
    operating_expenses = st.number_input("Enter the operating expenses as a percentage of gross rent (%)", min_value=0, value=20)
    vacancy_rate = st.number_input("Enter the vacancy rate (%)", min_value=0, max_value=100, value=5)
    investment_length = st.number_input("Enter the investment length (years)", min_value=1, value = 10)

mortgage = Mortgage(
    property_value=property_value, 
    down_payment_pct=down_payment_pct, 
    interest_rate=interest_rate, 
    loan_term=loan_term, 
    monthly_rent=monthly_rent, 
    operating_expenses=operating_expenses, 
    vacancy_rate=vacancy_rate, 
    investment_length=investment_length
)

st.dataframe(data=mortgage.mortgage_df)

# Create a line plot of the cumulative cashflow over time
df = mortgage.mortgage_df
fig, ax = plt.subplots()
cumulative_cash_flow = mortgage.mortgage_df['net cash flow'].cumsum()
ax.plot(df.index, cumulative_cash_flow)

ax.set_xlabel('Month')
ax.set_ylabel('Cumulative Cashflow ($)')

# format x-axis to display every 12 months
ax.xaxis.set_major_locator(ticker.MultipleLocator(12))

# Display Result
st.write("### Investment Property Cashflow")
st.pyplot(fig)


fig, ax = plt.subplots()
ax.plot(mortgage.mortgage_df.index, mortgage.mortgage_df['profit'], label='Profit')
ax.plot(mortgage.mortgage_df.index, mortgage.mortgage_df['net cash flow'], label='Net Cash Flow')

ax.set_xlabel('Month')
ax.set_ylabel('Amount ($)')

# format x-axis to display every 12 months
ax.xaxis.set_major_locator(ticker.MultipleLocator(12))
ax.axhline(y=0, linestyle='--', color='grey')
ax.legend()
# Display Result
st.write("### Profit vs Cash Flow")
st.pyplot(fig)