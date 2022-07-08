from time import sleep
import requests
import re
from bs4 import BeautifulSoup


#url = "https://www.familyeducation.com/baby-names/surname/origin/german?page=0"

headers = {
"Accept": "*/*",
"Referer":"https://www.allpointsfps.com/",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}
result_list = []
for pagenum in range(32):
    url = f'https://www.familyeducation.com/baby-names/surname/origin/dutch?page={pagenum}'
    page = requests.get(url, headers)
    src = (page.text)
    soup = BeautifulSoup(src, "lxml")

    uls = soup.find_all("ul", {"class": "baby-names-list links col-xs-12 col-sm-4"})

    for ul in uls:
        lis = ul.find_all("li")
        for li in lis:
            result_list.append(li.text)
    print(pagenum, " ",len(lis),"surs")
    sleep(1)

with open ("out/fam_edu_nl.txt", "a", encoding="utf-8") as file:
    file.write('\n'.join(str(surname) for surname in result_list))
