import os
import sys
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
import pdb

# Create the images directory if it doesn't exist
if not os.path.exists('images'):
    os.makedirs('images')

# Initialize index.json data structure
index_data = {"images": []}

def download_image(img_url, page_url, depth):
    try:
        response = requests.get(img_url)
        response.raise_for_status()
        img_name = os.path.join('images', img_url.split('/')[-1])

        # pdb.set_trace()

        with open(img_name, 'wb') as img_file:
            img_file.write(response.content)
        
        index_data["images"].append({"url": img_url, "page": page_url, "depth": depth})
    except (requests.RequestException, ValueError) as e:
        print(f"Failed to download {img_url}: {e}")

def crawl_page(url, depth, max_depth):
    if depth > max_depth:
        return

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find and download all images on the current page
        for img_tag in soup.find_all('img'):
            img_url = img_tag.get('src')
            if not img_url:
                continue
            
            img_url = urljoin(url, img_url)  # Handle relative URLs
            download_image(img_url, url, depth)
        
        # Recursively crawl linked pages if depth allows
        if depth < max_depth:
            for a_tag in soup.find_all('a', href=True):
                next_url = urljoin(url, a_tag['href'])
                crawl_page(next_url, depth + 1, max_depth)
    
    except requests.RequestException as e:
        print(f"Failed to crawl {url}: {e}")

def save_index():
    with open('images/index.json', 'w') as json_file:
        json.dump(index_data, json_file, indent=4)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: crawl <start_url> <depth>")
        sys.exit(1)

    start_url = sys.argv[1]
    max_depth = int(sys.argv[2])

    crawl_page(start_url, 1, max_depth)
    save_index()
    print("Crawling completed.", start_url, max_depth)
