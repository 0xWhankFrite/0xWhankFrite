import requests
from bs4 import BeautifulSoup
import re
import time
import random
import json
import os

# Base URL (without page number)
base_url = "https://privatekeys.pw/keys/bitcoin/"

# Maximum page number based on your given limit
max_page = int(2.573157538607E+75)

# File to save and load visited pages
visited_pages_file = "visited_pages.json"

# Function to check the balance on the page
def get_balance(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Regex to match the balance text
    balance_text = soup.find(text=re.compile("Total balance on the page:"))
    
    if balance_text:
        # Extract balance amount
        balance = re.search(r"Total balance on the page:\s*₿\s*(\d+)", balance_text)
        if balance:
            return int(balance.group(1))
    return 0

# Function to save visited pages to a file
def save_visited_pages(visited_pages):
    with open(visited_pages_file, 'w') as f:
        json.dump(list(visited_pages), f)

# Function to load visited pages from a file
def load_visited_pages():
    if os.path.exists(visited_pages_file):
        with open(visited_pages_file, 'r') as f:
            return set(json.load(f))
    return set()

# Load previously visited pages if any
visited_pages = load_visited_pages()

# Main loop to keep checking until balance > 0
while True:
    # Pick a random page number
    page_number = random.randint(1, max_page)
    
    # Ensure the page hasn't been visited before
    while page_number in visited_pages:
        page_number = random.randint(1, max_page)
    
    # Mark this page as visited
    visited_pages.add(page_number)
    
    current_url = f"{base_url}{page_number}"
    print(f"Checking page: {page_number} -> {current_url}")
    
    balance = get_balance(current_url)
    
    if balance > 0:
        print(f"Balance found on page {page_number}: {balance} BTC")
        break
    else:
        print(f"No balance on page {page_number}.")
    
    # Save visited pages to file after each check
    save_visited_pages(visited_pages)
    
    # Delay before the next attempt
    time.sleep(.1)
