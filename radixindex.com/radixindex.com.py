from time import sleep
import requests
import re
from bs4 import BeautifulSoup
import tg_test

url = "https://www.radixindex.com/en/surnames"

headers = {
"Accept": "*/*",
"Referer":"https://www.allpointsfps.com/",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}

page = requests.get(url, headers=headers)

src = page.text

soup = BeautifulSoup(src, "lxml")

alpha_a = soup.find(class_="content").find_all("a")

alpha_urls = []
for url in alpha_a:
    alpha_urls.append(url.get("href"))

iter_count = len(alpha_urls)
count = 0
for url in alpha_urls:
    page = requests.get(url, headers=headers)
    src = page.text
    soup = BeautifulSoup(src, "lxml")
    families_a = soup.find_all("a", {'href': re.compile(r'surnames\/surname')})
    for fam in families_a:
        with open("out/hu_families.txt", "a", encoding="utf-8") as file:
            file.write(fam.text+'\n')
    count += 1
    iter_count -= 1
    print(f"{count} pages parsed")
    print(f"{iter_count} pages left\n")
    sleep(1)
print('work_done')

tg_test.send_msg(f'work done {count} pages parsed')
