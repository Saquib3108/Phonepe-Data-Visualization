import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector as sql
import mysql
import pandas as pd
import plotly.express as px
import requests
import json
from PIL import Image


#DataFrame Creation

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="phonepe_db")

cursor=mydb.cursor()
cursor = mydb.cursor(buffered=True)

#aggregated_insurance_df
cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1 = cursor.fetchall()

Aggre_insurance=pd.DataFrame(table1,columns=("states", "years", "quarter", "transaction_type",
                                             "transaction_count", "transaction_amount"))

#aggregated_transaction_df
cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2 = cursor.fetchall()

Aggre_transaction=pd.DataFrame(table2,columns=("states", "years", "quarter", "transaction_type",
                                             "transaction_count", "transaction_amount"))


#aggregated_user_df
cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3 = cursor.fetchall()

Aggre_user=pd.DataFrame(table3,columns=("states", "years", "quarter", "Brands",
                                             "transaction_count", "Percentage"))


#map_insurance_df
cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4 = cursor.fetchall()

map_insurance=pd.DataFrame(table4,columns=("states", "years", "quarter", "Districts",
                                             "transaction_count", "transaction_amount"))

#map_transaction_df
cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5 = cursor.fetchall()

map_transaction=pd.DataFrame(table5,columns=("states", "years", "quarter", "Districts",
                                             "transaction_count", "transaction_amount"))

#map_user_df
cursor.execute("SELECT * FROM map_users")
mydb.commit()
table6 = cursor.fetchall()

map_users=pd.DataFrame(table6,columns=("states", "years", "quarter", "Districts",
                                    "RegisteredUsers", "AppOpens"))


#top_insurance_df
cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7 = cursor.fetchall()

top_insurance=pd.DataFrame(table7,columns=("states", "years", "quarter", "Pincodes",
                                    "transaction_count", "transaction_amount"))

#top_transaction_df
cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8 = cursor.fetchall()

top_transaction=pd.DataFrame(table8,columns=("states", "years", "quarter", "Pincodes",
                                    "transaction_count", "transaction_amount"))


#top_user_df
cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9 = cursor.fetchall()

top_user=pd.DataFrame(table9,columns=("states", "years", "quarter", "Pincodes",
                                    "RegisteredUsers"))






