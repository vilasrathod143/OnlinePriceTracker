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
import json

class EnhancedScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
    def setup_driver(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument(f'--user-agent={self.headers["User-Agent"]}')
        
        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
    
    def extract_price(self, text: str) -> Optional[float]:
        patterns = [
            r'₹[\s]*([0-9,]+(?:\.[0-9]{2})?)',
            r'Rs[\s]*([0-9,]+(?:\.[0-9]{2})?)',
            r'([0-9,]+(?:\.[0-9]{2})?)[\s]*₹'
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
        driver = self.setup_driver()
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "productTitle")))
            
            product_data = {
                'name': '',
                'price': 0.0,
                'image_url': '',
                'seller': 'Amazon',
                'platform': 'Amazon'
            }
            
            # Product name
            try:
                name_elem = driver.find_element(By.ID, "productTitle")
                product_data['name'] = name_elem.text.strip()
            except:
                pass
            
            # Price extraction with multiple strategies
            price_found = False
            
            # Strategy 1: Amazon price elements (updated selectors)
            price_selectors = [
                '.a-price.priceToPay .a-price-whole',
                '.a-price.reinventPricePriceToPayMargin .a-price-whole', 
                'span.a-price-whole',
                '.a-price .a-offscreen',
                '#apex_desktop .a-price .a-price-whole',
                '.a-section .a-price .a-price-whole'
            ]
            
            for selector in price_selectors:
                try:
                    price_elem = driver.find_element(By.CSS_SELECTOR, selector)
                    price_text = price_elem.text.strip().replace(',', '')
                    if price_text and price_text.isdigit():
                        price = float(price_text)
                        if price > 0:
                            product_data['price'] = price
                            price_found = True
                            break
                except:
                    continue
                    
            # Try offscreen price if whole number not found
            if not price_found:
                try:
                    offscreen_elem = driver.find_element(By.CSS_SELECTOR, '.a-price .a-offscreen')
                    price_text = offscreen_elem.text.strip()
                    price = self.extract_price(price_text)
                    if price and price > 0:
                        product_data['price'] = price
                        price_found = True
                except:
                    pass
            
            # Strategy 2: JSON-LD structured data
            if not price_found:
                try:
                    scripts = driver.find_elements(By.XPATH, "//script[@type='application/ld+json']")
                    for script in scripts:
                        try:
                            data = json.loads(script.get_attribute('innerHTML'))
                            if isinstance(data, list):
                                data = data[0]
                            if 'offers' in data:
                                price = float(data['offers']['price'])
                                product_data['price'] = price
                                price_found = True
                                break
                        except:
                            continue
                except:
                    pass
            
            # Strategy 3: Page source analysis for Amazon
            if not price_found:
                page_source = driver.page_source
                # Look for price in various formats
                price_patterns = [
                    r'"price":\s*"([0-9,]+(?:\.[0-9]{2})?)"',
                    r'"displayPrice":\s*"[^"]*?([0-9,]+(?:\.[0-9]{2})?)"',
                    r'priceToPay[^>]*>.*?₹([0-9,]+)',
                    r'a-price-whole[^>]*>([0-9,]+)'
                ]
                
                for pattern in price_patterns:
                    matches = re.findall(pattern, page_source)
                    if matches:
                        try:
                            price = float(matches[0].replace(',', ''))
                            if 100 < price < 1000000:  # Reasonable price range
                                product_data['price'] = price
                                price_found = True
                                break
                        except:
                            continue
            
            # Image
            try:
                img_selectors = ['#landingImage', '.a-dynamic-image', '#imgTagWrapperId img']
                for selector in img_selectors:
                    try:
                        img_elem = driver.find_element(By.CSS_SELECTOR, selector)
                        product_data['image_url'] = img_elem.get_attribute('src')
                        break
                    except:
                        continue
            except:
                pass
            
            return product_data
            
        except Exception as e:
            print(f"Amazon scraping error: {e}")
            return None
        finally:
            driver.quit()
    
    def scrape_flipkart(self, url: str) -> Dict:
        driver = self.setup_driver()
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1, .B_NuCI")))
            
            product_data = {
                'name': '',
                'price': 0.0,
                'image_url': '',
                'seller': 'Flipkart',
                'platform': 'Flipkart'
            }
            
            # Product name
            name_selectors = ['h1 span', '.B_NuCI', '._35KyD6', '.VU-ZEz']
            for selector in name_selectors:
                try:
                    name_elem = driver.find_element(By.CSS_SELECTOR, selector)
                    product_data['name'] = name_elem.text.strip()
                    break
                except:
                    continue
            
            # Price
            price_selectors = [
                '.Nx9bqj.CxhGGd',
                '._30jeq3._16Jk6d',
                '._1_WHN1',
                '.CEmiEU .Nx9bqj'
            ]
            
            for selector in price_selectors:
                try:
                    price_elem = driver.find_element(By.CSS_SELECTOR, selector)
                    price_text = price_elem.text.strip()
                    if price_text and '₹' in price_text:
                        price = self.extract_price(price_text)
                        if price and price > 0:
                            product_data['price'] = price
                            break
                except:
                    continue
            
            # Image - Flipkart with better selectors
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "img"))
                )
            except:
                pass
                
            img_selectors = [
                '._4WELSP img',
                '.DByuf4.IZexXJ.jLEJ7H',
                '._396cs4._2amPTt._3qGmMb',
                'img[src*="rukminim"]',
                'img[data-src*="rukminim"]',
                '.vU5WPQ img',
                '._8id3KM img'
            ]
            
            for selector in img_selectors:
                try:
                    img_elem = driver.find_element(By.CSS_SELECTOR, selector)
                    img_src = img_elem.get_attribute('src') or img_elem.get_attribute('data-src')
                    if img_src and ('rukminim' in img_src or 'flixcart.com' in img_src):
                        # Convert to higher quality image
                        if 'rukminim' in img_src and '128/128' in img_src:
                            img_src = img_src.replace('128/128', '416/416')
                        product_data['image_url'] = img_src
                        break
                except:
                    continue
            
            return product_data
            
        except Exception as e:
            print(f"Flipkart scraping error: {e}")
            return None
        finally:
            driver.quit()
    
    def scrape_myntra(self, url: str) -> Dict:
        driver = self.setup_driver()
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1, .pdp-name")))
            
            product_data = {
                'name': '',
                'price': 0.0,
                'image_url': '',
                'seller': 'Myntra',
                'platform': 'Myntra'
            }
            
            # Product name
            name_selectors = ['h1.pdp-name', '.pdp-name', 'h1']
            for selector in name_selectors:
                try:
                    name_elem = driver.find_element(By.CSS_SELECTOR, selector)
                    product_data['name'] = name_elem.text.strip()
                    break
                except:
                    continue
            
            # Price
            price_selectors = [
                '.pdp-price strong',
                '.pdp-price .pdp-price-info',
                'span.pdp-price',
                '.price-info .price'
            ]
            
            for selector in price_selectors:
                try:
                    price_elem = driver.find_element(By.CSS_SELECTOR, selector)
                    price_text = price_elem.text.strip()
                    if price_text and ('₹' in price_text or price_text.replace(',', '').isdigit()):
                        price = self.extract_price(price_text) if '₹' in price_text else float(price_text.replace(',', ''))
                        if price and price > 0:
                            product_data['price'] = price
                            break
                except:
                    continue
            
            # Image - Wait for Myntra images to load
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "img"))
                )
            except:
                pass
                
            img_selectors = [
                'img.image-grid-image',
                '.image-grid-container img',
                '.pdp-image img', 
                'img[src*="assets.myntassets.com"]',
                'img[data-src*="assets.myntassets.com"]',
                '.image-grid img',
                'img[alt]'
            ]
            
            for selector in img_selectors:
                try:
                    img_elem = driver.find_element(By.CSS_SELECTOR, selector)
                    img_src = img_elem.get_attribute('src') or img_elem.get_attribute('data-src')
                    if img_src and ('myntassets.com' in img_src or 'http' in img_src):
                        product_data['image_url'] = img_src
                        break
                except:
                    continue
            
            return product_data
            
        except Exception as e:
            print(f"Myntra scraping error: {e}")
            return None
        finally:
            driver.quit()
    
    def scrape_product(self, url: str) -> Optional[Dict]:
        url_lower = url.lower()
        
        if 'amazon' in url_lower:
            return self.scrape_amazon(url)
        elif 'flipkart' in url_lower:
            return self.scrape_flipkart(url)
        elif 'myntra' in url_lower:
            return self.scrape_myntra(url)
        else:
            # Generic scraper fallback
            try:
                response = requests.get(url, headers=self.headers)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                title = soup.find('title')
                name = title.text if title else 'Unknown Product'
                
                price_text = soup.get_text()
                price = self.extract_price(price_text)
                
                return {
                    'name': name[:200],
                    'price': price or 0.0,
                    'image_url': '',
                    'seller': 'Unknown',
                    'platform': 'Other'
                }
            except Exception as e:
                print(f"Generic scraping error: {e}")
                return None