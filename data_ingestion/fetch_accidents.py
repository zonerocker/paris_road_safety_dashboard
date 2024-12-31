import pandas as pd
import re
from typing import List, Dict, Union
import numpy as np

def extract_accident_details(resume: str) -> Dict[str, Union[str, bool]]:
    """Extracts accident details from a résumé string using regex.

    Args:
        resume: A string containing the accident details.

    Returns:
        A dictionary containing the extracted accident details.
    """

    if pd.isna(resume):
        return {}

    result = {}

    #  Severity
    if "Accident Léger non mortel" in resume:
      result["severity"] = "Léger non mortel"
    elif "Accident Grave non mortel" in resume:
        result["severity"] = "Grave non mortel"
    elif "Accident Mortel" in resume:
        result["severity"] = "Mortel"
    else:
        result["severity"] = None


    # Location context
    if "En agglomération" in resume:
        result["location_context"] = "En agglomération"
    elif "Hors agglomération" in resume:
        result["location_context"] = "Hors agglomération"
    else:
        result["location_context"] = None
    

    # Road configuration
    road_config_patterns = {
        "En Y": r"En Y",
        "En T": r"En T",
        "En X": r"En X",
        "Hors intersection": r"Hors intersection",
        "Place": r"Place",
        "A plus de 4 branches": r"A plus de 4 branches"
    }
    
    result["road_configuration"] = None  # default
    for key, pattern in road_config_patterns.items():
      if re.search(pattern, resume):
        result["road_configuration"] = key
        break


    # Lighting/Time
    lighting_patterns = {
        "Plein jour": r"Plein jour",
        "Crépuscule ou aube": r"Crépuscule ou aube",
        "Nuit avec éclairage public allumé": r"Nuit avec éclairage public allumé",
        "Nuit sans éclairage public": r"Nuit sans éclairage public"
    }
    
    result["lighting"] = None  # default
    for key, pattern in lighting_patterns.items():
      if re.search(pattern, resume):
        result["lighting"] = key
        break

    # Weather
    weather_patterns = {
      "Normale": r"météo Normale",
      "Pluie légère": r"météo Pluie légère",
      "Temps couvert": r"météo Temps couvert",
       "Pluie forte": r"météo Pluie forte"
    }
    result["weather"] = None  # default
    for key, pattern in weather_patterns.items():
      if re.search(pattern, resume):
        result["weather"] = key
        break
    

    # Surface
    surface_patterns = {
        "Normale": r"surface chaussée : Normale",
        "Mouillée": r"surface chaussée : Mouillée",
        "Non renseigné": r"surface chaussée : Non renseigné",
        "Autre": r"surface chaussée : Autre",
         "Corps gras - huile": r"surface chaussée : Corps gras - huile",
        "Enneigée": r"surface chaussée : Enneigée",
         "Flaques": r"surface chaussée : Flaques"

    }
    result["surface"] = None  # default
    for key, pattern in surface_patterns.items():
      if re.search(pattern, resume):
        result["surface"] = key
        break


    vehicle_patterns = {
    "Cyclomoteur <=50 cm3": r"Cyclomoteur <=50 cm3",
    "Véhicule de tourisme (VT)": r"Véhicule de tourisme \(VT\)",
    "Moto ou sidecar > 50 <= 125 cm3": r"Moto ou sidecar > 50 <= 125 cm3",
    "Moto ou sidecar > 125 cm3": r"Moto ou sidecar > 125 cm3",
    "Scooter <= 50 cm3": r"Scooter <= 50 cm3",
    "Scooter > 125 cm3": r"Scooter > 125 cm3",
    "Scooter > 50 <= 125 cm3": r"Scooter > 50 <= 125 cm3",
    "VU seul 1,5T < PTAC <=3,5T": r"VU seul 1,5T < PTAC <=3,5T",
    "PL > 3,5T + remorque": r"PL > 3,5T \+ remorque",
    "PL seul 3,5T <=": r"PL seul 3,5T <=",
    "Autocar": r"Autocar",
    "Autobus": r"Autobus",
    "Bicyclette": r"Bicyclette",
    "EDP-m": r"EDP-m",
    "Voiturette": r"Voiturette",
    "Quad léger <= 50 cm3": r"Quad léger <= 50 cm3",
    "Tramway": r"Tramway",
    "Autre véhicule": r"Autre véhicule",
    "Tracteur routier + semi-remorque": r"Tracteur routier \+ semi-remorque",
    "PL seul PTAC > 7,5T" : r"PL seul PTAC > 7,5T",
    "3 RM > 125 cm3": r"3 RM > 125 cm3",
    "3 RM <= 50 cm3": r"3 RM <= 50 cm3",
    "Vélo par assistance électrique": r"Vélo par assistance électrique",
    "Engin spécial": r"Engin spécial",
    "EDP-sm": r"EDP-sm",
    "Quad lourd > 50 cm3": r"Quad lourd > 50 cm3",
    "Tracteur agricole": r"Tracteur agricole",
    "EDP sans moteur": r"Autre engin de déplacement personnel \(EDP\) sans moteur",
    "Indéterminable" : r"Indéterminable",
}

    result["vehicle_types"] = []  # default
    for key, pattern in vehicle_patterns.items():
      if re.search(pattern, resume):
        result["vehicle_types"].append(key)

    # Parties Involved
    parties_patterns = {
        "1 Piéton Feminin": r"1 Piéton Feminin",
        "1 Piéton Masculin": r"1 Piéton Masculin",
        "1 Piéton": r"1 Piéton",
         "1 usager Masculin": r"1 usager Masculin",
         "1 usager Feminin": r"1 usager Feminin",
         "avec 1 passager": r"avec 1 passager",
         "avec 2 passagers": r"avec 2 passager",
          "avec 3 passagers": r"avec 3 passager",
        "av": r"av", #av means avec
        "1 Bic": r"1 Bic" #means bicyclette,
        
    }

    result["parties_involved"] = []  # default
    for key, pattern in parties_patterns.items():
      if re.search(pattern, resume):
        result["parties_involved"].append(key)
        
    if re.search(r"heurte 1 Piéton Feminin de \d+ ans \(BH\)",resume):
      result["parties_involved"].append( "1 Piéton Feminin" )
    
    if re.search(r"heurte 1 Piéton Masculin de \d+ ans \(Ind\)",resume):
      result["parties_involved"].append("1 Piéton Masculin")


    if re.search(r"heurte 1 Véhicule de tourisme \(VT\)",resume):
      result["parties_involved"].append("1 Véhicule de tourisme (VT)")
      

    return result

# Load your CSV file
df = pd.read_csv("./data/accidents.csv", encoding='utf-8', sep=";")

# Normalize spaces
df['Résumé'] = df['Résumé'].apply(lambda x: re.sub(r'\s+', ' ', x.strip()) if isinstance(x, str) else x)

# Apply the extraction function to the 'Résumé' column
df['Résumé_Details'] = df['Résumé'].apply(extract_accident_details)

# Create new columns from the extracted details
df = pd.concat([df, df['Résumé_Details'].apply(pd.Series)], axis=1)


#Optional: remove the original Résumé_Details
df = df.drop('Résumé_Details',axis=1)

#Display the result to check
print(df[['Résumé', 'severity', 'location_context', 'road_configuration','lighting', 'weather','surface','vehicle_types','parties_involved']].head(15).to_markdown(index=False))

# Optionnal, saving the new csv :
df.to_csv('accidents-enriched.csv', index = False)