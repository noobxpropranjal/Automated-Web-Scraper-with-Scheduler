from selenium.webdriver.common.by import By
import sqlite3
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import schedule
import time
from datetime import datetime

# Setup SQLite DB and create table
conn = sqlite3.connect('scraped_data.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price TEXT,
        scrape_time TEXT
    )
''')
conn.commit()

# Setup Selenium WebDriver options (headless = no browser window)
chrome_options = Options()
chrome_options.add_argument("--headless")

def scrape_data():
    print(f"Scraping started at {datetime.now()}")

    # Initialize WebDriver (make sure chromedriver is in your PATH or project folder)
    driver = webdriver.Chrome(options=chrome_options)
    
    # Example: Scrape product names and prices from an example e-commerce site
    url = "https://webscraper.io/test-sites/e-commerce/ajax/computers/laptops"
    driver.get(url)
    
    products = driver.find_elements(By.CLASS_NAME, "thumbnail")

    scraped_items = []
    for product in products:
        name = product.find_element(By.CLASS_NAME, "title").text
        price = product.find_element(By.CLASS_NAME, "price").text
        scraped_items.append((name, price, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
    driver.quit()
    
    # Save to database
    c.executemany("INSERT INTO products (name, price, scrape_time) VALUES (?, ?, ?)", scraped_items)
    conn.commit()
    print(f"Scraped and saved {len(scraped_items)} items.")

def export_to_csv():
    df = pd.read_sql_query("SELECT * FROM products", conn)
    df.to_csv("scraped_products.csv", index=False)
    print("Exported data to scraped_products.csv")

# Schedule the scraper to run every 1 hour
schedule.every(1).hours.do(scrape_data)

print("Scheduler started. Press Ctrl+C to exit.")

# Run once at start
scrape_data()

while True:
    schedule.run_pending()
    time.sleep(1)

# schedule
    import schedule
    import time
    from datetime import datetime

    def scrape_data():
    # Your existing scraping code here
     print(f"Scraping started at {datetime.now()}")
    # ... scrape and save data ...
    print("Scraped and saved items.")

    # Schedule the job every 30 minutes
    schedule.every(30).minutes.do(scrape_data)

    print("Scheduler started. Press Ctrl+C to stop.")

# Run once before starting scheduler (optional)
    scrape_data()

    while True:
      schedule.run_pending()
      time.sleep(1)
