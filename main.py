import requests
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import font

class WebScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Scraping Automation")
        self.root.geometry("650x500")
        self.root.resizable(False, False)
        
        # Background Color
        self.root.config(bg="#f4f4f9")

        # Set Custom Font for the Application
        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(family="Helvetica", size=12)

        self.create_widgets()

    def create_widgets(self):
        # Header Label
        self.header_label = tk.Label(self.root, text="Web Scraping Automation", font=("Helvetica", 18, "bold"), fg="#4A90E2", bg="#f4f4f9")
        self.header_label.pack(pady=20)

        # URL Entry Section
        self.url_frame = tk.Frame(self.root, bg="#f4f4f9")
        self.url_frame.pack(pady=10)
        
        self.url_label = tk.Label(self.url_frame, text="Enter URL:", font=self.default_font, bg="#f4f4f9")
        self.url_label.grid(row=0, column=0, padx=10)

        self.url_entry = tk.Entry(self.url_frame, width=50, font=self.default_font, bd=2, relief="solid", fg="#333")
        self.url_entry.grid(row=0, column=1, padx=10)

        # Data to Scrape Section
        self.data_frame = tk.Frame(self.root, bg="#f4f4f9")
        self.data_frame.pack(pady=20)

        self.data_label = tk.Label(self.data_frame, text="Select Data to Scrape:", font=self.default_font, bg="#f4f4f9")
        self.data_label.grid(row=0, column=0, padx=10)

        self.data_options = ["Title", "Price", "Description"]
        self.data_listbox = tk.Listbox(self.data_frame, selectmode=tk.MULTIPLE, height=3, font=self.default_font, bg="#fff", bd=2, relief="solid", fg="#333")
        for item in self.data_options:
            self.data_listbox.insert(tk.END, item)
        self.data_listbox.grid(row=0, column=1, padx=10)

        # Scrape and Save Buttons
        self.button_frame = tk.Frame(self.root, bg="#f4f4f9")
        self.button_frame.pack(pady=20)

        self.scrape_button = tk.Button(self.button_frame, text="Scrape Data", command=self.scrape_data, width=20, font=self.default_font, bg="#4A90E2", fg="white", bd=0, relief="flat")
        self.scrape_button.grid(row=0, column=0, padx=10)

        self.save_button = tk.Button(self.button_frame, text="Save Data", command=self.save_data, width=20, font=self.default_font, bg="#4A90E2", fg="white", bd=0, relief="flat", state=tk.DISABLED)
        self.save_button.grid(row=0, column=1, padx=10)

        # Output Text Box
        self.output_frame = tk.Frame(self.root, bg="#f4f4f9")
        self.output_frame.pack(pady=20)

        self.output_text = tk.Text(self.output_frame, height=10, width=70, wrap=tk.WORD, font=self.default_font, bd=2, relief="solid", fg="#333", bg="#fff")
        self.output_text.pack()

    def scrape_data(self):
        url = self.url_entry.get()
        selected_data = [self.data_options[i] for i in self.data_listbox.curselection()]
        if not url:
            messagebox.showerror("Error", "Please enter a URL.")
            return
        if not selected_data:
            messagebox.showerror("Error", "Please select data to scrape.")
            return

        try:
            self.output_text.delete(1.0, tk.END)  # Clear previous output
            data = self.fetch_and_parse_data(url, selected_data)
            self.display_data(data)
            self.save_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def fetch_and_parse_data(self, url, selected_data):
        # Fetch the HTML content from the URL
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch the page. Status code: {response.status_code}")

        soup = BeautifulSoup(response.content, 'html.parser')

        # Initialize an empty list to store the scraped data
        scraped_data = []

        # Extract data based on the selected options
        for data_type in selected_data:
            if data_type == "Title":
                title = soup.title.string if soup.title else "No title found"
                scraped_data.append(("Title", title))
            elif data_type == "Price":
                price = soup.find("span", class_="price")  # Update class based on target site
                scraped_data.append(("Price", price.text.strip() if price else "Price not found"))
            elif data_type == "Description":
                description = soup.find("meta", {"name": "description"})
                scraped_data.append(("Description", description["content"] if description else "No description"))

        return scraped_data

    def display_data(self, data):
        # Display the scraped data in the Text widget
        for data_type, value in data:
            self.output_text.insert(tk.END, f"{data_type}: {value}\n")

    def save_data(self):
        # Ask user for the file type (CSV or JSON)
        file_type = messagebox.askquestion("Save As", "Do you want to save the data as CSV?", icon='question')

        data_to_save = self.output_text.get(1.0, tk.END).strip().split("\n")

        if file_type == "yes":  # Save as CSV
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
            if file_path:
                # Create DataFrame and save as CSV
                data_dict = {data.split(":")[0]: data.split(":")[1] for data in data_to_save}
                df = pd.DataFrame([data_dict])
                df.to_csv(file_path, index=False)
                messagebox.showinfo("Success", f"Data saved to {file_path}")
        else:  # Save as JSON
            file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
            if file_path:
                # Create DataFrame and save as JSON
                data_dict = {data.split(":")[0]: data.split(":")[1] for data in data_to_save}
                df = pd.DataFrame([data_dict])
                df.to_json(file_path, orient='records', lines=True)
                messagebox.showinfo("Success", f"Data saved to {file_path}")

    # New function to fetch and display raw HTML
    def fetch_html(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a URL to fetch HTML.")
            return

        try:
            # Fetch the raw HTML content of the website
            response = requests.get(url)
            if response.status_code != 200:
                raise Exception(f"Failed to fetch the page. Status code: {response.status_code}")

            # Display raw HTML content in the output text box
            self.output_text.delete(1.0, tk.END)  # Clear previous output
            self.output_text.insert(tk.END, response.text)  # Insert the raw HTML content
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while fetching HTML: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = WebScraperApp(root)

    # Add a new button for fetching HTML
    fetch_html_button = tk.Button(root, text="Fetch HTML", command=app.fetch_html, width=20, font=app.default_font, bg="#4A90E2", fg="white", bd=0, relief="flat")
    fetch_html_button.pack(pady=10)

    root.mainloop()
