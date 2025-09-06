# Import SQLAlchemy components for database operations
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base  # Base class for models
from sqlalchemy.orm import sessionmaker, relationship  # Session management and relationships
from datetime import datetime  # For timestamp fields
import os  # Environment variables
from dotenv import load_dotenv  # Load .env file

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment or use default SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./price_tracker.db")

# Create database engine with SQLite-specific settings
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# Create session factory for database connections
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base class for all database models
Base = declarative_base()

class User(Base):
    """User model for storing user account information"""
    __tablename__ = "users"
    
    # Primary key and unique identifier
    id = Column(Integer, primary_key=True, index=True)
    # User's email address (unique and indexed for fast lookups)
    email = Column(String, unique=True, index=True)
    # Hashed password (never store plain text passwords)
    hashed_password = Column(String)
    # Account status (can be used to disable accounts)
    is_active = Column(Boolean, default=True)
    # Account creation timestamp
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship: One user can track many products
    tracked_products = relationship("TrackedProduct", back_populates="user")

class TrackedProduct(Base):
    __tablename__ = "tracked_products"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_url = Column(String, index=True)
    product_name = Column(String)
    current_price = Column(Float)
    original_price = Column(Float)
    image_url = Column(String)
    seller = Column(String)
    platform = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="tracked_products")
    price_history = relationship("PriceHistory", back_populates="product")

class PriceHistory(Base):
    __tablename__ = "price_history"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("tracked_products.id"))
    price = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    product = relationship("TrackedProduct", back_populates="price_history")

class AlternativeProduct(Base):
    __tablename__ = "alternative_products"
    
    id = Column(Integer, primary_key=True, index=True)
    original_product_id = Column(Integer, ForeignKey("tracked_products.id"))
    name = Column(String)
    price = Column(Float)
    url = Column(String)
    platform = Column(String)
    image_url = Column(String)
    similarity_score = Column(Float)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)