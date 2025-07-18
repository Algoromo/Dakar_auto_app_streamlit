from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

def scrape_dakar_auto(url,type_object,max_pages = 5):
    options = webdriver.ChromeOptions() 
    options.add_argument("--headless") 
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    data = []
    
    for page in range(1,max_pages + 1):
        driver.get(f"{url}?page={page}")
        time.sleep(2)
        containers = driver.find_elements(By.CSS_SELECTOR,'div.listing-card')

        for container in containers:
            try:

                modele = container.find_element(By.CSS_SELECTOR,"[class = 'listing-card__header__title mb-md-2 mb-0']").text.split(' ')
                marque = modele[0]
                annee = int(modele[-1])                
                prix = float( container.find_element(By.CSS_SELECTOR,"[class = 'listing-card__header__price font-weight-bold text-uppercase mb-0']").text.replace('\u202f','').split(' ')[0] )
                localisation = container.find_element(By.CSS_SELECTOR,"[class = 'col-12 entry-zone-address']").text.split(', ') 
                adresse = ', '.join(localisation) 
                info_vehicule = container.find_element(By.CSS_SELECTOR,"[class = 'listing-card__attribute-list list-inline mb-0']").text.split(' ')
                proprietaire = container.find_element(By.CSS_SELECTOR,"[class = 'time-author m-0']").text.replace('Par ','')
                try:

                    kilometrage = float(info_vehicule[2]) if info_vehicule[2] else None
                    boite_vitesse = info_vehicule[4] if info_vehicule[4] else None
                    carburant = info_vehicule[5] if info_vehicule[5] else None
                
                except ValueError:
                    kilometrage = None # il y a des vehicules dont le kilometrage n'est pas spécifié, on les remplace par une valeur nulle.
                    boite_vitesse = info_vehicule[2] if info_vehicule[2] else None
                    carburant = info_vehicule[3] if info_vehicule[3] else None
                
                record = {
                    'marque':marque,
                    'annee': annee,
                    'prix':prix,
                    'adresse':adresse,
                    'kilometrage':kilometrage,
                    'boite_vitesse': boite_vitesse,
                    'carburant': carburant,
                    'proprietaire': proprietaire,
                    'type': type_object
                }
            
                data.append(record)


            except Exception:
                continue

    driver.quit()
    return pd.DataFrame(data)