def Transaction_amount_count_Y(df, year):
    tacy =df[df["years"]==year]
    tacy.reset_index(drop=True, inplace=True) 


    tacyg = tacy.groupby("states")[["transaction_count", "transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    
    
    col1,col2 = st.columns(2)
    
    with col1:


        fig_amount = px.bar(tacyg, x="states", y="transaction_amount", title=f"{year} TRANSACTION_AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Agsunset, height=650, width= 600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count = px.bar(tacyg, x="states", y="transaction_count", title=f"{year} TRANSACTION_COUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=650, width=600)
        st.plotly_chart(fig_count)
        
        
    col1,col2= st.columns(2) 
    with col1:
        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

        response= requests.get(url)
        data1= json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()


        fig_india_1= px.choropleth(tacyg, geojson=data1, locations="states", featureidkey= "properties.ST_NM",
                                color= "transaction_amount", color_continuous_scale=px.colors.sequential.Rainbow,
                                range_color= (tacyg["transaction_amount"].min(), tacyg["transaction_amount"].max()),
                                hover_name= "states", title =f"{year} TRANSACTION_AMOUNT", fitbounds="locations",
                                height=600, width= 600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)
        
    with col2:
        fig_india_2= px.choropleth(tacyg, geojson=data1, locations="states", featureidkey= "properties.ST_NM",
                                color= "transaction_count", color_continuous_scale=px.colors.sequential.Rainbow,
                                range_color= (tacyg["transaction_count"].min(), tacyg["transaction_count"].max()),
                                hover_name= "states", title =f"{year} TRANSACTION_COUNT", fitbounds="locations",
                                height=600, width= 600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)
    return tacy


def Transaction_amount_count_Y_Q(df, quarter):
    tacy =df[df["quarter"]== quarter]
    tacy.reset_index(drop=True, inplace=True)


    tacyg = tacy.groupby("states")[["transaction_count", "transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    
    col1,col2 =st.columns(2)
    with col1:
        
        fig_amount = px.bar(tacyg, x="states", y="transaction_amount", title=f"{tacy['years'].unique()} YEAR {quarter} QUARTER TRANSACTION_AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Agsunset, height=650, width= 600)
        st.plotly_chart(fig_amount)


    with col2:
        
        fig_count = px.bar(tacyg, x="states", y="transaction_count", title=f"{tacy['years'].unique()} YEAR {quarter} QUARTER TRANSACTION_COUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=650, width= 600)
        st.plotly_chart(fig_count)
    
    
    col1,col2= st.columns(2)
    with col1:
        
        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

        response= requests.get(url)
        data1= json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])


        states_name.sort()


        fig_india_1= px.choropleth(tacyg, geojson=data1, locations="states", featureidkey= "properties.ST_NM",
                                color= "transaction_amount", color_continuous_scale=px.colors.sequential.Rainbow,
                                range_color= (tacyg["transaction_amount"].min(), tacyg["transaction_amount"].max()),
                                hover_name= "states", title =f"{tacy['years'].unique()} YEAR {quarter} QUARTER TRANSACTION_AMOUNT", fitbounds="locations",
                                height=600, width= 600)
        
        fig_india_1.update_geos(visible=False)

        st.plotly_chart(fig_india_1)
    with col2:
    
        fig_india_2= px.choropleth(tacyg, geojson=data1, locations="states", featureidkey= "properties.ST_NM",
                                color= "transaction_count", color_continuous_scale=px.colors.sequential.Rainbow,
                                range_color= (tacyg["transaction_count"].min(), tacyg["transaction_count"].max()),
                                hover_name= "states", title =f"{tacy['years'].unique()} YEAR {quarter} QUARTER TRANSACTION_COUNT", fitbounds="locations",
                                height=600, width= 600)
        
        fig_india_2.update_geos(visible=False)

        st.plotly_chart(fig_india_2)
        
    return tacy
        
def Agg_Tran_Transaction_type(df, state):

    tacy =df[df["states"]== state]
    tacy.reset_index(drop=True, inplace=True)

    tacyg = tacy.groupby("transaction_type")[["transaction_count", "transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    
    
    col1, col2 = st.columns(2)
    with col1:
        
        fig_pie_1 = px.pie(data_frame= tacyg, names= "transaction_type", values= "transaction_amount",
                            width=600, title= f"{state.upper()} TRANSACTION AMOUNT", hole= 0.5)

        st.plotly_chart(fig_pie_1)

    with col2:
        
        fig_pie_2 = px.pie(data_frame= tacyg, names= "transaction_type", values= "transaction_count",
                            width=600, title= f"{state.upper()} TRANSACTION COUNT", hole= 0.5)

        st.plotly_chart(fig_pie_2)  
        
#Aggregated_user_Analysis_1

def Aggre_user_plot_1(df, year):
    agguy= df[df["years"]== year]
    agguy.reset_index(drop= True, inplace= True)

    agguyg = pd.DataFrame(agguy.groupby("Brands")[["transaction_count"]].sum())
    agguyg.reset_index(inplace= True)


    fig_bar_1 = px.bar(agguyg, x="Brands", y= "transaction_count", title= f"{year} BRANDS AND TRANSACTION COUNT", width= 900,
                    color_discrete_sequence= px.colors.sequential.haline_r, hover_name= "Brands")

    st.plotly_chart(fig_bar_1)
    
    return agguy


#Aggre_user_Analysis_2

def Aggre_user_plot2(df, quarter):
    agguq= df[df["quarter"]== quarter]
    agguq.reset_index(drop= True, inplace= True)


    agguqg = pd.DataFrame(agguq.groupby("Brands")["transaction_count"].sum())
    agguqg.reset_index(inplace= True)

    fig_bar_1 = px.bar(agguqg, x="Brands", y= "transaction_count", title= f"{quarter} QUARTER, BRANDS AND TRANSACTION COUNT", width= 900,
                        color_discrete_sequence= px.colors.sequential.Bluered_r, hover_name= "Brands")

    st.plotly_chart(fig_bar_1)

    return agguq


#Aggregated_user_Analysis_3

def Aggre_user_plot_3(df, state):

    agguqs = df[df["states"]== state]
    agguqs.reset_index(drop= True, inplace= True)


    fig_line_1 = px.line(agguqs, x= "Brands", y= "transaction_count", hover_data = "Percentage",
                        title = f"{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE", width= 900, markers= True)

    st.plotly_chart(fig_line_1)
    

#Map_insurance_district
def Map_insure_Districts(df, state):

    tacy =df[df["states"]== state]
    tacy.reset_index(drop=True, inplace=True)

    tacyg = tacy.groupby("Districts")[["transaction_count", "transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
            
        fig_bar_1 = px.bar(tacyg, x = "transaction_amount", y= "Districts", orientation= "h", height= 600,
                            title= f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence=px.colors.sequential.Mint_r)

        st.plotly_chart(fig_bar_1)
        
    with col2:
            
        fig_bar_2 = px.bar(tacyg, x = "transaction_count", y= "Districts", orientation= "h", height= 600,
                            title= f"{state.upper()} DISTRICT AND TRANSACTION COUNT", color_discrete_sequence=px.colors.sequential.Bluered_r)

        st.plotly_chart(fig_bar_2)
        
#Map_user_plot_1
def map_users_plot_1(df, year):
    muy= df[df["years"]== year]
    muy.reset_index(drop= True, inplace= True)

    muyg = muy.groupby("states")[["RegisteredUsers", "AppOpens"]].sum()
    muyg.reset_index(inplace= True)

    fig_line_1 = px.line(muyg, x= "states", y= ["RegisteredUsers", "AppOpens"],
                            title = f"{year} REGISTERED USER, APPOPENS", width= 900, height=800, markers= True)

    st.plotly_chart(fig_line_1)
    
    return muy


#Map_user_plot_2
def map_users_plot_2(df, quarter):
    muyq= df[df["quarter"]== quarter]
    muyq.reset_index(drop= True, inplace= True)

    muyqg = muyq.groupby("states")[["RegisteredUsers", "AppOpens"]].sum()
    muyqg.reset_index(inplace= True)

    fig_line_1 = px.line(muyqg, x= "states", y= ["RegisteredUsers", "AppOpens"],
                            title = f"{df['years'].min()} YEARS {quarter} QUARTER REGISTERED USER, APPOPENS", width= 900, height=800, markers= True,
                            color_discrete_sequence= px.colors.sequential.BuPu_r)

    st.plotly_chart(fig_line_1)
    
    return muyq

#map_user_plot_3
def map_users_plot_3(df, states):
    muyqs= df[df["states"]== states]
    muyqs.reset_index(drop= True, inplace= True)
    
    col1,col2 =st.columns(2)
    with col1:
        fig_map_user_bar_1 =px.bar(muyqs, x= "RegisteredUsers", y="Districts", orientation= "h",
                                title= f"{states.upper()} REGISTERED USER", height= 800, color_discrete_sequence= px.colors.sequential.Brwnyl_r)

        st.plotly_chart(fig_map_user_bar_1)
    with col2:
        fig_map_user_bar_2 =px.bar(muyqs, x= "AppOpens", y="Districts", orientation= "h",
                                title= f"{states.upper()} APPOPENS", height= 800, color_discrete_sequence= px.colors.sequential.Rainbow_r)

        st.plotly_chart(fig_map_user_bar_2)
        
        
        
#top_insurance_plot_1
def Top_insurance_plot_1(df, state):
    tiy= df[df["states"]== state]
    tiy.reset_index(drop= True, inplace= True)
    
    col1, col2 = st.columns(2)
    with col1:

        fig_top_insure_bar_1 =px.bar(tiy, x= "quarter", y="transaction_amount", hover_data= "Pincodes",
                                    title= "TRANSACTION AMOUNT", height= 600, width=550, color_discrete_sequence= px.colors.sequential.Emrld_r)

        st.plotly_chart(fig_top_insure_bar_1)
    with col2:
        fig_top_insure_bar_2 =px.bar(tiy, x= "quarter", y="transaction_count", hover_data= "Pincodes",
                                    title= "TRANSACTION COUNT", height= 600, width=550, color_discrete_sequence= px.colors.sequential.GnBu_r)

        st.plotly_chart(fig_top_insure_bar_2)


def top_user_plot_1(df, year):
    tpuy= df[df["years"]== year]
    tpuy.reset_index(drop= True, inplace= True)

    tpuyg = pd.DataFrame(tpuy.groupby(["states", "quarter"])[["RegisteredUsers"]].sum())
    tpuyg.reset_index(inplace= True)

    fig_top_user_plot_1= px.bar(tpuyg, x= "states", y= "RegisteredUsers", color="quarter", width= 900, height = 800, hover_name = "states",
                                title = f"{year} REGISTERED USERS",  color_discrete_sequence = px.colors.sequential.Burgyl)

    st.plotly_chart(fig_top_user_plot_1)
    
    return tpuy

#Top_user_plot_2
def top_user_plot_2(df, state):
    tpuys= df[df["states"]== state]
    tpuys.reset_index(drop= True, inplace= True)

    fig_top_user_plot_2= px.bar(tpuys, x= "quarter", y= "RegisteredUsers", title= "REGISTERED USERS, PINCODES, QUARTER",
                                width= 1000, height=800, color= "RegisteredUsers", hover_data= "Pincodes",
                                color_continuous_scale= px.colors.sequential.Magenta)

    st.plotly_chart(fig_top_user_plot_2)


#sql_connection_1

def top_chart_transaction_amount(table_name):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        database="phonepe_db")

    cursor=mydb.cursor()
    cursor = mydb.cursor(buffered=True)

    query1 = f'''select states, sum(transaction_amount) as transaction_amount 
                from {table_name}
                group by states
                order by transaction_amount desc limit 10;'''
                
    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns=("states", "transaction_amount"))
    
    col1, col2 = st.columns(2)
    with col1:

        fig_amount_plot_1 = px.bar(df_1, x="states", y="transaction_amount", title= "TOP 10 OF TRANSACTION AMOUNT", hover_name= "states",
                                color_discrete_sequence=px.colors.sequential.Agsunset, height=650, width= 600)
        st.plotly_chart(fig_amount_plot_1)


    query2 = f'''select states, sum(transaction_amount) as transaction_amount 
                from {table_name}
                group by states
                order by transaction_amount limit 10;'''
                
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns=("states", "transaction_amount"))

    with col2:
        fig_amount_plot_2 = px.bar(df_2, x="states", y="transaction_amount", title= "LAST 10 OF TRANSACTION AMOUNT", hover_name= "states",
                                color_discrete_sequence=px.colors.sequential.algae_r, height=650, width= 600)
        st.plotly_chart(fig_amount_plot_2)

    #plot3

    query3 = f'''select states, avg(transaction_amount) as transaction_amount 
                from {table_name}
                group by states
                order by transaction_amount;'''
                
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=("states", "transaction_amount"))

    fig_amount_plot_3 = px.bar(df_3, y="states", x="transaction_amount", title= "AVERAGE OF TRANSACTION AMOUNT", hover_name= "states", orientation= "h",
                            color_discrete_sequence=px.colors.sequential.Bluered_r, height=750, width= 950)
    st.plotly_chart(fig_amount_plot_3)
    
    
    #sql connection_2

def top_chart_transaction_count(table_name):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        database="phonepe_db")

    cursor=mydb.cursor()
    cursor = mydb.cursor(buffered=True)

    query1 = f'''select states, sum(transaction_count) as transaction_count
                from {table_name}
                group by states
                order by transaction_count desc limit 10;'''
                
    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns=("states", "transaction_count"))
    
    col1, col2 = st.columns(2)
    with col1:
        
        fig_amount_plot_1 = px.bar(df_1, x="states", y="transaction_count", title= "TOP 10 OF TRANSACTION COUNT", hover_name= "states",
                                color_discrete_sequence=px.colors.sequential.Agsunset, height=650, width= 600)
        st.plotly_chart(fig_amount_plot_1)


    query2 = f'''select states, sum(transaction_count) as transaction_count 
                from {table_name}
                group by states
                order by transaction_amount limit 10;'''
                
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns=("states", "transaction_count"))

    with col2:
        fig_amount_plot_2 = px.bar(df_2, x="states", y="transaction_count", title= "LAST 10 OF TRANSACTION COUNT", hover_name= "states",
                                color_discrete_sequence=px.colors.sequential.algae_r, height=650, width= 600)
        st.plotly_chart(fig_amount_plot_2)

    #plot3

    query3 = f'''select states, avg(transaction_count) as transaction_count 
                from {table_name}
                group by states
                order by transaction_count;'''
                
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=("states", "transaction_count"))

    fig_amount_plot_3 = px.bar(df_3, y="states", x="transaction_count", title= "AVERAGE OF TRANSACTION COUNT", hover_name= "states", orientation= "h",
                            color_discrete_sequence=px.colors.sequential.Bluered_r, height=750, width= 950)
    st.plotly_chart(fig_amount_plot_3)


