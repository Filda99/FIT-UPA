import argparse
import uuid
from pymongo import MongoClient

DB_NAME = "test"
id_accident = str(uuid.uuid4())

AVAILABLE_LOCATIONS = {
    1: "Brno-střed",
    2: "Brno-sever",
    3: "Brno-Židenice",
    4: "Brno-Černovice",
    5: "Brno-Bystrc",
    6: "Brno-Kníničky",
    7: "Brno-Tuřany",
    8: "Brno-Slatina",
    9: "Brno-Líšeň",
    10: "Brno-Komín",
    11: "Brno-Bosonohy",
    12: "Brno-Královo Pole",
    13: "Brno-Starý Lískovec",
    14: "Brno-Řečkovice a Mokrá Hora",
    15: "Brno-Maloměřice a Obřany",
    16: "Brno-Bohunice",
    17: "Brno-Jehnice",
    18: "Brno-Útěchov",
    19: "Brno-Chrlice",
    20: "Brno-Třešť",
    21: "Brno-Horní Heršpice",
    22: "Brno-Úvoz",
    23: "Brno-Stránice",
    24: "Brno-Medlánky",
    25: "Brno-Žabovřesky",
    26: "Brno-Husovice",
    27: "Brno-Žebětín",
    28: "Brno-Štýřice",
    29: "Brno-Jundrov",
}

def insert_accident(location_id):
    # Create a new accident record
    accident = {
        "_id": id_accident,
        "datum": input("Datum: "),
        "rok": int(input("Rok (int): ")),
        "zavineni": input("Zavineni: "),
        "viditelnost": input("Viditelnost: "),
        "situovani": input("Situovani: "),
        "mesic_t": input("Mesic_t: "),
        "doba": input("Doba: "),
        "den_v_tydnu": input("Den_v_tydnu: "),
        "alkohol": input("Alkohol: "),
        "alkohol_vinik": input("Alkohol_vinik: "),
        "hlavni_pricina": input("Hlavni_pricina: "),
        "srazka": input("Srazka: "),
        "nasledky": input("Nasledky: "),
        "pricina": input("Pricina: "),
        "stav_vozovky": input("Stav_vozovky: "),
        "povetrnostni_podm": input("Povetrnostni_podm: "),
        "rozhled": input("Rozhled: "),
        "misto_nehody": input("Misto_nehody: "),
        "druh_komun": input("Druh_komun: "),
        "usmrceno_os": int(input("Usmrceno_os (int): ")),
        "tezce_zran_os": int(input("Tezce_zran_os (int): ")),
        "lehce_zran_os": int(input("Lehce_zran_os (int): ")),
        "hmotna_skoda": int(input("Hmotna_skoda (int): ")),
        "smrt": int(input("Smrt (int): ")),
        "tz": int(input("Tz (int): ")),
        "lz": int(input("Lz (int): ")),
        "vek_skupina": input("Vek_skupina: "),
        "pohlavi": input("Pohlavi: "),
        "druh_vozidla": input("Druh_vozidla: "),
        "stav_ridic": input("Stav_ridic: "),
        "osoba": input("Osoba: "),
        "ozn_osoba": input("Ozn_osoba: "),
        "nasledek": input("Nasledek: "),
        "ZSJ": input("ZSJ: "),
        "MC": AVAILABLE_LOCATIONS.get(location_id, ""),
        "x": int(input("x (int): ")),
        "y": int(input("y (int): ")),
    }

    return accident

def insert_new_accident(location_id):
    location = AVAILABLE_LOCATIONS.get(int(location_id))
    print("Location is filled automatically: ", location)
    if location:
        accident = insert_accident(location_id)

        # Connect to the database and insert the new accident
        client = MongoClient("mongodb://127.0.0.1:27017")
        db = client[DB_NAME]
        accidents = db["accidents"]
        accidents.insert_one(accident)

        # Update the list of accident IDs in the locations collection
        locations = db["locations"]
        location_record = locations.find_one({"_id": location})

        if location_record:
            accident_id = accident["_id"]
            if "accident_ids" not in location_record:
                location_record["accident_ids"] = []
            location_record["accident_ids"].append(accident_id)
            locations.update_one({"_id": location}, {"$set": {"accident_ids": location_record["accident_ids"]}})
            print(f"Accident inserted with ID: {accident_id}")
        else:
            print("Location not found.")

# MAIN FUNCTION
print(AVAILABLE_LOCATIONS)
location_id = input("Lokace: ")
insert_new_accident(location_id)
print("Saved with ID: ", id_accident)