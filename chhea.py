import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

# Step 1: Prompt the user to enter the URL
url = input("Enter the URL to scrape: ")  # User input for URL

# Step 2: Send a GET request to the website
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    print("Successfully fetched the webpage")
else:
    print(f"Failed to retrieve the webpage with status code {response.status_code}")
    exit()

# Step 3: Parse the content of the page
soup = BeautifulSoup(response.text, 'html.parser')

# Step 4: Extracting text from different HTML elements

# Extract all headings (h1, h2, h3, etc.)
headings = []
for i in range(1, 7):
    for h in soup.find_all(f'h{i}'):
        print(h.text.strip())

# Extract all paragraphs
paragraphs = []
for p in soup.find_all('p'):
    paragraphs.append(p.text.strip())


# Extract all lists (ordered and unordered)
lists = []
for ul in soup.find_all('ul'):
    for li in ul.find_all('li'):
        print(li.text.strip())

# Extract all ordered lists (ordered)
for ol in soup.find_all('ol'):
    for li in ol.find_all('li'):
        print(li.text.strip())

# Step 5: Extract all links (URLs from <a> tags)
links = []
for a in soup.find_all('a', href=True):
    print(a['href'])

# Step 6: Extract all tables (if present)
tables = soup.find_all('table')
table_data = []
for table in tables:
    rows = table.find_all('tr')
    table_rows = []
    for row in rows:
        cols = row.find_all('td')
        cols = [col.text.strip() for col in cols]
        table_rows.append(cols)
    table_data.append(table_rows)

# Step 7: Extract all images (URLs from <img> tags)
images = []
for img in soup.find_all('img', src=True):
    images.append(img['src'])
    print(img['src'])
# Step 8: Save the extracted data to a JSON file
url_name = url.split("/")[-1]
json_file_name = f"{url_name}.json"
with open(json_file_name, 'w') as f:
    json.dump({
        "Headings": headings,
        "Paragraphs": paragraphs,
        "Lists": lists,
        "Links": links,
        "Images": images
    }, f, indent=4)
print(f"Data has been written to {json_file_name}")

# Step 9: Prepare data for saving to a CSV file
data_dict = {
    "Headings": pd.Series(headings),
    "Paragraphs": pd.Series(paragraphs),
    "Lists": pd.Series(lists),
    "Links": pd.Series(links),
    "Images": pd.Series(images)
}

# Convert dictionary to DataFrame
csv_df = pd.DataFrame(data_dict)
# Step 10: Save the extracted data to a CSV file
csv_file_name = f"{url_name}.csv"
csv_df.to_csv(csv_file_name, index=False)
print(f"Data has been written to {csv_file_name}")
