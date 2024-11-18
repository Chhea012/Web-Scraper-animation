import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import tkinter as tk
from tkinter import messagebox

# Function to start the web scraping process
def scrape():
    # Get URL from the user input
    url = url_entry.get()

    # Send GET request
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx/5xx responses
        messagebox.showinfo("Success", "Successfully fetched the webpage")

        # Parse the content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract data based on user selection
        data = {}

        if var_headings.get():
            headings = [h.text.strip() for i in range(1, 7) for h in soup.find_all(f'h{i}')]
            data["Headings"] = headings

        if var_paragraphs.get():
            paragraphs = [p.text.strip() for p in soup.find_all('p')]
            data["Paragraphs"] = paragraphs

        if var_lists.get():
            lists = [li.text.strip() for ul in soup.find_all('ul') for li in ul.find_all('li')]
            data["Lists"] = lists

        if var_links.get():
            links = [a['href'] for a in soup.find_all('a', href=True)]
            data["Links"] = links

        if var_images.get():
            images = [img['src'] for img in soup.find_all('img', src=True)]
            data["Images"] = images

        # Save data to JSON
        url_name = url.split("/")[-1]
        json_file_name = f"{url_name}.json"
        with open(json_file_name, 'w') as f:
            json.dump(data, f, indent=4)

        # Save data to CSV
        data_dict = {key: pd.Series(value) for key, value in data.items()}
        csv_df = pd.DataFrame(data_dict)
        csv_file_name = f"{url_name}.csv"
        csv_df.to_csv(csv_file_name, index=False)

        messagebox.showinfo("Success", f"Data saved to {json_file_name} and {csv_file_name}")

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to retrieve the webpage: {e}")

# Create main window
root = tk.Tk()
root.title("Web Scraping Tool")

# Create a label and entry for the URL
url_label = tk.Label(root, text="Enter URL to scrape:")
url_label.pack(pady=5)

url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Checkboxes for selecting what data to scrape
var_headings = tk.BooleanVar(value=True)
var_paragraphs = tk.BooleanVar(value=True)
var_lists = tk.BooleanVar(value=True)
var_links = tk.BooleanVar(value=True)
var_images = tk.BooleanVar(value=True)

checkbox_headings = tk.Checkbutton(root, text="Headings (h1, h2, h3, ...)", variable=var_headings)
checkbox_headings.pack()

checkbox_paragraphs = tk.Checkbutton(root, text="Paragraphs", variable=var_paragraphs)
checkbox_paragraphs.pack()

checkbox_lists = tk.Checkbutton(root, text="Lists (ul, ol)", variable=var_lists)
checkbox_lists.pack()

checkbox_links = tk.Checkbutton(root, text="Links (a tags)", variable=var_links)
checkbox_links.pack()

checkbox_images = tk.Checkbutton(root, text="Images (img tags)", variable=var_images)
checkbox_images.pack()

# Button to start the scraping
scrape_button = tk.Button(root, text="Start Scraping", command=scrape)
scrape_button.pack(pady=20)

# Start the GUI event loop
root.mainloop()



# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# import json
# import tkinter as tk
# from tkinter import messagebox
# from tkinter import font

# # Function to start the web scraping process
# def scrape():
#     # Get URL from the user input
#     url = url_entry.get()

#     # Send GET request
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # Raise an exception for 4xx/5xx responses
#         messagebox.showinfo("Success", "Successfully fetched the webpage")

#         # Parse the content
#         soup = BeautifulSoup(response.text, 'html.parser')

#         # Extract data based on user selection
#         data = {}

#         if var_headings.get():
#             headings = [h.text.strip() for i in range(1, 7) for h in soup.find_all(f'h{i}')]
#             data["Headings"] = headings

#         if var_paragraphs.get():
#             paragraphs = [p.text.strip() for p in soup.find_all('p')]
#             data["Paragraphs"] = paragraphs

#         if var_lists.get():
#             lists = [li.text.strip() for ul in soup.find_all('ul') for li in ul.find_all('li')]
#             data["Lists"] = lists

