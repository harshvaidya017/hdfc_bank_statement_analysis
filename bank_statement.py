#importing packages required
from datetime import date, datetime
import plotly.express as px
from tabula import read_pdf
import pandas as pd
import csv
import warnings
import streamlit as st

# Suppress UserWarnings
warnings.simplefilter(action='ignore', category=UserWarning)

#reading pdf file page wise
st.write('### Visualize Your Bank Statement')
link = "C:\\Users\\LENOVO\\Downloads\\hdfc1.pdf"
dfs = read_pdf(link, pages=1)

# Save the DataFrame to a CSV file
final_df = pd.concat(dfs, ignore_index=True)
final_df.to_csv('data.csv', index=False)
df=pd.read_csv('data.csv')

#this have latest data 
final_df = pd.concat(dfs, ignore_index=True)

#for second page
df2 = read_pdf(link, pages=2)
result_dfs = [df.head(4) for df in df2]
result_df = pd.concat(result_dfs, ignore_index=True)
result_df.to_csv('data2.csv', index=False)
df2=pd.read_csv('data2.csv')

df2 = df2.T.reset_index().T.reset_index(drop=True)
df2.columns = ['Date','Narration','Chq./Ref.No.','Value Dt','Withdrawal Amt.','Col6']
df2[['Deposit Amt.', 'Closing Balance']] = df2['Col6'].str.split(' ', n=1, expand=True)

df2.to_csv('data2.csv', index=False)
df2=pd.read_csv('data2.csv')
result_df = pd.concat([final_df, df2])
result_df = result_df.drop(columns=['Col6'])
result_df.to_csv('data2.csv', index=False)
result_df=pd.read_csv('data2.csv')

# Converting the datatypes


result_df['Withdrawal Amt.'] = pd.to_numeric(result_df['Withdrawal Amt.'].str.replace(',', ''), errors='coerce')
result_df['Deposit Amt.'] = pd.to_numeric(result_df['Deposit Amt.'].str.replace(',', ''), errors='coerce')
result_df['Date'] = pd.to_datetime(result_df['Date'], format='%d/%m/%y', errors='coerce')
result_df['Date'] = pd.to_datetime(result_df['Date'], format='%y-%m-%d').dt.date
result_df['Value Dt'] = pd.to_datetime(result_df['Value Dt'].str.replace(',',''),errors='coerce')
result_df['Value Dt'] = pd.to_datetime(result_df['Value Dt'], format='%y-%m-%d').dt.date
result_df['Closing Balance'] = pd.to_numeric(result_df['Closing Balance'].str.replace(',', ''), errors='coerce')
result_df['Chq./Ref.No.'] = result_df['Chq./Ref.No.'].astype(str).str.replace(',', '', regex=True)
result_df['Narration'] = result_df['Narration'].astype(str).str.replace(',', '', regex=True)
result_df.index = range(1, len(result_df) + 1)

total_withdrawal = result_df['Withdrawal Amt.'].sum()
st.write("Total Withdrwal:" ,total_withdrawal)
total_deposit = result_df['Deposit Amt.'].sum()
st.write("Total deposit:" ,total_deposit)
st.write(f"Total Withdrawal and Deposit: Rs {total_withdrawal} - Rs {total_deposit}")
opening_balance = result_df['Closing Balance'].iloc[0] + result_df['Withdrawal Amt.'].iloc[0]
st.write(f"Closing and Opening Balance: {result_df['Closing Balance'].iloc[-2]} and {opening_balance}")
valid_dates = result_df['Date'].dropna()
total_valid_dates = len(valid_dates)
st.write(f"Total Transactions: {total_valid_dates}")
start_date = result_df['Date'].iloc[0]
end_date = result_df['Date'].loc[result_df['Date'].last_valid_index()]
st.write(f"Statement Period: {start_date} to {end_date}")
days = (end_date - start_date).days
st.write(f"Number of Days: {days}")
st.write(f"Average Withdrawal per day: {(total_withdrawal / days):.2f}")
st.write(f"Average Withdrawal per month: {total_withdrawal / (days / 30):.2f}")

# Visualization (you can customize this based on your data and preferences)
st.write("### Visualizations")
fig = px.bar(result_df, x='Date', y='Withdrawal Amt.', title='Withdrawals Over Time')
st.plotly_chart(fig)

time_frame = list(result_df['Date'])
balance = list(result_df['Closing Balance'])
line = pd.DataFrame({'Closing Balance': balance}, index=time_frame)
st.subheader('Balance Trend')
st.line_chart(line, use_container_width=True)
st.dataframe(df, use_container_width=True)

withdrawal = list(result_df['Withdrawal Amt.'])
withdrawal = [float(value.replace(',', '')) if isinstance(value, str) else float(value) for value in withdrawal]
for i in range(1, len(withdrawal)):
    withdrawal[i] = withdrawal[i] + withdrawal[i - 1]

deposited = list(result_df['Deposit Amt.'])
deposited = [float(value.replace(',', '')) if isinstance(value, str) else float(value) for value in deposited]
for i in range(1, len(deposited)):
    deposited[i] = deposited[i] + deposited[i - 1]

val = st.radio('Select', ('Withdrawal', 'Deposited'))
if val == 'Withdrawal':
     withdraw_line = pd.DataFrame({'Withdrawal Amt.': withdrawal}, index=time_frame)
     
     fig = px.bar(df, x='Date', y='Withdrawal Amt.', title='Withdrawals')
     st.plotly_chart(fig, use_container_width=True)
     figs = px.scatter(df, x='Date', y='Withdrawal Amt.', title='Withdrawals')
     st.plotly_chart(figs, use_container_width=True)
     

elif val == 'Deposited':
     deposit_line = pd.DataFrame({'Deposit Amt.': deposited}, index=time_frame)
     fig = px.bar(df, x='Date', y='Deposit Amt.', title='Deposits')
     st.plotly_chart(fig, use_container_width=True)
     figs = px.scatter(df, x='Date', y='Deposit Amt.', title='Deposits')
     st.plotly_chart(figs, use_container_width=True)
     