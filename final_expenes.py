import streamlit as st
import pandas as pd
import sqlite3 
import matplotlib.pyplot as plt
import seaborn as sns



conn = sqlite3.connect(r"expens.db")  

cursor = conn.cursor()

st.title("Analysing Personal Expenses")


cursor.execute('''
CREATE TABLE IF NOT EXISTS analyzing_personal_expenses (
    transaction_date TEXT,
    Category TEXT,
    Amount_Paid TEXT,
    Payment_mode TEXT,
    Descriptions TEXT,
    Cashback TEXT
)
''')

import pandas as pd
df = pd.read_csv("C:\\Users\\megal\\Downloads\\new monthly expenses-1.csv")




values_to_insert = df[['transaction_date', 'Category','Amount Paid','Payment Mode', 'Description', 'Cashback']]


cursor.executemany("""
INSERT INTO analyzing_personal_expenses(transaction_date, Category, Amount_Paid, Payment_mode, Descriptions, Cashback)
VALUES (?, ?, ?, ?, ?, ?)
""", values_to_insert.values.tolist())  


conn.commit()


cursor.execute('SELECT * FROM analyzing_personal_expenses')
rows = cursor.fetchall()
columns = [description[0] for description in cursor.description]  
table = pd.DataFrame(rows, columns=columns)
st.dataframe(table)



options = ['Total Amount','AVG Amount','Min Amount','Max Amount','Limit', 'Min cashback', 'Max cashback','Avg cashback','Total cashback','CA','Food','shop','Credit','Online','dates']
selected_option = st.sidebar.radio("Select any Sqlquery:", options)


st.write(f"You selected: {selected_option}")


if selected_option == 'Total Amount':
    cursor.execute("SELECT SUM(Amount_Paid) AS Total_Expenses FROM analyzing_personal_expenses")
    total_expenses = cursor.fetchall()
    st.write(f"Total Expenses: {total_expenses}")

if selected_option == 'AVG Amount':
    cursor.execute("SELECT AVG(Amount_Paid) FROM analyzing_personal_expenses")
    avg = cursor.fetchall()
    st.write(f"average :{avg}")



if selected_option == 'Min Amount':
    cursor.execute("SELECT MIN(Amount_Paid) AS Total_Expenses FROM analyzing_personal_expenses")
    Minimum_expenses = cursor.fetchall()
    st.write(f"Minimum Expenses: {Minimum_expenses}")

if selected_option == 'Max Amount':
    cursor.execute("SELECT MAX(Amount_Paid) AS Total_Expenses FROM analyzing_personal_expenses")
    Maximum_expenses = cursor.fetchall()
    st.write(f"Max Expenses: {Maximum_expenses}")

if selected_option == 'Limit':
    cursor.execute("SELECT * FROM analyzing_personal_expenses LIMIT 5 OFFSET 5")
    b_rows = cursor.fetchall()
    b_columns = [description[0] for description in cursor.description]
    bb = pd.DataFrame(b_rows, columns=b_columns)
    st.dataframe(bb)


if selected_option == 'Min cashback':
    cursor.execute("SELECT MIN(Cashback) FROM analyzing_personal_expenses")
    min_cashback = cursor.fetchall()
    st.write(f"Minimum Cashback: {min_cashback}")

if selected_option == 'Max cashback':
    cursor.execute("SELECT MAX(Cashback) FROM analyzing_personal_expenses")
    max_cashback = cursor.fetchall()
    st.write(f"Maximum Cashback: {max_cashback}")

if selected_option == 'Avg cashback':
    cursor.execute("SELECT AVG(Cashback) FROM analyzing_personal_expenses")
    avgcash = cursor.fetchall()
    st.write(f"average cash :{avgcash}")


if selected_option == 'Total cashback':
    cursor.execute("SELECT sum(Cashback) AS Total_CashBack FROM analyzing_personal_expenses")
    sum_cashback = cursor.fetchall()
    st.write(f"Total Cashback: {sum_cashback}")

if selected_option == 'CA':
    cursor.execute("SELECT count(Cashback),Amount_Paid FROM analyzing_personal_expenses group by Amount_Paid order by count(Cashback)")
    counts = cursor.fetchall()
    
    if counts:
        count = pd.DataFrame(counts,columns=[description[0] for description in cursor.description])
        st.dataframe(count)

    else:
        st.write("No cash transactions found for this datas")




if selected_option == 'Food':
    cursor.execute("SELECT * FROM analyzing_personal_expenses WHERE Category = 'Food' AND Payment_mode = 'Cash'")
    food_rows = cursor.fetchall()
    if food_rows:
        foods = pd.DataFrame(food_rows, columns=[description[0] for description in cursor.description])
        st.table(foods)  
    else:
        st.write("No cash transactions found for Food")


