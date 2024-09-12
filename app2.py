
import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import streamlit_option_menu
from streamlit_option_menu import option_menu
import mysql.connector
import time
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import streamviz
import plotly.graph_objects as go


st.set_page_config(page_title="Performance 4.0 Dashboard", page_icon=":bar_chart:", layout="wide")
# Read CSV file
mydb = mysql.connector.connect(host='localhost',
                            database='data',
                            user='root',
                            password='Tunis123456789@')
mycursor = mydb.cursor()
theme_plotly = None 

mycursor.execute('''select * from machine_stop_table_mould''')
myresult = mycursor.fetchall()
mycursor.execute('''select * from machine_daily_table_mould''')
myresult1 = mycursor.fetchall()
mycursor.execute('''select * from Real_Time_Table''')
myresult2 = mycursor.fetchall()
# ---- SIDEBAR ----
with st.sidebar:
    st.sidebar.image("Image/logo99.png",width=300,caption="")
    selected = option_menu(
    menu_title = "Menu Principal",
    options = ["Dashboard Live","Arrêts","Production"],
    icons = ["house","gear","activity"],
    menu_icon = "cast",
    default_index = 0,
    #orientation = "horizontal",
)
if selected == "Dashboard Live":
    # ---- MAINPAGE ----
    if  myresult2[0][9] == 'on':
            column1,column2,column3= st.columns(3)
            with column1:
                st.markdown(f"<h3 style='font-size:60px; background-color:green;text-align:center;'> Production </h3>", unsafe_allow_html=True)
            with column2:
                st.markdown(f"<h3 style='font-size:60px;textlign:center;'></h3>", unsafe_allow_html=True)
            with column3:
                st.markdown(f"<h3 style='font-size:60px;text-align:center;'></h3>", unsafe_allow_html=True)        
    else: 
        column1,column2,column3 = st.columns(3)
        with column1:  
            st.markdown(f"<h3 style='font-size:60px; background-color:red;text-align:center;'>Arrêts</h3>", unsafe_allow_html=True) 
        with column2:
                st.markdown(f"<h3 style='font-size:60px;text-align:center;color:red;'>{myresult2[0][10]}</h3>", unsafe_allow_html=True)
        with column3:
                st.markdown(f"<h3 style='font-size:60px;text-align:center;'></h3>", unsafe_allow_html=True)     
    st.markdown("""---""")        

    left_column, middle_column,right_column = st.columns(3)
    with left_column:
        st.markdown(f"<h3 style='font-size:40px;color:white;background-color:rgb(70, 74, 150);text-align:center;'>Machine</h3>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='font-size:40px;text-align:center;'> IPS01 </h3>", unsafe_allow_html=True)
    with middle_column:
        article_value =str( myresult2[0][2])
        st.markdown(f"<h3 style='font-size:40px;color:white;background-color:rgb(70, 74, 150);text-align:center;'>Article</h3>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='font-size:40px;text-align:center;'> {article_value} </h3>", unsafe_allow_html=True)
    with right_column:
        article_value = myresult2[0][8]
        st.markdown(f"<h3 style='font-size:40px;color:white;background-color:rgb(70, 74, 150);text-align:center;'>Pilote</h3>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='font-size:40px;text-align:center;'> {article_value} </h3>", unsafe_allow_html=True)

    st.markdown("""---""")
    df = pd.DataFrame(myresult2, columns=['Machine', 'ordre', 'article','planif', 'bon', 'rejet', 'purge','stop_time','regleur','cavity','couleur','trs'])
    left_column, right_column = st.columns(2)
    with left_column:
        df['bon'] = df['bon'].astype('float') 
        current_bon = df['bon'].astype('int') 
        current_bon = current_bon.iloc[0]
        df['planif'] = df['planif'].astype('float') 
        current_plan = df['planif'].astype('int') 
        current_plan = current_plan.iloc[0]
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=current_bon,
            title={'text': "Quantités Produites(u)"},
            gauge={'axis': {'range': [0, current_plan]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, current_plan/3], 'color': "lightgreen"},
                    {'range': [ current_plan/3, 2*current_plan/3], 'color': "darkorange"},
                    {'range': [ 2*current_plan/3, current_plan], 'color': "darkred"}],
                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': current_plan}}))
        st.plotly_chart(fig,use_container_width=True)


    with right_column:
    ##########performance###########
        df['trs'] = df['trs'].astype('float') 

        current_value = df['trs'].astype('int') 
        current_value = current_value.iloc[0]
        # Créer le graphique de jauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=current_value-20,
            title={'text': "Performance (%)"},
            gauge={'axis': {'range': [0, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 40], 'color': "darkred"},
                    {'range': [40, 60], 'color': "darkorange"},
                    {'range': [60, 100], 'color': "lightgreen"}],
                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 100}}))
        st.plotly_chart(fig,use_container_width=True)
    left_column,middle_column, right_column = st.columns(3)
    with left_column:
        current_bon = myresult2[0][4]
        st.markdown(f"<h3 style='font-size:40px;color:blue; background-color:lightgreen;text-align:center;'>Quantités Bonnes</h3>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='font-size:40px;text-align:center;'> {current_bon} </h3>", unsafe_allow_html=True)
    with right_column:
        current_purge = myresult2[0][6]
        st.markdown(f"<h3 style='font-size:40px;color:blue; background-color:yellow;text-align:center;'>Quantités Purgées</h3>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='font-size:40px;text-align:center;'> {current_purge} </h3>", unsafe_allow_html=True)    
    with middle_column: 
        current_rejet = myresult2[0][5]
        st.markdown(f"<h3 style='font-size:40px;color:white;background-color:red;text-align:center;'>Quantités Rejetées</h3>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='font-size:40px;text-align:center;'> {current_rejet} </h3>", unsafe_allow_html=True) 
    
    
    st.markdown("""---""")
    
