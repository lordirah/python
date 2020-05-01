import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table
from mail import *

try:
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)
    client = gspread.authorize(creds)
    sheet = client.open("Expense_tracker").sheet1
    data = sheet.get_all_records()
    print("Data downloaded !!")
except:
    print("Error while connecting to GSheets")
    exit(1)

try:
    date_filter = input("Enter the period to parse (Mon-YYYY) : ")
    filtered_expense = [d for d in data if d['Date'] in date_filter]
    df = pd.DataFrame(filtered_expense)
    expense = df['Expense'].sum()
    income = df['Income'].sum()
    expense_df = df[df['Expense']!=0].drop(['Income','Date','Comments'], axis =1)
    income_df = df[df['Income']!=0].drop(['Expense','Date','Comments'], axis =1)
    expense_df = expense_df.groupby(['Category']).sum().reset_index()
    income_df = income_df.groupby(['Category']).sum().reset_index()
    print("Total expense for the period is ", expense)
    print("Total income for the period is ", income)
    print("Data frames formed !!")
except:
    print("Error while generating data frames !!")
    exit(1)
try:    
    plt.figure(figsize=(16,8))
    ax1 = plt.subplot(121, aspect='equal')
    df.plot(kind='pie', y = 'Expense', ax=ax1, autopct='%1.1f%%',startangle=90, shadow=False, labels=df['Category'], legend = False, fontsize=14)
    ax2 = plt.subplot(122)
    plt.axis('off')
    tbl = table(ax2, expense_df, loc='center')
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(12)
    plt.savefig('expense.png')
    print("Graph generated in the path !!")
except:
    print("Error while generating report !!")
    exit(1)
    
try:
    mail(date_filter,expense,income)
    print("Mail sent successfully")
except:
    print("Error while sending mail !!")
    exit(1)