if selected_option == 'shop':
    cursor.execute("SELECT * FROM analyzing_personal_expenses WHERE Category = 'Shopping' AND Payment_mode = 'Debit card'")
    shop_rows = cursor.fetchall()
    if shop_rows:
        shops = pd.DataFrame(shop_rows, columns=[description[0] for description in cursor.description])
        st.table(shops) 
    else:
        st.write("No cash transactions found for Food")



if selected_option == 'Credit':
    cursor.execute("SELECT * FROM analyzing_personal_expenses WHERE Payment_mode = 'Credit card'")
    crads = cursor.fetchall()
    if crads:
        card = pd.DataFrame(crads, columns=[description[0] for description in cursor.description])
        st.table(card)
    else:
        st.write("No transactions found for Credit card")

if selected_option == 'Online':
    cursor.execute("SELECT * FROM analyzing_personal_expenses WHERE Payment_mode = 'Online'")
    on = cursor.fetchall()
    if on:
        ons = pd.DataFrame(on,columns=[description[0] for description in cursor.description])
        st.table(ons)
    else:
        st.write("NO transactions found for Online")

if selected_option == 'dates':
    cursor.execute("select transaction_date,sum(Amount_Paid) AS TotalAmount,sum(Cashback) AS Totalcashbacks from analyzing_personal_expenses group by transaction_date")
    date = cursor.fetchall()
    if date:
        dates = pd.DataFrame(date,columns=[description[0] for description in cursor.description])
        st.table(dates)
    else:
        st.write("NO transactions found for this transactions date")





opt = st.sidebar.radio("Select any visualizaton",options = ('pie','bars','don','bar','histogram'))

if opt == "pie":
    pi =table['Payment_mode'].value_counts()
    fig, ax = plt.subplots()
    ax = plt.pie(pi,autopct='%1.1f%%',colors=['pink','blue','pink','blue'],labels=pi.index,)
    st.title('Paymentif Mode Distribution')
    st.write(fig)

if opt == "bars":
    food_data = table[table['Category'] == 'Food']
    payment_counts = food_data['Payment_mode'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 5))  # Adjust the size as needed
    ax.bar(payment_counts.index, payment_counts.values, color=['blue', 'orange'])
    ax.set_xlabel('Payment Mode')
    ax.set_ylabel('Number of Transactions')
    ax.set_title('Number of Transactions for Food Category by Payment Mode')
    st.pyplot(fig)

if opt == "don":
    count = table['Category'].value_counts()
    fig, ax = plt.subplots()
    ax = plt.pie(count,autopct='%1.1f%%',labels=count.index)
    st.title('Categorys')
    center_circle = plt.Circle((0,0),0.50,fc = 'white')
    fig.gca().add_artist(center_circle)
    st.write(fig)
    
if opt == "bar":
    cash_counts = table[table['Payment_mode'] == 'Cash']['Category'].value_counts()
    online_counts = table[table['Payment_mode'] == 'Online']['Category'].value_counts()
    combined_counts = pd.DataFrame({
        'Cash': cash_counts,
        'Online': online_counts
    }).fillna(0) 
    fig, ax = plt.subplots(figsize=(10, 6))
    combined_counts.plot(kind='bar', ax=ax)
    ax.set_xlabel('Category')
    ax.set_ylabel('Number of Transactions')
    ax.set_title('Number of Transactions by Category and Payment Mode')
    ax.legend(title='Payment Mode')
    st.pyplot(fig)



if opt == "histogram":
    paid = table['Amount_Paid']
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(paid, bins=30, color='blue',label=paid.index) 
    ax.set_xlabel('Amount Paid')
    ax.set_ylabel('Frequency')
    ax.set_title('Histogram of Amount Paid')
    st.pyplot(fig)


table['transaction_date'] = pd.to_datetime(table['transaction_date'])
table['Amount_Paid'] = pd.to_numeric(table['Amount_Paid'], errors='coerce')
table['month'] = table['transaction_date'].dt.to_period('M')

top_categories = table.groupby('Category')['Amount_Paid'].sum().reset_index()
top_categories = top_categories.sort_values(by='Amount_Paid', ascending=False)

monthly_expenditure = table.groupby(['month', 'Category'])['Amount_Paid'].sum().unstack().fillna(0)
fig, ax = plt.subplots(figsize=(12, 6))
monthly_expenditure.plot(kind='bar', stacked=True, ax=ax)
ax.set_title('Monthly Expenditure Breakdown by Category')
ax.set_xlabel('Month')
ax.set_ylabel('Amount Paid')
st.pyplot(fig)