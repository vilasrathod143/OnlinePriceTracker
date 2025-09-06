import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict
import time
import random

class AlternativeScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def search_amazon(self, query: str, limit: int = 2) -> List[Dict]:
        """Search Amazon for alternative products"""
        try:
            search_url = f"https://www.amazon.in/s?k={query.replace(' ', '+')}"
            response = requests.get(search_url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            products = []
            items = soup.find_all('div', {'data-component-type': 's-search-result'})[:limit]
            
            for item in items:
                try:
                    name_elem = item.find('h2', class_='a-size-mini')
                    if not name_elem:
                        name_elem = item.find('span', class_='a-size-medium')
                    
                    price_elem = item.find('span', class_='a-price-whole')
                    if not price_elem:
                        price_elem = item.find('span', class_='a-offscreen')
                    
                    image_elem = item.find('img', class_='s-image')
                    link_elem = item.find('h2').find('a') if item.find('h2') else None
                    
                    if name_elem and price_elem:
                        price_text = price_elem.text.replace(',', '').replace('₹', '')
                        price = float(re.findall(r'\d+', price_text)[0]) if re.findall(r'\d+', price_text) else 0
                        
                        products.append({
                            'name': name_elem.text.strip()[:100],
                            'price': price,
                            'platform': 'Amazon',
                            'url': f"https://amazon.in{link_elem['href']}" if link_elem else '#',
                            'image_url': image_elem['src'] if image_elem else ''
                        })
                except:
                    continue
            
            return products
        except:
            return []
    
    def search_flipkart(self, query: str, limit: int = 2) -> List[Dict]:
        """Search Flipkart for alternative products"""
        try:
            search_url = f"https://www.flipkart.com/search?q={query.replace(' ', '%20')}"
            response = requests.get(search_url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            products = []
            items = soup.find_all('div', class_='_1AtVbE')[:limit]
            
            for item in items:
                try:
                    name_elem = item.find('div', class_='_4rR01T')
                    price_elem = item.find('div', class_='_30jeq3')
                    image_elem = item.find('img', class_='_396cs4')
                    link_elem = item.find('a', class_='_1fQZEK')
                    
                    if name_elem and price_elem:
                        price_text = price_elem.text.replace(',', '').replace('₹', '')
                        price = float(re.findall(r'\d+', price_text)[0]) if re.findall(r'\d+', price_text) else 0
                        
                        products.append({
                            'name': name_elem.text.strip()[:100],
                            'price': price,
                            'platform': 'Flipkart',
                            'url': f"https://flipkart.com{link_elem['href']}" if link_elem else '#',
                            'image_url': image_elem['src'] if image_elem else ''
                        })
                except:
                    continue
            
            return products
        except:
            return []
    
    def get_alternatives(self, product_name: str, platform: str) -> List[Dict]:
        """Get alternative products from different platforms"""
        alternatives = []
        
        # Extract key search terms
        search_terms = ' '.join(product_name.split()[:3])
        
        # Search other platforms
        if platform != 'Amazon':
            alternatives.extend(self.search_amazon(search_terms, 2))
            time.sleep(random.uniform(1, 2))
        
        if platform != 'Flipkart':
            alternatives.extend(self.search_flipkart(search_terms, 2))
            time.sleep(random.uniform(1, 2))
        
        return alternatives