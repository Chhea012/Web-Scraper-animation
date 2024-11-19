import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Initialize Selenium WebDriver
def init_driver():
    """Initialize Selenium WebDriver."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    return driver

# Function to scrape product names and prices
def scrape_data(driver, url):
    """Scrape data from the webpage (product names and prices)."""
    driver.get(url)
    time.sleep(2)  # Wait for the page to load (you can adjust the time based on the website)
    
    # Find product names and prices using CSS selectors (Modify these selectors for the target webpage)
    products = driver.find_elements(By.CSS_SELECTOR, ".product-title")  # Example selector for product names
    prices = driver.find_elements(By.CSS_SELECTOR, ".price")  # Example selector for product prices
    
    # Create a list of dictionaries to store scraped data
    scraped_data = []
    for product, price in zip(products, prices):
        scraped_data.append({
            "Product Name": product.text.strip(),
            "Price": price.text.strip()
        })
    
    return scraped_data

# Function to save data to CSV and JSON
def save_data(scraped_data, filename):
    """Save scraped data to CSV and JSON files."""
    # Save as JSON
    with open(f"{filename}.json", "w") as json_file:
        json.dump(scraped_data, json_file, indent=4)

    # Save as CSV using pandas
    df = pd.DataFrame(scraped_data)
    df.to_csv(f"{filename}.csv", index=False)

    print(f"Data saved as {filename}.csv and {filename}.json")

# Main function to orchestrate the scraping process
def main():
    url = "https://www.example.com/products"  # Replace with the actual URL you want to scrape
    filename = "scraped_data"  # Base filename for saving data

    # Initialize the WebDriver
    driver = init_driver()

    try:
        # Scrape data
        scraped_data = scrape_data(driver, url)
        
        # Save the scraped data to CSV and JSON
        save_data(scraped_data, filename)
    finally:
        # Close the WebDriver
        driver.quit()

# Run the script
if __name__ == "__main__":
    main()