#sql_connection_3

def top_chart_registered_user(table_name, state):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        database="phonepe_db")

    cursor=mydb.cursor()
    cursor = mydb.cursor(buffered=True)

    query1 = f'''select Districts, sum(RegisteredUsers) As RegisteredUser
                from {table_name} where states= '{state}'
                group by Districts
                order by RegisteredUser desc
                limit 10;'''
                
    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns=("Districts", "RegisteredUser"))
    
    col1, col2 = st.columns(2)
    with col1:

        fig_amount_plot_1 = px.bar(df_1, x="Districts", y="RegisteredUser", title= "TOP 10 OF REGISTERED USER", hover_name= "Districts",
                                color_discrete_sequence=px.colors.sequential.Agsunset, height=650, width= 600)
        st.plotly_chart(fig_amount_plot_1)


    query2 = f'''select Districts, sum(RegisteredUsers) As RegisteredUser
                from {table_name} where states= '{state}'
                group by Districts
                order by RegisteredUser asc
                limit 10;'''
                
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns=("Districts", "RegisteredUser"))
    
    with col2:

        fig_amount_plot_2 = px.bar(df_2, x="Districts", y="RegisteredUser", title= "LAST 10 OF REGISTERED USER", hover_name= "Districts",
                                color_discrete_sequence=px.colors.sequential.algae_r, height=650, width= 600)
        st.plotly_chart(fig_amount_plot_2)

    #plot3

    query3 = f'''select Districts, avg(RegisteredUsers) As RegisteredUser
                from {table_name} where states= '{state}'
                group by Districts
                order by RegisteredUser;'''

    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=("Districts", "RegisteredUser"))

    fig_amount_plot_3 = px.bar(df_3, y="Districts", x="RegisteredUser", title= "AVERAGE OF REGISTERED USER", hover_name= "Districts", orientation= "h",
                            color_discrete_sequence=px.colors.sequential.Bluered_r, height=800, width= 1000 )
    st.plotly_chart(fig_amount_plot_3)


