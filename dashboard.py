import streamlit as st
import pandas as pd
import plotly.express as px

def show_dashboard(df:pd.DataFrame):

    st.subheader(" DashBoard : Données nettoyées")

    st.write("Apercu des données")
    st.dataframe(df.head())

    if 'prix' in df.columns:
        try:
            fig = px.histogram(df, x ='prix',nbins=30,title = "Distribution des prix")
            st.plotly_chart(fig)
        except:
            st.warning("Impossible d'afficher l'histogramme des prix.")

    if 'marque' in df.columns:
        top_marques = df['marque'].value_counts().head(10)
        fig2 = px.bar(top_marques,title='Top 10 marques')
        st.plotly_chart(fig2)



