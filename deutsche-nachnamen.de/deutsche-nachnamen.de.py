from time import sleep
import requests
import re
from bs4 import BeautifulSoup

url = "https://www.deutsche-nachnamen.de/index.php/herkunft-a-z/"

headers = {
"Accept": "*/*",
"Referer":"https://www.allpointsfps.com/",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}

page = requests.get(url, headers)

src = (page.text)

soup = BeautifulSoup(src, "lxml")

letter_urls = soup.find(class_="pagination alphabox").find_all("a", {'href': re.compile('catalog')})

i = 0
for letter in letter_urls:
    url = 'https://www.deutsche-nachnamen.de' + letter.get("href")
    page = requests.get(url, headers)
    src = (page.text)
    soup = BeautifulSoup(src, "lxml")
    print(url)

    #Find last page number
    pag = soup.find(class_="pagination-end").find("a")
    end = re.search('(?<=start=).*', pag.get("href")).group(0)
    sleep(1)

    #Run while for every letter:
    pnum = 0
    while pnum <= int(end):
        url = 'https://www.deutsche-nachnamen.de' + letter.get("href") + '&start=' + str(pnum)
        page = requests.get(url, headers)
        src = (page.text)
        soup = BeautifulSoup(src, "lxml")
        
        surnamelist = []
        for tr in soup.find_all("tr", {'class':re.compile('even|odd')}):
            surname = tr.find_all("td")[0].text.strip()
            if ' / ' in surname:
                tl = surname.split(' / ')
                surnamelist += tl
            else:
                surnamelist.append(surname)
        print(surnamelist)

        with open("out/deutche-nach.txt", "a", encoding="utf-8") as file:
                file.write('\n'.join(surnamelist) + '\n')

        print(pnum, '-',letter )

        pnum += 10

        sleep(1)

    i += 1
    print(f'{i} pages parsed')

