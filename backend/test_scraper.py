from enhanced_scraper import EnhancedScraper

def test_scrapers():
    scraper = EnhancedScraper()
    
    test_urls = [
        "https://www.amazon.in/realme-Wireless-Earbuds-Spatial-Charging/dp/B0DBGP48NW/?th=1",
        "https://www.flipkart.com/nescafe-classic-coffee-imported-roast-ground/p/itmeb2db85bd2d02",
        "https://www.myntra.com/flip-flops/hrx+by+hrithik+roshan/hrx-by-hrithik-roshan-men-black-printed--sliders/23773922/buy"
    ]
    
    for url in test_urls:
        print(f"\nTesting: {url}")
        result = scraper.scrape_product(url)
        if result:
            print(f"Name: {result['name']}")
            print(f"Price: ₹{result['price']}")
            print(f"Platform: {result['platform']}")
            print(f"Image: {result['image_url'][:100]}...")
        else:
            print("Failed to scrape")

if __name__ == "__main__":
    test_scrapers()