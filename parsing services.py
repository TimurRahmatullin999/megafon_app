import requests
from bs4 import BeautifulSoup
import json
import re

url = "https://bashkortostan.megafon.ru/"
type_url = ["services/?filter=internet", "services/?filter=calls"]
header = {
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

request = [requests.get(url+type_url[0], headers=header), requests.get(url+type_url[1], headers = header)]

with open("services_html/internet.html", "w", encoding="utf-8") as file:
    src_1 = request[0].text
    file.write(src_1)

with open("services_html/calls.html", "w", encoding="utf-8") as file:
    src_2 = request[1].text
    file.write(src_2)

with open("services_html/internet.html", encoding="utf-8") as file:
    res = file.read()

soup_1 = BeautifulSoup(res, "lxml")

with open("json_type/internet_services.json", encoding="utf-8") as file:
    res = json.load(file)

def replace_string(st):
    l = st.replace("\xa0", " ")
    return l

def for_podkl(st):
    return int(st.split()[1]) if st != '10 000 ₽' else 10000

def for_ezh(st):
    return int(st.split()[0])

tariffs = list(filter(lambda x: "ГБ" in x,map(lambda x: x.replace("\xa0", " "),list(res))))
print(res)
description_tariffs = list(filter(lambda x: "Подписка" in x.text or "Дополнительный" in x.text,soup_1.find_all("p", class_="mfui-v6-paragraph mfui-v6-paragraph_color_gray mfui-v6-paragraph_space_wide services-card-content__text")))
print(description_tariffs)
price_service = soup_1.find_all("div", class_="mfui-v6-price-badge__text")
del price_service[1]
dict_tariffs = {tariff: {} for tariff in tariffs}

for i in range(len(tariffs)):
    description = replace_string(description_tariffs[i].text)
    dict_tariffs[tariffs[i]]["Тип услуги"] = "Интернет"
    dict_tariffs[tariffs[i]]["Описание"] = description
    price = replace_string(price_service[i].text)
    if price.endswith("подключение") or price.endswith("10 000 ₽"):
        dict_tariffs[tariffs[i]]["Цена"] = for_podkl(price)
        dict_tariffs[tariffs[i]]["Тип списания"] = "Одноразовое"
        dict_tariffs[tariffs[i]]["Текст для списания"] = price
    elif price.endswith("Бесплатно"):
        dict_tariffs[tariffs[i]]["Цена"] = 0
        dict_tariffs[tariffs[i]]["Тип списания"] = "Бесплатное"
        dict_tariffs[tariffs[i]]["Текст для списания"] = price
    elif price.endswith("30 дней") or price.endswith("в день"):
        dict_tariffs[tariffs[i]]["Цена"] = for_ezh(price)
        dict_tariffs[tariffs[i]]["Тип списания"] = "Ежемесячноe"
        dict_tariffs[tariffs[i]]["Текст для списания"] = price
    dict_tariffs[tariffs[i]]["Значение"] = int(re.sub(r"[А-Яа-я\+ ]", "", tariffs[i]))
    dict_tariffs[tariffs[i]]["URL"] = res[tariffs[i]]

print(dict_tariffs)

with open("json_type/info_about_internet_service.json", "w", encoding="utf-8") as file:
    json.dump(dict_tariffs, file, indent=4, ensure_ascii=False)


with open("json_type/info_about_internet_service.json", encoding="utf-8") as file:
    elements = json.load(file)

"""connection = sqlite3.connect("Users.db")
cursor = connection.cursor()

for key, value in elements.items():
    val = list(value.values())
    cursor.execute("INSERT INTO Services (title, type_of_service, description, price, type_of_written, text_for_written, value, url_tar) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (key, val[0], val[1], val[2], val[3], val[4], val[5], val[6]))
    connection.commit()

cursor.close()
connection.close()"""
