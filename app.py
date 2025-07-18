from scraper.selenium_scraper import scrape_dakar_auto
from scraper.cleaning import clean_data
import streamlit as st
import pandas as pd
from dashboard import show_dashboard

st.set_page_config(page_title='Dakar Auto Scraper',layout="wide")

st.title(' 🚗 Dakar Auto - Analyse des vehicules')

menu = st.sidebar.radio("Menu", ["Scraper avec selenium","Données Webscraper CSV", "Dashboard", "Formulaire d'évaluation" ])

if menu == 'Scraper avec selenium':
    st.subheader('🔎 Scraper des données')

    url_type_map = {
        'Voitures': ('https://dakar-auto.com/senegal/voitures-4','voiture'),
        'Motos & scooters' : ('https://dakar-auto.com/senegal/motos-and-scooters-3', 'moto'),
        'Location de voitures' : ('https://dakar-auto.com/senegal/location-de-voitures-19','location')

    }

    choix  = st.selectbox(" Choisir parmi ces options", list(url_type_map.keys()))
    url, type_objet = url_type_map[choix]

    st.write(f"URL sélectionné: {url}")

    max_pages = st.slider('Nombre de pages a scraper',1,10,3)

    if st.button("Lancer le scraping"):
        raw_df = scrape_dakar_auto(url, type_objet, max_pages)
        st.success('Scraping terminé')
        # st.write("Données brutes")
        # st.dataframe(raw_df.head())

        cleaned_df = clean_data(raw_df)
        st.write("Données nettoyées")
        st.dataframe(cleaned_df.head(10))

        st.download_button("Telecharger données nettoyées" , cleaned_df.to_csv(index=False),file_name=f"{type_objet}_nettoye.csv")

elif menu == 'Données Webscraper CSV':

    st.subheader('Telecharger les données scraper via webscraper')
    file_option = st.selectbox("choisir un fichier", ['voitures','motos','location'])
    path = f"data/dakar_auto_{file_option}.csv"

    try: 
        df = pd.read_csv(path)
        st.dataframe(df.head())
        st.download_button("Telecharger le fichier brutes" , df.to_csv(index=False),file_name=f"{file_option}_webscraper_dakar_auto.csv")
    except:
        st.error("Fichier non trouvé.")

elif menu == "Dashboard":

    st.subheader('Visualiser les données')

    file_option = st.selectbox("choisir un fichier", ['voitures','motos','location'])
    path = f"data/dakar_auto_{file_option}.csv"
    df = pd.read_csv(path)
    df = clean_data(df)

    show_dashboard(df)

elif menu == "Formulaire d'évaluation":

    st.subheader("Formulaire d'évaluation")
    st.markdown("Merci de bien vouloir remplir ce formulaire d'évaluation")

    form_html = """ <iframe src="https://ee.kobotoolbox.org/i/o7LBVaeg" width="800" height="600"></iframe> """

    st.components.v1.html(form_html, height= 650,scrolling =True)