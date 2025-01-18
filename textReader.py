import cv2
import pytesseract
import os
import re
from firebaseHandler import FirebaseManager


def process_file(files_directory, shop, i, db_data):
    piwo_typ_list = ["piwa", "piwo", "pszenicz", "okocim", "tatra", "łomzą", 'atecki', 'jasn, "browaru', "rnas", "niepasteryzowa",
                     "browary"]
    wino_typ_list = ["grzaniec", "zbojeckie", "wino", "wina", "grza", "grono", "monte", "monastrell", "jumil",
                     "porto tawny", "edelkirsch", "witosha", "montelago", "jumilla", "wytrawne", "czerwone", "białe",
                     "masseria", "primitivo", "moscato", "chardonnay", "budowa", "negroamaro", "premirivo",
                     "rześkość", "słodycz", "półwyt", "astrale", "chianti", "custoza", "vignon", "półsłodkie", "monte",
                     "mogen david", "concord", "mionetto", "carlo rossi", "fresco"]
    szampan_typ_list = ["secco", "dorato", "michel", "uperiore"]
    aperitif_typ_list = ["martini", "bianco", "martin", "erol", "aperitif", "aperol", "rosso", "fiero"]
    wodka_typ_list = ["vodka", "umbras", "wódka", "absolut", "stumbras", "stock", "bocian", "bols", "marine", "tadeusz",
                      "wyborów", "wyboro", "żubrówka", "wodka", "żoładkowa", "amundsen", "gorzka", "ytrynowka",
                      "ytrynówka", "barmańska", "zołądkowa", "zołądkoma", "wiśniów"]
    likier_typ_list = ["czekolada", "czekolady", "likier", "likiter", "jagermeister", "advocaat", "karmel",
                       "coffee layered", "baileys", "sheri", "johanneswald", "diplomat"]
    whiskey_typ_list = ["whisky", "whiskey", "tine", "ballantine", "whisk", "jack dan", "jacksdaniel", "jack",
                        "tullamore", "jameson", "scotch", "jamesok"]
    gin_typ_list = ["gin", "giń", "lubus", "longston"]
    rum_typ_list = ["spiced", "rum", "blanca", "bacard"]
    brandy_typ_list = ["brandy", "saperavi barrel", ]
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    folders_list = os.listdir(files_directory)
    for folder in folders_list:
        folder_dir = files_directory+folder
        if "alkohole" in folder:
            pattern = fr"alkohole(.*){shop}"
            try:
                date = re.match(pattern, folder).group(1)
            except AttributeError:
                continue
            date="od-17-01-do-22-01-"
            files_list = os.listdir(folder_dir)
            for file in files_list:
                filename = os.path.join(files_directory, folder, file)
                print(f"*   Processing {filename}")
                img = cv2.imread(filename)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                thresh1 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                                cv2.THRESH_BINARY_INV, 11, 2)
                bnt = cv2.bitwise_not(thresh1)
                text = pytesseract.image_to_string(bnt, lang='pol', config='--psm 11')
                if len(text) > 100:
                    if any(word in text.lower() for word in piwo_typ_list):
                        type = "piwo"
                    elif any(word in text.lower() for word in wino_typ_list):
                        type = "wino"
                    elif any(word in text.lower() for word in szampan_typ_list):
                        type = "szampan"
                    elif any(word in text.lower() for word in aperitif_typ_list):
                        type = "aperitif"
                    elif any(word in text.lower() for word in wodka_typ_list):
                        type = "wódka"
                    elif any(word in text.lower() for word in likier_typ_list):
                        type ="likier"
                    elif any(word in text.lower() for word in whiskey_typ_list):
                        type = "whiskey"
                    elif any(word in text.lower() for word in gin_typ_list):
                        type = "gin"
                    elif any(word in text.lower() for word in rum_typ_list):
                        type = "rum"
                    elif any(word in text.lower() for word in brandy_typ_list):
                        type = "brandy"
                    else:
                        type = "inne"
                    print(type)
                    key = f"offer{i}"
                    db_data[key] = {
                        "shop": shop,
                        "date": date,
                        "type": type,
                        "storage_path": ""
                    }
                    print(text)
                    storage_url = f"images/{date}_{shop}_{file}"
                    image_url = firebase_manager.upload_image(
                        image_path=filename,
                        storage_path=storage_url
                    )
                    db_data[key]["storage_path"] = storage_url
                    firebase_manager.upload_data(db_data)
                    i += 1
                    print(f"Image URL: {image_url}")
        else:
            pattern = fr"(.*){shop}$"
            try:
                date = re.match(pattern, folder).group(1)
            except AttributeError:
                continue
            print(date)
            files_list = os.listdir(folder_dir)
            for file in files_list:
                filename = os.path.join(files_directory,folder,file)
                print(f"*   Processing {filename}")
                img = cv2.imread(filename)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                thresh1 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                                cv2.THRESH_BINARY_INV, 11, 2)
                bnt = cv2.bitwise_not(thresh1)
                text = pytesseract.image_to_string(bnt, lang='pol', config='--psm 11')
                if re.search(r'\b(piwo|alkoholu)\b', text, re.IGNORECASE):
                    type = "piwo"
                    key = f"offer{i}"
                    db_data[key] = {
                        "shop": shop,
                        "date": date,
                        "type": type,
                        "storage_path": ""
                    }
                    storage_url = f"images/{date}_{shop}_{file}"
                    image_url = firebase_manager.upload_image(
                         image_path=filename,
                         storage_path=storage_url
                     )
                    db_data[key]["storage_path"] = storage_url
                    firebase_manager.upload_data(db_data)
                    i += 1
                    print(f"Image URL: {image_url}")
    return i, db_data


if __name__ == "__main__":
    firebase_manager = FirebaseManager(
        service_account_key="serviceAccountKey.json",
        bucket_name="alkoalertfirebase.firebasestorage.app",
        database_url="https://alkoalertfirebase-default-rtdb.europe-west1.firebasedatabase.app/"
    )
    firebase_manager.delete_storage_data()
    i = 0
    db_data = {}
    shops = ['lidl', 'biedronka']
    for shop in shops:
        i, db_data = process_file("C:\\Users\\Marta\\Desktop\\scrape\\", shop, i, db_data)
