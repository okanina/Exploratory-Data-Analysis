# importing necessary libraries.
import sqlite3
import pandas as pd

#connect to the db.
conn=sqlite3.connect("sales.db")
c=conn.cursor()

# reading the data to dataframe
pd.set_option("display.max_columns", None)
df=pd.read_csv(r"C:\Users\Cynthia\Documents\Data Science\Data\Diwali Sales Data.csv", encoding="unicode_escape")
df.rename(columns={"Age Group":"Age_Group"}, inplace=True)

# Create Table
c.execute('''DROP TABLE IF EXISTS diwaliSales''')
c.execute('''CREATE TABLE diwaliSales(User_ID INT, Cust_name TEXT, Product_ID char, 
 Gender VARCHAR, Age_Group INT, Age INT,Marital_Status BOOL, State TEXT, Zone TEXT, Occupation TEXT, Product_category TEXT, Orders INT, Amount REAL, Status TEXT, unnamed1 TEXT)''')

#  insert dataframe into db
for row in df.itertuples():
    c.execute('''INSERT INTO diwaliSales(User_ID, Cust_name, Product_ID,Gender, Age_Group, Age, Marital_Status, State, Zone, Occupation, Product_category 
            , Orders, Amount, Status, unnamed1) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
        (row.User_ID, row.Cust_name, row.Product_ID, row.Gender, row.Age_Group, 
        row.Age, row.Marital_Status, row.State, row.Zone, row.Occupation,
        row.Product_Category, row.Orders, row.Amount, row.Status, row.unnamed1
        ))
conn.commit()