#sql_connection_4

def top_chart_AppOpens(table_name, state):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        database="phonepe_db")

    cursor=mydb.cursor()
    cursor = mydb.cursor(buffered=True)

    query1 = f'''select Districts, sum(AppOpens) As AppOpens
                from {table_name} where states= '{state}'
                group by Districts
                order by AppOpens desc
                limit 10;'''
                
    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns=("Districts", "AppOpens"))

    col1, col2 = st.columns(2)
    with col1:
        
        fig_amount_plot_1 = px.bar(df_1, x="Districts", y="AppOpens", title= "TOP 10 OF APPOPENS", hover_name= "Districts",
                                color_discrete_sequence=px.colors.sequential.Agsunset, height=650, width= 600)
        st.plotly_chart(fig_amount_plot_1)


    query2 = f'''select Districts, sum(AppOpens) As AppOpens
                from {table_name} where states= '{state}'
                group by Districts
                order by AppOpens asc
                limit 10;'''
                
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns=("Districts", "AppOpens"))

    with col2:
        
        fig_amount_plot_2 = px.bar(df_2, x="Districts", y="AppOpens", title= "LAST 10 OF APPOPENS", hover_name= "Districts",
                                color_discrete_sequence=px.colors.sequential.algae_r, height=650, width= 600)
        st.plotly_chart(fig_amount_plot_2)

    #plot3

    query3 = f'''select Districts, avg(AppOpens) As AppOpens
                from {table_name} where states= '{state}'
                group by Districts
                order by AppOpens;'''

    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=("Districts", "AppOpens"))

    fig_amount_plot_3 = px.bar(df_3, y="Districts", x="AppOpens", title= "AVERAGE OF APPOPENS", hover_name= "Districts", orientation= "h",
                            color_discrete_sequence=px.colors.sequential.Bluered_r, height=800, width= 1000 )
    st.plotly_chart(fig_amount_plot_3)


