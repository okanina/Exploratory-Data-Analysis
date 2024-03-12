import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sqlite3, config

def wrangle(db_path):

    conn=sqlite3.connect(db_path)

    query="""SELECT * FROM 'diwaliSales'"""

    df=pd.read_sql(query, conn, index_col="User_ID")

    return df

st.set_page_config(page_title="DiwaliSales", page_icon=":bar_chart:", layout="wide")
st.title(":bar_chart: Diwali Sales EDA")

f1=st.file_uploader("Upload a file", type=["csv", "xlsx"])
if f1 is not None and type=="csv":            
        filename=f1.name
        st.write(filename)
        df=pd.read_csv()

elif f1 is not None and type=="xlsx":
        filename=f1.name
        st.write(filename)
        df=pd.read_xlsx(filename)
else:
        
        df=wrangle(config.db_name)

st.sidebar.header("Filter the data")

# region
region=st.sidebar.multiselect("Please select a region", df["Zone"].unique())
if not region:
       df2=df.copy()
else:
       df2=df[df["Zone"].isin(region)]

#state
state =st.sidebar.multiselect("Please select the state", df["State"].unique())
if not state:
       df3=df2.copy()
else:
       df3=df2[df2["State"].isin(state)]

if not region and not state:
       filtered_df=df

elif not state:
       filtered_df=df[df["Zone"].isin(region)]

elif not region:
       filtered_df=df[df["State"].isin(state)]

elif region and state:
       filtered_df=df3[df["State"].isin(state) & df3["Zone"].isin(region)]


age_group=filtered_df.groupby(["Age_Group", "Gender"], as_index=False)["Amount"].mean().sort_values(by="Amount", ascending=False)
male, female=filtered_df["Gender"].value_counts(normalize=True) * 100

st.subheader("Sales by Gender")
fig=px.pie(filtered_df, values=[male, female], names=["Female", "Male"], hole=0.5)
fig.update_traces(text=filtered_df["Gender"], textposition="outside")
st.plotly_chart(fig, use_container_width=True, )


st.subheader("Sales by Age Group")
fig=px.bar(filtered_df, x="Age_Group", y="Amount", template="seaborn")
plt.xticks()
st.plotly_chart(fig, use_container_with=True, height=200)

 
col1, col2=st.columns(2)

category_df=filtered_df.groupby(["Product_category"], as_index=False)["Amount"].sum()

with col1:
       st.subheader("Catagory Sales")
       fig=px.bar(category_df, x="Product_category", y="Amount", template="seaborn")
       st.plotly_chart(fig, use_container_with=True, height=200)

with col2:
       st.subheader("Region Sales")
       fig=px.pie(filtered_df, values="Amount", names="Zone", hole=0.5)
       fig.update_traces(text=filtered_df["Zone"], textposition="outside")
       st.plotly_chart(fig, use_container_width=True, )


st.subheader("Summary Statistics")
st.write(df.describe())
    
