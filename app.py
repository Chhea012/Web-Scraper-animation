# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin
# import csv

# # URL of the site to scrape
# url = 'http://books.toscrape.com/'

# # Send a GET request to fetch the HTML content
# response = requests.get(url)
# if response.status_code == 200:
#     soup = BeautifulSoup(response.text, 'html.parser')
    
#     # Find all books in the main book section
#     books = soup.find_all('article', class_='product_pod')
    
#     # List to store book details
#     books_data = []
    
#     # Loop through each book and extract the details
#     for book in books:
#         # Get title
#         title = book.h3.a['title']
        
#         # Get price
#         price = book.find('p', class_='price_color').text.strip()
        
#         # Get availability status
#         availability = book.find('p', class_='instock availability').text.strip()
        
#         # Get rating by counting the class name for the star rating
#         rating_class = book.find('p', class_='star-rating')['class']
#         rating = rating_class[1] if len(rating_class) > 1 else "No rating"
        
#         # Get link to the book's page (relative link converted to absolute URL)
#         link = book.h3.a['href']
#         full_link = urljoin(url, link)  # Convert relative URL to absolute URL
        
#         # Append the book details to the list
#         books_data.append({
#             'Title': title,
#             'Price': price,
#             'Availability': availability,
#             'Rating': rating,
#             'Link': full_link
#         })

#     # Write the data to a CSV file with UTF-8 encoding
#     with open('books_data.csv', mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.DictWriter(file, fieldnames=['Title', 'Price', 'Availability', 'Rating', 'Link'])
#         writer.writeheader()  # Write header row
#         writer.writerows(books_data)  # Write book data rows
    
#     print("Data has been written to books_data.csv")

# else:
#     print("Failed to retrieve the webpage.")

# # Write the data to a Json file with UTF-8 encoding


import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import csv

# URL of the site to scrape
# url = 'http://books.toscrape.com/'
url = input("Enter the URL of the site to scrape: ")

# Send a GET request to fetch the HTML content
response = requests.get(url)

if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all books in the main book section
    books = soup.find_all('article', class_='product_pod')
    
    # List to store book details
    books_data = []
    
    # Loop through each book and extract the details
    for book in books:
        # Get title
        title = book.h3.a['title']
        
        # Get price
        price = book.find('p', class_='price_color').text.strip()
        
        # Get availability status
        availability = book.find('p', class_='instock availability').text.strip()
        
        # Get rating by counting the class name for the star rating
        rating_class = book.find('p', class_='star-rating')['class']
        rating = rating_class[1] if len(rating_class) > 1 else "No rating"
        
        # Get link to the book's page (relative link converted to absolute URL)
        link = book.h3.a['href']
        full_link = urljoin(url, link)  # Convert relative URL to absolute URL
        
        # Append the book details to the list
        books_data.append({
            'Title': title,
            'Price': price,
            'Availability': availability,
            'Rating': rating,
            'Link': full_link
        })

    # Write the data to a JSON file with UTF-8 encoding
    with open('books.json', 'w', encoding='utf-8') as f:
        json.dump(books_data, f, indent=4)
        print("Data has been written to books.json")
    # Write the data to a CSV file with UTF-8 encoding
    with open('books_data.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Title', 'Price', 'Availability', 'Rating', 'Link'])
        writer.writeheader()  # Write header row
        writer.writerows(books_data)  # Write book data rows
    print("Data has been written to books_data.csv")
else:
    print("Failed to retrieve the webpage.")



        
        



    