#sql_connection_5

def top_chart_registered_user_1(table_name):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        database="phonepe_db")

    cursor=mydb.cursor()
    cursor = mydb.cursor(buffered=True)

    query1 = f'''select states, sum(RegisteredUsers) As RegisteredUsers from {table_name}
                group by states
                order by RegisteredUsers desc
                limit 10;'''
                
    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns=("states", "RegisteredUsers"))

    col1, col2 = st.columns(2)
    with col1:
    
        fig_amount_plot_1 = px.bar(df_1, x="states", y="RegisteredUsers", title= "TOP 10 OF REGISTERED USERS", hover_name= "states",
                                color_discrete_sequence=px.colors.sequential.Agsunset, height=650, width= 600)
        st.plotly_chart(fig_amount_plot_1)


    query2 = f'''select states, sum(RegisteredUsers) As RegisteredUsers from {table_name}
                group by states
                order by RegisteredUsers asc
                limit 10;'''
                
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns=("states", "RegisteredUsers"))

    with col2:
        
        fig_amount_plot_2 = px.bar(df_2, x="states", y="RegisteredUsers", title= "LAST 10 OF REGISTERED USERS", hover_name= "states",
                                color_discrete_sequence=px.colors.sequential.algae_r, height=650, width= 600)
        st.plotly_chart(fig_amount_plot_2)

    #plot3

    query3 = f'''select states, avg(RegisteredUsers) As RegisteredUsers from {table_name}
                group by states
                order by RegisteredUsers;'''

    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=("states", "RegisteredUsers"))

    fig_amount_plot_3 = px.bar(df_3, y="states", x="RegisteredUsers", title= "AVERAGE OF REGISTERED USERS", hover_name= "states", orientation= "h",
                            color_discrete_sequence=px.colors.sequential.Bluered_r, height=800, width= 1000 )
    st.plotly_chart(fig_amount_plot_3)




