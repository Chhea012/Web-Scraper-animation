from bs4 import BeautifulSoup
import requests

url = "https://www.janespatisserie.com/"
result = requests.get(url)

# Corrected the typo here: 'html.paser' -> 'html.parser'
doc = BeautifulSoup(result.text, "html.parser")

# Find all occurrences of "$" in the text
prices = doc.find_all(text="$")

# If a price is found, extract the <strong> tag content
if prices:
    parent = prices[0].parent
    strong = parent.find("strong")
    if strong:
        print(strong.string)
    else:
        print("No <strong> tag found")
else:
    print("No prices found")
