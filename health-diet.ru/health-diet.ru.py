from email import header
import random
from textwrap import indent
from time import sleep
from matplotlib.font_manager import json_dump
import requests
from bs4 import BeautifulSoup
import json
import csv
# url = "https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie"
# #url = "https://www.radixindex.com/en/surnames/alphabetical_index/ca"

headers = {
"Accept": "*/*",
"Referer":"https://health-diet.ru/",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}

# req = requests.get(url, headers=headers)
# src = req.text
# print(src)

# with open("index.html", "w", encoding="utf-8") as file:
#     file.write(src)

######

# with open("index.html", encoding="utf-8") as file:
#     src = file.read()

# soup = BeautifulSoup(src, "lxml")

# all_products_hrefs = soup.find_all(class_="mzr-tc-group-item-href")

# all_categories_dict = {}

# for item in all_products_hrefs:
#     item_text = item.text
#     item_href = "https://health-diet.ru" + item.get("href")
#     all_categories_dict[item_text] = item_href

# with open ("all_categories_dict.json", "w", encoding="utf-8") as file:
#     json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)

with open ("all_categories_dict.json", encoding="utf-8") as file:
    all_categories = json.load(file)

iteration_count = int(len(all_categories)) - 1

print(f'Iterations count: {iteration_count}')

count = 0
for category_name, category_href in all_categories.items():

    rep = [',', ' ', '-', "'"]
    for item in rep:
        category_name = category_name.replace(item, "_")
    
    req = requests.get(url=category_href, headers=headers)
    src = req.text

    with open (f'data/{count}_{category_name}.html', 'w', encoding="utf-8") as file:
        file.write(src)
    
    with open (f'data/{count}_{category_name}.html', encoding="utf-8") as file:
        src = file.read()
    
    soup = BeautifulSoup(src, "lxml")

    #проверка страницы на наличие
    alert_block = soup.find(class_="uk-alert uk-alert-danger uk-h1 uk-text-center mzr-block mzr-grid-3-column-margin-top")
    if alert_block is not None:
        continue


    #headers table

    table_head = soup.find(class_="uk-table mzr-tc-group-table uk-table-hover uk-table-striped uk-table-condensed") \
                        .find("tr") \
                        .find_all("th")
    
    product = table_head[0].text
    calories = table_head[1].text
    proteins = table_head[2].text
    fats = table_head[3].text
    carbohydrates = table_head[4].text

    with open (f"data/{count}_{category_name}.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                product,
                calories,
                proteins,
                fats,
                carbohydrates  
            )
        )
    
    #собираем данные продуктов

    product_info = []

    products_data = soup.find(class_="uk-table mzr-tc-group-table uk-table-hover uk-table-striped uk-table-condensed") \
                        .find("tbody").find_all("tr")
    for item in products_data:
        product_tds = item.find_all("td")
    
        title = product_tds[0].find("a").text
        calories = product_tds[1].text
        proteins = product_tds[2].text
        fats = product_tds[3].text
        carbohydrates = product_tds[4].text

        product_info.append(
            {
                "Title": title,
                "Calories": calories,
                "Proteins": proteins,
                "Fats": fats,
                "Carbohydrates": carbohydrates
            }

        
        )

        with open (f"data/{count}_{category_name}.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                title,
                calories,
                proteins,
                fats,
                carbohydrates  
                )
            )
    
    with open(f"data/{count}_{category_name}.json", "a", encoding="utf-8") as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)

    count += 1
    print(f"iteration{count}, {category_name} записан")
    iteration_count = iteration_count - 1

    if iteration_count == 0:
        print('work done')
        break

    print(f'left {iteration_count} iterations')
    sleep(random.randrange(2, 4))