import requests
from bs4 import BeautifulSoup
import csv
import argparse
from urllib.parse import urlparse
from datetime import datetime

class WebScraper:
    def __init__(self, url, user_agent=None, timeout=10):
        self.url = url
        self.headers = {'User-Agent': user_agent or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        self.timeout = timeout
        self.soup = None
        self.domain = urlparse(url).netloc

    def fetch_page(self):
        try:
            response = requests.get(self.url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            self.soup = BeautifulSoup(response.content, 'html.parser')
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page: {e}")
            return False

    def extract_data(self, selector, element_type='text', attribute=None):
        if not self.soup:
            return []

        elements = self.soup.select(selector)
        results = []

        for elem in elements:
            if element_type == 'text':
                results.append(elem.get_text(strip=True))
            elif element_type == 'attribute' and attribute:
                results.append(elem.get(attribute, ''))
            else:
                results.append(str(elem))

        return results

    def save_to_csv(self, data, filename=None):
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.domain}_{timestamp}.csv"

        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(data)
        print(f"Data saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description='Web Scraper')
    parser.add_argument('url', help='URL to scrape')
    parser.add_argument('-s', '--selector', required=True, help='CSS selector for target elements')
    parser.add_argument('-t', '--type', choices=['text', 'attribute'], default='text',
                        help='Type of data to extract')
    parser.add_argument('-a', '--attribute', help='HTML attribute to extract when using attribute type')
    parser.add_argument('-o', '--output', help='Output CSV filename')
    parser.add_argument('--user-agent', help='Custom User-Agent string')

    args = parser.parse_args()

    scraper = WebScraper(args.url, user_agent=args.user_agent)

    if not scraper.fetch_page():
        return

    data = scraper.extract_data(
        selector=args.selector,
        element_type=args.type,
        attribute=args.attribute
    )

    if data:
        print(f"Found {len(data)} elements:")
        for i, item in enumerate(data[:5], 1):  # Show first 5 results as preview
            print(f"{i}. {item[:100]}...")  # Truncate long text

        # Prepare data for CSV
        csv_data = [['Index', 'Data']] + [[i+1, item] for i, item in enumerate(data)]
        scraper.save_to_csv(csv_data, args.output)
    else:
        print("No elements found with the specified selector")

if __name__ == '__main__':
    main()