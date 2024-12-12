import requests
from bs4 import BeautifulSoup
import json
import sqlite3

#url = "https://bashkortostan.megafon.ru/"

headers = {
    "User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

#req = requests.get(url, headers=headers)

# src = req.text

#with open("megafon_main_menu.html", "w", encoding="utf-8") as file:
#    file.write(src)

# with open("megafon_main_menu.html", encoding="utf-8") as file:
#    src = file.read()

# soup = BeautifulSoup(src, "lxml")

# tariffs = soup.find_all("a", class_="tariffs-card-header-v4__title-link gtm-tariff-title-link")

# all_tariffs = {}

# for res in tariffs:
#    item_text = res.text
#    item_url = "https://bashkortostan.megafon.ru/"+res.get("href")
#    all_tariffs[item_text] = item_url

#with open("all_tariffs.json", "w", encoding="utf-8") as file:
#    json.dump(all_tariffs, file, indent=4, ensure_ascii=False)

#with open("all_tariffs.json", encoding="utf-8") as file:
#    tariffs = json.load(file)

#count = 0

#for title, url in tariffs.items():
#
#    with open(f"tariffs_html/{title}.html", "w", encoding="utf-8") as file:
#        req = requests.get(url, headers=headers)
#        src = req.text
#        file.write(src)

#info_tar = {}

#for title in tariffs:

#    with open(f"tariffs_html/{title}.html", encoding="utf-8") as file:
#        src = file.read()

#    soup = BeautifulSoup(src, "lxml")

#    dict_tariffs = {}

#    all_tar = soup.find_all("div", class_="tariffs-detail-short-base-item")
#    k = 0
#    for j in all_tar:
"""        named_tariff = j.find("h3",
                              class_="mfui-v6-header mfui-v6-header_color_default mfui-v6-header_level_h3 mfui-v6-header_h-align_inherit").text
        value_tariff = int(j.find("div", class_="tariffs-detail-short-base-item__value").text.split()[0])
        dict_tariffs[named_tariff] = value_tariff
        k += 1

        if k == 3:
            break

    price_tariff = int(soup.find("span", class_="tariffs-price__price tariffs-price__price_current").text.split()[0])
    dict_tariffs["Цена"] = price_tariff
    info_tar[title] = dict_tariffs


with open(f"info_tariffs.json", "w", encoding="utf-8") as file:
    json.dump(info_tar, file, indent=4, ensure_ascii=False)


with open(f"info_tariffs.json", encoding="utf-8") as file:
    res = json.load(file)

connection = sqlite3.connect("Users.db")
cursor = connection.cursor()

for title, values in res.items():
    val = list(values.values())
    cursor.execute("INSERT INTO Tariffs (Title, Internet, Minutes, Sms, Price) VALUES (?, ?, ?, ?, ?)", (title, val[0], val[1], val[2], val[3]))
    connection.commit()

cursor.close()
connection.close()"""