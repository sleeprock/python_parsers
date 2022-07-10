import pandas as pd

surnames = []
for page in range(1001):
    url = f'https://www.prijmeni.cz/oblast/3000-ceska_republika&page={page}'
    df = pd.read_html(url)
    surnames = df[0]['Příjmení'].to_list()
    with open("out/pz_prijmeni.txt", "a", encoding="utf-8") as file:
        file.write("\n".join(str(s) for s in surnames) + "\n")
    print(str(page))




# df = pd.read_html(url)



