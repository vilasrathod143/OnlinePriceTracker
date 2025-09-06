import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
from typing import Dict, Optional

class ProductScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def setup_driver(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        return webdriver.Chrome(options=options)
    
    def extract_price(self, text: str) -> Optional[float]:
        # Multiple price patterns
        patterns = [
            r'₹[\s]*([\d,]+(?:\.\d{2})?)',
            r'Rs[\s]*([\d,]+(?:\.\d{2})?)',
            r'MRP[\s]*₹[\s]*([\d,]+(?:\.\d{2})?)',
            r'Price[\s]*₹[\s]*([\d,]+(?:\.\d{2})?)',
            r'([\d,]+(?:\.\d{2})?)[\s]*₹'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text.replace(',', ''))
            if matches:
                try:
                    return float(matches[0])
                except ValueError:
                    continue
        return None
    
    def scrape_amazon(self, url: str) -> Dict:
        try:
            driver = self.setup_driver()
            driver.get(url)
            time.sleep(3)
            
            product_data = {
                'name': '',
                'price': 0.0,
                'image_url': '',
                'seller': 'Amazon',
                'platform': 'Amazon'
            }
            
            # Product name
            try:
                name_element = driver.find_element(By.ID, "productTitle")
                product_data['name'] = name_element.text.strip()
            except:
                pass
            
            # Price - Amazon specific selectors
            price_selectors = [
                'span.a-price-whole',
                '.a-price .a-offscreen',
                '.priceToPay .a-price-whole',
                '.savingPriceOverride',
                '#priceblock_dealprice',
                '#priceblock_ourprice'
            ]
            
            for selector in price_selectors:
                try:
                    price_element = driver.find_element(By.CSS_SELECTOR, selector)
                    price_text = price_element.text.strip()
                    if price_text and '₹' in price_text:
                        price = self.extract_price(price_text)
                        if price and price > 0:
                            product_data['price'] = price
                            break
                except:
                    continue
            
            # Image
            try:
                img_element = driver.find_element(By.CSS_SELECTOR, '#landingImage, .a-dynamic-image')
                product_data['image_url'] = img_element.get_attribute('src')
            except:
                pass
            
            driver.quit()
            return product_data
            
        except Exception as e:
            print(f"Error scraping Amazon: {e}")
            return None
    
    def scrape_flipkart(self, url: str) -> Dict:
        try:
            driver = self.setup_driver()
            driver.get(url)
            time.sleep(3)
            
            product_data = {
                'name': '',
                'price': 0.0,
                'image_url': '',
                'seller': 'Flipkart',
                'platform': 'Flipkart'
            }
            
            # Product name
            try:
                name_element = driver.find_element(By.CSS_SELECTOR, '.B_NuCI, ._35KyD6')
                product_data['name'] = name_element.text.strip()
            except:
                pass
            
            # Price - Flipkart specific selectors
            price_selectors = [
                '.Nx9bqj.CxhGGd',
                '._30jeq3._16Jk6d',
                '._1_WHN1',
                '.CEmiEU .Nx9bqj',
                '._16Jk6d'
            ]
            
            for selector in price_selectors:
                try:
                    price_element = driver.find_element(By.CSS_SELECTOR, selector)
                    price_text = price_element.text.strip()
                    if price_text and '₹' in price_text:
                        price = self.extract_price(price_text)
                        if price and price > 0:
                            product_data['price'] = price
                            break
                except:
                    continue
            
            # Image
            try:
                img_element = driver.find_element(By.CSS_SELECTOR, '._396cs4._2amPTt._3qGmMb')
                product_data['image_url'] = img_element.get_attribute('src')
            except:
                pass
            
            driver.quit()
            return product_data
            
        except Exception as e:
            print(f"Error scraping Flipkart: {e}")
            return None
    
    def scrape_product(self, url: str) -> Optional[Dict]:
        if 'amazon' in url.lower():
            return self.scrape_amazon(url)
        elif 'flipkart' in url.lower():
            return self.scrape_flipkart(url)
        else:
            # Generic scraper
            try:
                response = requests.get(url, headers=self.headers)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Try to extract basic info
                title = soup.find('title')
                name = title.text if title else 'Unknown Product'
                
                # Try to find price in common patterns
                price_text = soup.get_text()
                price = self.extract_price(price_text)
                
                return {
                    'name': name[:100],
                    'price': price or 0.0,
                    'image_url': '',
                    'seller': 'Unknown',
                    'platform': 'Other'
                }
            except Exception as e:
                print(f"Error with generic scraper: {e}")
                return None