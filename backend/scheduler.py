import schedule
import time
import threading
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal, TrackedProduct, PriceHistory, User
from enhanced_scraper import EnhancedScraper
from agent import PriceTrackerAgent
from email_service import EmailService

class PriceScheduler:
    def __init__(self):
        self.scraper = EnhancedScraper()
        self.agent = PriceTrackerAgent()
        self.email_service = EmailService()
        self.is_running = False
    
    def check_all_prices(self):
        """Check prices for all active products"""
        print(f"[{datetime.now()}] Starting price check...")
        
        db = SessionLocal()
        try:
            active_products = db.query(TrackedProduct).filter(
                TrackedProduct.is_active == True
            ).all()
            
            print(f"Found {len(active_products)} active products to check")
            
            for product in active_products:
                try:
                    self.check_single_product(db, product)
                    time.sleep(2)  # Rate limiting
                except Exception as e:
                    print(f"Error checking product {product.id}: {e}")
                    continue
            
            db.commit()
            print(f"[{datetime.now()}] Price check completed")
            
        except Exception as e:
            print(f"Error in price check: {e}")
            db.rollback()
        finally:
            db.close()
    
    def check_single_product(self, db: Session, product: TrackedProduct):
        """Check price for a single product"""
        print(f"Checking: {product.product_name}")
        
        # Scrape current price
        current_data = self.scraper.scrape_product(product.product_url)
        if not current_data or not current_data.get('price'):
            print(f"Failed to scrape price for {product.product_name}")
            return
        
        new_price = current_data['price']
        old_price = product.current_price
        
        # Check if price changed significantly (>1% change)
        if abs(new_price - old_price) / old_price > 0.01:
            print(f"Price changed: {old_price} -> {new_price}")
            
            # Update product price
            product.current_price = new_price
            
            # Add to price history
            price_history = PriceHistory(
                product_id=product.id,
                price=new_price
            )
            db.add(price_history)
            
            # Send email alert
            user = db.query(User).filter(User.id == product.user_id).first()
            if user:
                self.send_price_alert(user, product, old_price, new_price)
    
    def send_price_alert(self, user: User, product: TrackedProduct, old_price: float, new_price: float):
        """Send price alert email"""
        try:
            alert_content = self.agent.generate_price_alert_content(
                product.product_name, old_price, new_price, product.product_url
            )
            
            product_data = {
                'name': product.product_name,
                'old_price': old_price,
                'new_price': new_price,
                'platform': product.platform,
                'url': product.product_url
            }
            
            success = self.email_service.send_price_alert(user.email, product_data, alert_content)
            if success:
                print(f"Email sent to {user.email}")
            else:
                print(f"Failed to send email to {user.email}")
                
        except Exception as e:
            print(f"Error sending email: {e}")
    
    def start_scheduler(self):
        """Start the price checking scheduler"""
        if self.is_running:
            return
        
        self.is_running = True
        print("Starting price scheduler...")
        
        # Schedule price checks every 6 hours
        schedule.every(6).hours.do(self.check_all_prices)
        
        # Run initial check after 1 minute
        schedule.every(1).minutes.do(self.check_all_prices).tag('initial')
        
        def run_scheduler():
            while self.is_running:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        
        # Start scheduler in background thread
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        
        print("Price scheduler started successfully")
    
    def stop_scheduler(self):
        """Stop the scheduler"""
        self.is_running = False
        schedule.clear()
        print("Price scheduler stopped")

# Global scheduler instance
price_scheduler = PriceScheduler()