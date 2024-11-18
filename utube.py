# from bs4 import BeautifulSoup
# import requests

# url = "https://www.bakingmad.com/recipes/easy-banana-bread?gad_source=1&gclid=CjwKCAiAxea5BhBeEiwAh4t5K6auegzStNNKGF2-I9aVPceG_Zyy8bBB8PjSym5thHtU30NZ2eZyhhoCTnoQAvD_BwE"
# page = requests.get(url)
# soup = BeautifulSoup(page.text, "html")
# print(soup)

# import requests
# url = "https://www.geeksforgeeks.org/web-technology/"
# r = requests.get(url)
# print(r.text)



# from bs4 import BeautifulSoup
# import requests
# url = "https://www.geeksforgeeks.org/web-technology/"
# r = requests.get(url)
# soup = BeautifulSoup(r.text, "lxml")
# print(soup)




import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://webscraper.io/"
r = requests.get(url)
soup = BeautifulSoup(r.text, "lxml")

names = soup.find_all("a", class_= "title")
print(names)
product_name = []
for i in names :
    name = i.text
    product_name.append(name)

print(product_name)