if selected == "Arrêts":
    st.title(":bar_chart: données des Arrêts")
    st.markdown("##")
    total1,total2=st.columns(2)
    with total1:

        st.subheader("Tous les enregistrements d’arrêts :floppy_disk:")
        
        
        df = pd.DataFrame(myresult, columns=['Machine', 'Date insert', 'Ordre de fabrication','Code Stops', 'Temps Debut', 'Temps Fin', 'Regleur'])
        st.dataframe(df)
        csv = df.to_csv(index=False)
        st.download_button(
        label="Télécharger en CSV",
        data=csv,
        file_name='data.csv',
        mime='text/csv'
        )
        with total2:
            df['Date insert'] = pd.to_datetime(df['Date insert'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
            df['Temps Debut'] = pd.to_datetime(df['Temps Debut'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
            df['Temps Fin'] = pd.to_datetime(df['Temps Fin'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
            # Vérifier si les dates ont été correctement convertie
            # Calculer la durée de l'arrêt
            df['Duration_Stop'] = df['Temps Fin'] - df['Temps Debut']
            df['stop en minutes'] = round((df['Duration_Stop'].dt.total_seconds() / 60),2)    
            # Graphique d'analyse : Durée d'arrêt par type de code de stop
        
            fig = px.pie(df, values='Duration_Stop', names='Code Stops')
            fig.update_layout(legend_title="stop", legend_y=0.9)
            fig.update_traces(textinfo='percent+label', textposition='inside')
            st.markdown(f"<h3 style='font-size:30px;text-align:center;'> Arrêts en fonction des causes</h3>", unsafe_allow_html=True)
            fig.update_layout(width=800, height=500)
            st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    st.markdown("""---""")
    
    
    st.markdown(f"<h3 style='font-size:30px;text-align:center;'> Arrêts en fonction des dates</h3>", unsafe_allow_html=True) 
    st.bar_chart(df.groupby('Date insert')['stop en minutes'].sum(),use_container_width=True)
    
   
 
    
    
if selected == "Production":
    st.title(":bar_chart: Données de Production")
    st.markdown("##")
    st.subheader("Tous les enregistrements de Production :floppy_disk:")
    df = pd.DataFrame(myresult1, columns=['Machine', 'Date insert', 'Heures Production','Down Hours', 'Good QTY', 'Rejects QTY', 'Cycle Time','Availability_Rate','Performance_Rate','Quality_Rate','TRS','Shift','Part_Number'])
    st.dataframe(df) 
    csv = df.to_csv(index=False)
    st.download_button(
    label="Télécharger en CSV",
    data=csv,
    file_name='data.csv',
    mime='text/csv'
    )
    st.markdown("""---""")
    df.columns = df.columns.str.strip()
    ####Conversion des colonnes de varchar à numérique
    df['Date insert'] = pd.to_datetime(df['Date insert'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
    df['Heures Production'] = pd.to_numeric(df['Heures Production'], errors='coerce')
    df['Down Hours'] = pd.to_numeric(df['Down Hours'], errors='coerce')
    df['Good QTY'] = pd.to_numeric(df['Good QTY'], errors='coerce')
    df['Rejects QTY'] = pd.to_numeric(df['Rejects QTY'], errors='coerce')
    df['Cycle Time'] = pd.to_numeric(df['Cycle Time'], errors='coerce')
    df['Availability_Rate'] = pd.to_numeric(df['Availability_Rate'], errors='coerce')
    df['Performance_Rate'] = pd.to_numeric(df['Performance_Rate'], errors='coerce')
    df['Quality_Rate'] = pd.to_numeric(df['Quality_Rate'], errors='coerce')
    df['TRS'] = pd.to_numeric(df['TRS'], errors='coerce')
    # df['Date insert'] = df['Date insert'].str.replace(r'\s+', ' ', regex=True).str.strip()
    
    # df['Date insert'] = pd.to_datetime(df['Date insert'], infer_datetime_format=True, errors='coerce')
    #df['Date insert'] = pd.to_datetime(df['Date insert'], format='%Y/%m/%d %H:%M', errors='coerce')
   
    
    total1,total2=st.columns(2,gap='large')
    with total1:
        st.markdown(f"<h3 style='font-size:30px;text-align:center;'> TRS par rapport Dates</h3>", unsafe_allow_html=True)

        data_for_chart = df.set_index('Date insert')[['TRS']]

# Affichage du graphique en ligne
        st.line_chart(data_for_chart,use_container_width=True)
    with total2:
        st.markdown(f"<h3 style='font-size:30px;text-align:center;'> Temps de Production par rapport Dates</h3>", unsafe_allow_html=True)
        st.bar_chart(df.groupby('Date insert')['Heures Production'].sum(),use_container_width=True)

#theme
hide_st_style=""" 

<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""