# Streamlit Part

st.set_page_config(layout="wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:
    
    select=option_menu("Main menu",["HOME", "DATA EXPLORATION", "TOP CHARTS"])
if select=="HOME":
    
    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
        
    with col2:
        
        st.image(Image.open(r"C:\Users\DELL\Documents\Capstone Project\download.jpg"),width=500)
        
    col3,col4= st.columns(2)
    
    with col3:
        st.image(Image.open(r"C:\Users\DELL\Documents\Capstone Project\download (1).jpg"),width=450)

    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")    
        
    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        
        st.image(Image.open(r"C:\Users\DELL\Documents\Capstone Project\download (2).jpg"),width= 500)

elif select =="DATA EXPLORATION":
    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])
    with tab1:
        
        method =st.radio("Select the method", ["Insurance Analysis", "Transaction Analysis", "User Analysis"])
        
        if method=="Insurance Analysis":
            
            col1,col2=st.columns(2)
            with col1:
                
                years=st.slider("Select The Year", Aggre_insurance["years"].min(), Aggre_insurance["years"].max(), Aggre_insurance["years"].min())
            tac_Y= Transaction_amount_count_Y(Aggre_insurance, years)
            
            col1, col2 = st.columns(2)
            with col1:
                
                quarter=st.slider("Select The quarter", tac_Y["quarter"].min(), tac_Y["quarter"].max(), tac_Y["quarter"].min())
            Transaction_amount_count_Y_Q(tac_Y, quarter)
            
            
        elif method=="Transaction Analysis":
            
            col1,col2=st.columns(2)
            with col1:
                
                years=st.slider("Select The Year", Aggre_transaction["years"].min(), Aggre_transaction["years"].max(), Aggre_transaction["years"].min())
            Agg_trans_tac_Y= Transaction_amount_count_Y(Aggre_transaction, years)
            
            col1,col2=st.columns(2)
            with col1: 
                
                states = st.selectbox("Select The State", Agg_trans_tac_Y["states"].unique())

            Agg_Tran_Transaction_type(Agg_trans_tac_Y, states) 
            
            col1, col2 = st.columns(2)
            with col1:
                
                quarter=st.slider("Select The quarter", Agg_trans_tac_Y["quarter"].min(), Agg_trans_tac_Y["quarter"].max(), Agg_trans_tac_Y["quarter"].min())
            Agg_trans_tac_Y_Q= Transaction_amount_count_Y_Q(Agg_trans_tac_Y, quarter)
            
            col1,col2=st.columns(2)
            with col1: 
                
                states = st.selectbox("Select The State_ty", Agg_trans_tac_Y_Q["states"].unique())

            Agg_Tran_Transaction_type(Agg_trans_tac_Y_Q, states)
            
        elif method=="User Analysis":
            
            col1,col2=st.columns(2)
            with col1:
                years=st.slider("Select The Year", Aggre_user["years"].min(), Aggre_user["years"].max(), Aggre_user["years"].min())
            Aggre_user_Y = Aggre_user_plot_1(Aggre_user, years)
            
            col1, col2 = st.columns(2)
            with col1:
                
                quarter=st.slider("Select The quarter", Aggre_user_Y["quarter"].min(), Aggre_user_Y["quarter"].max(), Aggre_user_Y["quarter"].min())
            Aggre_user_Y_Q= Aggre_user_plot2(Aggre_user_Y, quarter)
            
            
            col1,col2=st.columns(2)
            with col1: 
                
                states = st.selectbox("Select The State", Aggre_user_Y_Q["states"].unique())

            Aggre_user_plot_3(Aggre_user_Y_Q, states)  
            
    with tab2:
        
        method2=st.radio("Select the method", ["Map Insurance", "Map Transaction", "Map User"])  
        
        if method2=="Map Insurance":
            
            col1,col2=st.columns(2)
            with col1:
                
                years=st.slider("Select The Year_map_insurance", map_insurance["years"].min(), map_insurance["years"].max(), map_insurance["years"].min())
            map_insure_tac_Y= Transaction_amount_count_Y(map_insurance, years)
            
            
            col1,col2=st.columns(2)
            with col1: 
                
                states = st.selectbox("Select The State_map_insurance", map_insure_tac_Y["states"].unique())

            Map_insure_Districts(map_insure_tac_Y, states)
            
            
            col1, col2 = st.columns(2)
            with col1:
                
                quarter=st.slider("Select The quarter_map_insurance", map_insure_tac_Y["quarter"].min(), map_insure_tac_Y["quarter"].max(), map_insure_tac_Y["quarter"].min())
            map_insure_tac_Y_Q= Transaction_amount_count_Y_Q(map_insure_tac_Y, quarter)
            
            col1,col2=st.columns(2)
            with col1: 
                
                states = st.selectbox("Select The State_ty", map_insure_tac_Y_Q["states"].unique())

            Map_insure_Districts(map_insure_tac_Y_Q, states)
            
        
        elif method2=="Map Transaction":
            
            col1,col2=st.columns(2)
            with col1:
                
                years=st.slider("Select The Year", map_transaction["years"].min(), map_transaction["years"].max(), map_transaction["years"].min())
            map_trans_tac_Y= Transaction_amount_count_Y(map_transaction, years)
            
            col1,col2=st.columns(2)
            with col1: 
                
                states = st.selectbox("Select The State_map_transaction", map_trans_tac_Y["states"].unique())

            Map_insure_Districts(map_trans_tac_Y, states)
            
            
            col1, col2 = st.columns(2)
            with col1:
                
                quarter=st.slider("Select The quarter_mt", map_trans_tac_Y["quarter"].min(), map_trans_tac_Y["quarter"].max(), map_trans_tac_Y["quarter"].min())
            map_trans_tac_Y_Q= Transaction_amount_count_Y_Q(map_trans_tac_Y, quarter)
            
            col1,col2=st.columns(2)
            with col1: 
                
                states = st.selectbox("Select The State_ty", map_trans_tac_Y_Q["states"].unique())

            Map_insure_Districts(map_trans_tac_Y_Q, states)
            
            
        
        elif method2=="Map User":
            
            col1,col2=st.columns(2)
            with col1:
                
                years=st.slider("Select The Year_map_user", map_users["years"].min(), map_users["years"].max(), map_users["years"].min())
            map_user_Y = map_users_plot_1(map_users, years)
            
            
            col1, col2 = st.columns(2)
            with col1:
                
                quarter=st.slider("Select The quarter_map_user", map_user_Y["quarter"].min(), map_user_Y["quarter"].max(), map_user_Y["quarter"].min())
            map_user_Y_Q= map_users_plot_2(map_user_Y, quarter)
            
            
            col1,col2=st.columns(2)
            with col1: 
                
                states = st.selectbox("Select The State_map_user", map_user_Y_Q["states"].unique())

            map_users_plot_3(map_user_Y_Q, states)

    with tab3:
        
        method3=st.radio("Select the method", ["Top Insurance", "Top Transaction", "Top User"])  
        
        if method3=="Top Insurance":
            
            col1,col2=st.columns(2)
            with col1:
                
                years=st.slider("Select The Year_top_insurance", top_insurance["years"].min(), top_insurance["years"].max(), top_insurance["years"].min())
            top_insure_tac_Y= Transaction_amount_count_Y(top_insurance, years)
            
            col1,col2=st.columns(2)
            with col1: 
                
                states = st.selectbox("Select The State_top_insurance", top_insure_tac_Y["states"].unique())

            Top_insurance_plot_1(top_insure_tac_Y, states)
            
            col1, col2 = st.columns(2)
            with col1:
                
                quarter=st.slider("Select The quarter_top_insurance", top_insure_tac_Y["quarter"].min(), top_insure_tac_Y["quarter"].max(), top_insure_tac_Y["quarter"].min())
            top_insure_tac_Y_Q= Transaction_amount_count_Y_Q(top_insure_tac_Y, quarter)
            
        
        elif method3=="Top Transaction":
            col1,col2=st.columns(2)
            with col1:
                
                years=st.slider("Select The Year_top_transaction", top_transaction["years"].min(), top_transaction["years"].max(), top_transaction["years"].min())
            top_trans_tac_Y= Transaction_amount_count_Y(top_transaction, years)
            
            col1,col2=st.columns(2)
            with col1: 
                
                states = st.selectbox("Select The State_top_transaction", top_trans_tac_Y["states"].unique())

            Top_insurance_plot_1(top_trans_tac_Y, states)
            
            col1, col2 = st.columns(2)
            with col1:
                
                quarter=st.slider("Select The quarter_top_transaction", top_trans_tac_Y["quarter"].min(), top_trans_tac_Y["quarter"].max(), top_trans_tac_Y["quarter"].min())
            top_trans_tac_Y_Q= Transaction_amount_count_Y_Q(top_trans_tac_Y, quarter)
        
        elif method3=="Top User":
            
            col1,col2=st.columns(2)
            with col1:
                
                years=st.slider("Select The Year_top_users", top_user["years"].min(), top_user["years"].max(), top_user["years"].min())
            top_user_Y= top_user_plot_1(top_user, years)
            
            col1,col2=st.columns(2)
            with col1: 
                
                states = st.selectbox("Select The State_top_users", top_user_Y["states"].unique())

            top_user_plot_2(top_user_Y, states)

