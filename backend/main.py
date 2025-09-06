# Import FastAPI framework and dependencies
from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import HTTPBearer  # For JWT token authentication
from fastapi.middleware.cors import CORSMiddleware  # Enable cross-origin requests
from sqlalchemy.orm import Session  # Database session management
from pydantic import BaseModel, EmailStr  # Data validation models
from typing import List, Optional  # Type hints
from datetime import datetime, timedelta  # Date/time handling
import schedule  # Task scheduling
import threading  # Background threads
import time  # Time utilities

# Import custom modules
from database import get_db, User, TrackedProduct, PriceHistory, AlternativeProduct  # Database models
from auth import get_password_hash, verify_password, create_access_token, get_current_user  # Authentication
from enhanced_scraper import EnhancedScraper  # Web scraping functionality
from agent import PriceTrackerAgent  # AI agent for price analysis
from email_service import EmailService  # Email notifications

# Create FastAPI application instance
app = FastAPI(title="Price Tracker Agent API", version="1.0.0")

# Configure CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,  # Allow cookies/auth headers
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Initialize core services
scraper = EnhancedScraper()  # Web scraping service
agent = PriceTrackerAgent()  # AI analysis service
email_service = EmailService()  # Email notification service

# Pydantic models for request/response validation
class UserCreate(BaseModel):
    """Model for user registration data"""
    email: EmailStr  # Validated email address
    password: str    # Plain text password (will be hashed)

class UserLogin(BaseModel):
    """Model for user login data"""
    email: EmailStr  # User's email
    password: str    # User's password

class ProductTrack(BaseModel):
    """Model for product tracking request"""
    url: str  # Product URL to track

class ProductResponse(BaseModel):
    """Model for product data response"""
    id: int                    # Unique product ID
    product_name: str          # Product name
    current_price: float       # Current price
    original_price: float      # Original price when first tracked
    image_url: Optional[str]   # Product image URL (optional)
    seller: str                # Seller name
    platform: str              # E-commerce platform
    product_url: str           # Original product URL
    created_at: datetime       # When tracking started

