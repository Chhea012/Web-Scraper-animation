import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import tkinter as tk
from tkinter import messagebox
from tkinter import font
from urllib.parse import urlparse
# https://fruit-website-indol.vercel.app/index.html
# https://fruit-website-indol.vercel.app/pages/shop.html
# https://fruit-website-indol.vercel.app/pages/contact.html
# https://www.w3schools.com/
# https://docs.python.org/3/library/tkinter.html
def fetch_webpage(url):
    
    """Fetches the webpage content for a given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        raise Exception("Failed to retrieve the webpage: " + str(e))
def extract_headings(soup):
    """Extracts headings from <h1> to <h6>."""
    headings = []  
    for i in range(1, 7):
        tag_name = 'h' + str(i) 
        for h in soup.find_all(tag_name):
            headings.append(h.text.strip())
        # print(headings)
    return headings
def extract_paragraphs(soup):
    """Extracts all paragraph texts."""
    paragraphs = []
    for p in soup.find_all('p'):
        paragraphs.append(p.text.strip())
    # print(paragraphs)
    return paragraphs
def extract_lists(soup):
    """Extracts list items from <ul> and <li>."""
    lists = []
    for ul in soup.find_all('ul'):
        for li in ul.find_all('li'):
            lists.append(li.text.strip())
        # print(lists)
    return lists
def extract_links(soup):
    """Extracts all hyperlinks."""
    links = []
    for a in soup.find_all('a'):
        link = a.get('href')
        if link:  # To avoid appending None if 'href' is missing
            links.append(link)
    # print(links)
    return links
def extract_images(soup):
    """Extracts all image URLs."""
    images = []
    for img in soup.find_all('img'):
        img_url = img.get('src')
        if img_url:  # To avoid appending None if 'src' is missing
            images.append(img_url)
    # print(images)
    return images
def parse_content(html_content, extract_headings_opt, extract_paragraphs_opt, extract_lists_opt, extract_links_opt, extract_images_opt):
    """Parses HTML content and combines all extractions based on user preferences."""
    soup = BeautifulSoup(html_content, 'html.parser')
    data = {}
    if extract_headings_opt:
        data["Headings"] = extract_headings(soup)
    if extract_paragraphs_opt:
        data["Paragraphs"] = extract_paragraphs(soup)
    if extract_lists_opt:
        data["Lists"] = extract_lists(soup)
    if extract_links_opt:
        data["Links"] = extract_links(soup)
    if extract_images_opt:
        data["Images"] = extract_images(soup)
    return data
def save_data(data, url):
    """Saves the extracted data into JSON and CSV files."""
    parsed_url = urlparse(url)
    domain_name = parsed_url.netloc.split('.')[1]  # Use the domain name

    # Save to JSON
    json_file_name =domain_name + ".json"
    # Save to JSON
    with open(json_file_name, 'w') as f:
        json.dump(data, f, indent=4)
    # Save to CSV
    data_dict = {key: pd.Series(value) for key, value in data.items()}
    csv_df = pd.DataFrame(data_dict)
    csv_file_name = domain_name + ".csv"
    csv_df.to_csv(csv_file_name, index=False)
    return json_file_name, csv_file_name
def scrape():
    """Main function to orchestrate the scraping process."""
    url = url_entry.get()
    try:
        # Step 1: Fetch the webpage content
        html_content = fetch_webpage(url)
        messagebox.showinfo("Success", "Successfully fetched the webpage")
        
        # Step 2: Parse the content
        data = parse_content(
            html_content,
            extract_headings_opt=var_headings.get(),
            extract_paragraphs_opt=var_paragraphs.get(),
            extract_lists_opt=var_lists.get(),
            extract_links_opt=var_links.get(),
            extract_images_opt=var_images.get(),
        )
        # Step 3: Save the data
        json_file, csv_file = save_data(data, url)
        # Notify user
        messagebox.showinfo("Success", "Data saved to " + json_file + " and " + csv_file)
    except Exception as e:
        messagebox.showerror("Error", "Error: " + str(e))
#  I want to see data in the console
    print(data)
# Create main window
window = tk.Tk()
window.title("Web Scraping Tool")
window.geometry("600x600")  # Set the window size
window.config(bg="#f0f0f0")  # Light gray background

# Define custom font
custom_font = font.Font(family="Arial", size=12, weight="bold")

# Create a frame for the content
frame = tk.Frame(window, bg="#f0f0f0")
frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

# Create a title label
title_label = tk.Label(frame, text="Web Scraping Tool", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333")
title_label.pack(pady=10)

# Create a label and entry for the URL
url_label = tk.Label(frame, text="Enter URL to scrape:", font=custom_font, bg="#f0f0f0", fg="#333")
url_label.pack(pady=5)

# Create a frame for the URL entry with padding
entry_frame = tk.Frame(frame, bg="#f0f0f0")
entry_frame.pack(pady=10)

# Entry for the URL (without x directly on Entry)
url_entry = tk.Entry(entry_frame, font=custom_font, width=45, relief="solid", bd=2)
url_entry.pack(padx=10, pady=5)  # Add padding for the Entry widget using pack() method

# Checkboxes for selecting what data to scrape
var_headings = tk.BooleanVar(value=True)
var_paragraphs = tk.BooleanVar(value=True)
var_lists = tk.BooleanVar(value=True)
var_links = tk.BooleanVar(value=True)
var_images = tk.BooleanVar(value=True)

checkbox_frame = tk.Frame(frame, bg="#f0f0f0")
checkbox_frame.pack(pady=10)

checkbox_headings = tk.Checkbutton(checkbox_frame, text="Headings (h1, h2, h3, ...)", variable=var_headings, font=custom_font, bg="#f0f0f0")
checkbox_headings.grid(row=0, column=0, sticky="w", padx=10)

checkbox_paragraphs = tk.Checkbutton(checkbox_frame, text="Paragraphs", variable=var_paragraphs, font=custom_font, bg="#f0f0f0")
checkbox_paragraphs.grid(row=1, column=0, sticky="w", padx=10)

checkbox_lists = tk.Checkbutton(checkbox_frame, text="Lists (ul, ol)", variable=var_lists, font=custom_font, bg="#f0f0f0")
checkbox_lists.grid(row=2, column=0, sticky="w", padx=10)

checkbox_links = tk.Checkbutton(checkbox_frame, text="Links (a tags)", variable=var_links, font=custom_font, bg="#f0f0f0")
checkbox_links.grid(row=3, column=0, sticky="w", padx=10)

checkbox_images = tk.Checkbutton(checkbox_frame, text="Images (img tags)", variable=var_images, font=custom_font, bg="#f0f0f0")
checkbox_images.grid(row=4, column=0, sticky="w", padx=10)

# Button to start the scraping
scrape_button = tk.Button(frame, text="Start Scraping", command=scrape, font=("Arial", 14), bg="#4CAF50", fg="white", relief="raised", bd=2, padx=20, pady=10)
scrape_button.pack(pady=20)

# Start the GUI event loop
window.mainloop()
