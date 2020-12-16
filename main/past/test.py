import time
import re
import csv
import requests as rq
from bs4 import BeautifulSoup as bs

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
HEADERS = {
    "method": "GET",
    "path": "/calculator/76561198031813016",
    "Referer": "https://steamdb.info/",
    # "sec-ch-ua": "\"Chromium\";v=\"86\", \"\\\"Not\\\\A;Brand\";v=\"99\", \"Google Chrome\";v=\"86\"",
    "User-Agent": USER_AGENT,
    "X-Requested-With": "XMLHttpRequest"
    }

# url = "https://steamdb.info/calculator/76561198031813016"
# html = rq.get(url, headers=HEADERS).text

# with open('test.txt','w',encoding='utf-8') as f:

#     soup = bs(html, "html.parser")


#     for tr in soup.find_all("tr", class_="app"):
#         # Get APP id
#         app_id = tr["data-appid"]
#         game_name = str.strip(tr.find("td", class_="text-left").text)
#         game_time = tr.find_all("td")[4 :: 5][0].text
#         res = str(game_name)
#         f.write(res)
# f.close()



# # Start Crawler
url = "https://steamdb.info/calculator/76561198031813016/" # name2
# html = urllib2.urlopen(url, timeout=12)
html = rq.get(url, headers=HEADERS)
html.encoding = 'gb2312'
html = html.text

soup = bs(html, "html.parser")

c = 1

res = list()

for tr in soup.find_all("tr", class_="app"):
    # Get APP id
    app_id = tr["data-appid"]
    game_name = str.strip(tr.find("td", class_="text-left").text)
    game_time = tr.find_all("td")[4 :: 5][0].text

    game_rating = tr.find_all("td")[5 :: 6][0].text

    game_price = tr.find_all("td")[3 :: 4][0].text
    game_price_hour = tr.find_all("td")[2 :: 3][0].text

    game_res = {"game_name": game_name,
    "game_time": game_time,
    "game_rating": game_rating,
    "game_price": game_price,
    "game_price_hour": game_price_hour,
    }
    res.append(game_res)

print(res)


# read lists
tar_file = "accounts.txt"
with open(tar_file,"r") as f:    #设置文件对象
    for line in f.readlines():
        line=line.strip("\n")
        if line is None or line == "":
            continue
        else:
            print(line)