elif select =="TOP CHARTS":
    
    question = st.selectbox("Select the Questions",["1. Transaction Amount and count of Aggregated Insurance",
                                                    "2. Transaction Amount and count of map Insurance",
                                                    "3. Transaction Amount and count of Top Insurance"
                                                    "4. Transaction Amount and count of Aggregated Transaction",
                                                    "5. Transaction Amount and count of Map Transaction",
                                                    "6. Transaction Amount and count of Top Transaction",
                                                    "7. Transaction count of Aggregated User",
                                                    "8. Registered users of Map Users",
                                                    "9. App opens of Map users",
                                                    "10.Registered users of Top Users"])
    
    if question == "1. Transaction Amount and count of Aggregated Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_insurance")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_insurance")
        
        
    elif question == "2. Transaction Amount and count of map Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_insurance")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_insurance")
        
    elif question == "3. Transaction Amount and count of Top Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_insurance")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_insurance") 
    
        
    elif question == "4. Transaction Amount and count of Aggregated Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction")
        
        
    elif question == "5. Transaction Amount and count of Map Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction")
        
        
    elif question == "6. Transaction Amount and count of Top Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction")
        
        
    elif question == "7. Transaction count of Aggregated User":
    
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user")
        
        
    elif question == "8. Registered users of Map Users":
        
        states =st.selectbox ("Select the state", map_users["states"].unique())
        st.subheader("REGISTERED USER")
        top_chart_registered_user("map_users", states)
        
        
    elif question == "9. App opens of Map users":
        
        states =st.selectbox ("Select the state", map_users["states"].unique())
        st.subheader("APPOPENS")
        top_chart_AppOpens("map_users", states)
        
    
    elif question == "10.Registered users of Top Users":
        
        st.subheader("REGISTERED USERS")
        top_chart_registered_user_1("top_user")