#         if var_links.get():
#             links = [a['href'] for a in soup.find_all('a', href=True)]
#             data["Links"] = links

#         if var_images.get():
#             images = [img['src'] for img in soup.find_all('img', src=True)]
#             data["Images"] = images

#         # Save data to JSON
#         url_name = url.split("/")[-1]
#         json_file_name = f"{url_name}.json"
#         with open(json_file_name, 'w') as f:
#             json.dump(data, f, indent=4)

#         # Save data to CSV
#         data_dict = {key: pd.Series(value) for key, value in data.items()}
#         csv_df = pd.DataFrame(data_dict)
#         csv_file_name = f"{url_name}.csv"
#         csv_df.to_csv(csv_file_name, index=False)

#         messagebox.showinfo("Success", f"Data saved to {json_file_name} and {csv_file_name}")

#     except requests.exceptions.RequestException as e:
#         messagebox.showerror("Error", f"Failed to retrieve the webpage: {e}")

# # Create main window
# root = tk.Tk()
# root.title("Web Scraping Tool")
# root.geometry("600x600")  # Set the window size
# root.config(bg="#f0f0f0")  # Light gray background

# # Define custom font
# custom_font = font.Font(family="Arial", size=12, weight="bold")

# # Create a frame for the content
# frame = tk.Frame(root, bg="#f0f0f0")
# frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

# # Create a title label
# title_label = tk.Label(frame, text="Web Scraping Tool", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333")
# title_label.pack(pady=10)

# # Create a label and entry for the URL
# url_label = tk.Label(frame, text="Enter URL to scrape:", font=custom_font, bg="#f0f0f0", fg="#333")
# url_label.pack(pady=5)

# # Create a frame for the URL entry with padding
# entry_frame = tk.Frame(frame, bg="#f0f0f0")
# entry_frame.pack(pady=10)

# # Entry for the URL (without padx directly on Entry)
# url_entry = tk.Entry(entry_frame, font=custom_font, width=45, relief="solid", bd=2)
# url_entry.pack(padx=10, pady=5)  # Add padding for the Entry widget using pack() method

# # Checkboxes for selecting what data to scrape
# var_headings = tk.BooleanVar(value=True)
# var_paragraphs = tk.BooleanVar(value=True)
# var_lists = tk.BooleanVar(value=True)
# var_links = tk.BooleanVar(value=True)
# var_images = tk.BooleanVar(value=True)

# checkbox_frame = tk.Frame(frame, bg="#f0f0f0")
# checkbox_frame.pack(pady=10)

# checkbox_headings = tk.Checkbutton(checkbox_frame, text="Headings (h1, h2, h3, ...)", variable=var_headings, font=custom_font, bg="#f0f0f0")
# checkbox_headings.grid(row=0, column=0, sticky="w", padx=10)

# checkbox_paragraphs = tk.Checkbutton(checkbox_frame, text="Paragraphs", variable=var_paragraphs, font=custom_font, bg="#f0f0f0")
# checkbox_paragraphs.grid(row=1, column=0, sticky="w", padx=10)

# checkbox_lists = tk.Checkbutton(checkbox_frame, text="Lists (ul, ol)", variable=var_lists, font=custom_font, bg="#f0f0f0")
# checkbox_lists.grid(row=2, column=0, sticky="w", padx=10)

# checkbox_links = tk.Checkbutton(checkbox_frame, text="Links (a tags)", variable=var_links, font=custom_font, bg="#f0f0f0")
# checkbox_links.grid(row=3, column=0, sticky="w", padx=10)

# checkbox_images = tk.Checkbutton(checkbox_frame, text="Images (img tags)", variable=var_images, font=custom_font, bg="#f0f0f0")
# checkbox_images.grid(row=4, column=0, sticky="w", padx=10)

# # Button to start the scraping
# scrape_button = tk.Button(frame, text="Start Scraping", command=scrape, font=("Arial", 14), bg="#4CAF50", fg="white", relief="raised", bd=2, padx=20, pady=10)
# scrape_button.pack(pady=20)

# Start the GUI event loop
# root.mainloop()
