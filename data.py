from bs4 import BeautifulSoup
import requests
url = "https://fruit-website-indol.vercel.app/pages/shop.html"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
print(soup)
#   I want to get the data to file.cvs
import csv
with open("shop_data.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "H1", "H2", "Link", "P", "List"])
    title = soup.find("title").text
    h1 = soup.find("h1").text
    h2 = soup.find("h2").text
    link = soup.find("a").get("href")
    p = soup.find("p").text
    lis = soup.find_all("li")
    data = [title, h1, h2, link, p, [li.text for li in lis]]
    writer.writerow(data)
print("Data exported to shop_data.csv")

#  I want to get the data to jonson file.

import json
with open("shop_data.json", "w") as file:
    json.dump({"title": title, "h1": h1,"h2":h2, "link": link, "p": p, "list": [li.text for li in lis]}, file)
print("Data exported to shop_data.json")