# Auth endpoints
@app.post("/auth/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Send welcome email
    email_service.send_welcome_email(user.email, user.email.split('@')[0])
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/auth/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Product tracking endpoints
@app.post("/products/track")
async def track_product(
    product: ProductTrack, 
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if already tracking
    existing = db.query(TrackedProduct).filter(
        TrackedProduct.user_id == current_user.id,
        TrackedProduct.product_url == product.url
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Product already being tracked")
    
    # Scrape product data
    product_data = scraper.scrape_product(product.url)
    if not product_data:
        raise HTTPException(status_code=400, detail="Unable to scrape product data")
    
    # Create tracked product
    db_product = TrackedProduct(
        user_id=current_user.id,
        product_url=product.url,
        product_name=product_data['name'],
        current_price=product_data['price'],
        original_price=product_data['price'],
        image_url=product_data.get('image_url', ''),
        seller=product_data['seller'],
        platform=product_data['platform']
    )
    
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    # Add initial price history
    price_history = PriceHistory(
        product_id=db_product.id,
        price=product_data['price']
    )
    db.add(price_history)
    db.commit()
    
    # Generate alternatives using AI
    background_tasks.add_task(generate_alternatives, db_product.id, product_data)
    
    return {"message": "Product tracking started", "product_id": db_product.id}

@app.get("/products/my-products", response_model=List[ProductResponse])
async def get_my_products(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    products = db.query(TrackedProduct).filter(
        TrackedProduct.user_id == current_user.id,
        TrackedProduct.is_active == True
    ).all()
    
    return products

@app.get("/products/{product_id}")
async def get_product_details(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    product = db.query(TrackedProduct).filter(
        TrackedProduct.id == product_id,
        TrackedProduct.user_id == current_user.id
    ).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Get price history
    price_history = db.query(PriceHistory).filter(
        PriceHistory.product_id == product_id
    ).order_by(PriceHistory.timestamp.desc()).limit(30).all()
    
    # Get AI analysis
    history_data = [{"price": p.price, "timestamp": p.timestamp} for p in price_history]
    ai_analysis = agent.analyze_product(product.product_name, product.current_price, history_data)
    
    # Get alternatives
    alternatives = db.query(AlternativeProduct).filter(
        AlternativeProduct.original_product_id == product_id
    ).all()
    
    return {
        "product": product,
        "price_history": price_history,
        "ai_analysis": ai_analysis,
        "alternatives": alternatives
    }

@app.delete("/products/{product_id}")
async def stop_tracking(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    product = db.query(TrackedProduct).filter(
        TrackedProduct.id == product_id,
        TrackedProduct.user_id == current_user.id
    ).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product.is_active = False
    db.commit()
    
    return {"message": "Product tracking stopped"}

@app.get("/dashboard/insights")
async def get_dashboard_insights(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    products = db.query(TrackedProduct).filter(
        TrackedProduct.user_id == current_user.id,
        TrackedProduct.is_active == True
    ).all()
    
    if not products:
        return {"message": "No products being tracked"}
    
    # Get AI suggestions
    products_data = [
        {
            "name": p.product_name,
            "price": p.current_price,
            "platform": p.platform
        } for p in products
    ]
    
    suggestions = agent.smart_tracking_suggestions(products_data)
    
    # Calculate savings
    total_savings = sum(
        (p.original_price - p.current_price) for p in products 
        if p.current_price < p.original_price
    )
    
    return {
        "total_products": len(products),
        "total_savings": total_savings,
        "ai_suggestions": suggestions,
        "recent_products": products[:5]
    }

# Background task functions
def generate_alternatives(product_id: int, product_data: dict):
    """Generate alternative products using real scraping"""
    from alternative_scraper import AlternativeScraper
    
    db = next(get_db())
    alt_scraper = AlternativeScraper()
    
    # Get real alternatives from other platforms
    real_alternatives = alt_scraper.get_alternatives(
        product_data['name'], 
        product_data['platform']
    )
    
    # Add AI-generated alternatives as fallback
    ai_alternatives = agent.find_alternatives(
        product_data['name'], 
        product_data['price'], 
        product_data['platform']
    )
    
    # Combine real and AI alternatives
    all_alternatives = real_alternatives + ai_alternatives[:3]
    
    for alt in all_alternatives:
        try:
            # Handle different data formats
            if 'price' in alt:
                price = float(alt['price'])
            elif 'estimated_price' in alt:
                if isinstance(alt['estimated_price'], str):
                    price_str = alt['estimated_price'].replace('₹', '').replace(',', '').strip()
                    if '-' in price_str:
                        price = float(price_str.split('-')[0].strip())
                    else:
                        price = float(price_str)
                else:
                    price = float(alt['estimated_price'])
            else:
                price = 0.0
                
            db_alt = AlternativeProduct(
                original_product_id=product_id,
                name=alt['name'][:200],
                price=price,
                url=alt.get('url', '#'),
                platform=alt['platform'],
                image_url=alt.get('image_url', ''),
                similarity_score=0.9 if 'price' in alt else 0.7
            )
            db.add(db_alt)
        except Exception as e:
            print(f"Error processing alternative: {e}")
            continue
    
    db.commit()
    db.close()

def check_price_updates():
    """Background task to check price updates"""
    db = next(get_db())
    
    active_products = db.query(TrackedProduct).filter(
        TrackedProduct.is_active == True
    ).all()
    
    for product in active_products:
        try:
            # Scrape current price
            current_data = scraper.scrape_product(product.product_url)
            if not current_data:
                continue
            
            new_price = current_data['price']
            old_price = product.current_price
            
            # Check if price changed significantly (>1% change)
            if abs(new_price - old_price) / old_price > 0.01:
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
                    alert_content = agent.generate_price_alert_content(
                        product.product_name, old_price, new_price, product.product_url
                    )
                    
                    product_data = {
                        'name': product.product_name,
                        'old_price': old_price,
                        'new_price': new_price,
                        'platform': product.platform,
                        'url': product.product_url
                    }
                    
                    email_service.send_price_alert(user.email, product_data, alert_content)
                
                db.commit()
                
        except Exception as e:
            print(f"Error checking price for product {product.id}: {e}")
            continue
    
    db.close()

# Schedule price checking
schedule.every(6).hours.do(check_price_updates)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

# Start scheduler in background thread
scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)