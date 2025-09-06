# Import required libraries for AI functionality
import google.generativeai as genai  # Google's Gemini AI library
import os  # For environment variables
from typing import List, Dict  # Type hints for better code clarity
import json  # For JSON parsing
from dotenv import load_dotenv  # Load environment variables from .env file

# Load environment variables (API keys, etc.)
load_dotenv()

class PriceTrackerAgent:
    """AI Agent for intelligent price analysis and recommendations"""
    
    def __init__(self):
        """Initialize the AI agent with Gemini API"""
        # Configure Gemini AI with API key from environment
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        # Initialize the Gemini model for text generation
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def analyze_product(self, product_name: str, current_price: float, price_history: List[Dict]) -> Dict:
        """Analyze product pricing trends and provide AI-powered insights"""
        
        # Convert price history to simplified format for AI analysis
        price_data = [{"price": p["price"], "date": p["timestamp"]} for p in price_history]
        
        # Create detailed prompt for AI analysis
        prompt = f"""
        As a price tracking AI agent, analyze this product:
        
        Product: {product_name}
        Current Price: ₹{current_price}
        Price History: {json.dumps(price_data, default=str)}
        
        Provide analysis in JSON format:
        {{
            "trend": "increasing/decreasing/stable",
            "recommendation": "buy_now/wait/good_deal",
            "price_prediction": "predicted_price_range",
            "best_time_to_buy": "timing_recommendation",
            "insights": "detailed_analysis"
        }}
        """
        
        try:
            # Send prompt to Gemini AI and get response
            response = self.model.generate_content(prompt)
            # Parse AI response as JSON
            return json.loads(response.text)
        except:
            # Fallback response if AI fails
            return {
                "trend": "stable",
                "recommendation": "monitor",
                "price_prediction": f"₹{current_price * 0.9} - ₹{current_price * 1.1}",
                "best_time_to_buy": "Current price seems reasonable",
                "insights": "Unable to analyze due to limited data"
            }
    
    def find_alternatives(self, product_name: str, current_price: float, platform: str) -> List[Dict]:
        """Find alternative products using AI across different platforms"""
        
        # Create prompt asking AI to suggest alternative products
        prompt = f"""
        Find 6 alternative products for:
        Product: {product_name}
        Current Price: ₹{current_price}
        Platform: {platform}
        
        Suggest alternatives from different platforms. Return as JSON array:
        [
            {{
                "name": "product_name",
                "estimated_price": 2500,
                "platform": "Amazon",
                "reason": "why_this_is_alternative",
                "search_keywords": "keywords_to_search"
            }}
        ]
        """
        
        try:
            # Get AI-generated alternatives
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except:
            # Fallback: Generate alternatives programmatically if AI fails
            platforms = ["Amazon", "Flipkart", "Myntra", "Snapdeal", "Nykaa", "Ajio"]
            alternatives = []
            # Create alternatives for each platform (except current one)
            for i, plat in enumerate(platforms):
                if plat != platform:  # Skip the current platform
                    # Vary price slightly for each alternative
                    price_var = current_price * (0.8 + (i * 0.1))
                    alternatives.append({
                        "name": f"Similar {product_name.split()[0]} from {plat}",
                        "estimated_price": round(price_var, 2),
                        "platform": plat,
                        "reason": f"Alternative from {plat}",
                        "search_keywords": product_name.split()[:2]  # First 2 words as keywords
                    })
            return alternatives[:5]  # Return only first 5 alternatives
    
    def generate_price_alert_content(self, product_name: str, old_price: float, new_price: float, product_url: str) -> Dict:
        """Generate personalized price alert email content using AI"""
        
        # Calculate price change percentage
        price_change = ((new_price - old_price) / old_price) * 100
        # Determine if price increased or decreased
        change_type = "decreased" if new_price < old_price else "increased"
        
        # Create prompt for AI to generate email content
        prompt = f"""
        Generate a professional price alert email for:
        Product: {product_name}
        Old Price: ₹{old_price}
        New Price: ₹{new_price}
        Price Change: {price_change:.1f}% {change_type}
        
        Create engaging email content in JSON:
        {{
            "subject": "email_subject",
            "greeting": "personalized_greeting",
            "main_message": "price_change_announcement",
            "call_to_action": "what_user_should_do",
            "urgency_level": "low/medium/high"
        }}
        """
        
        try:
            # Get AI-generated email content
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except:
            # Fallback email content if AI fails
            return {
                "subject": f"Price Alert: {product_name}",
                "greeting": "Hello!",
                "main_message": f"The price of {product_name} has {change_type} from ₹{old_price} to ₹{new_price}",
                "call_to_action": "Check it out now!" if change_type == "decreased" else "Keep monitoring",
                "urgency_level": "medium" if change_type == "decreased" else "low"
            }
    
    def smart_tracking_suggestions(self, user_products: List[Dict]) -> Dict:
        """Provide AI-powered smart suggestions for better price tracking"""
        
        # Extract essential product info for AI analysis
        products_info = [{"name": p["name"], "price": p["price"], "platform": p["platform"]} for p in user_products]
        
        # Create prompt asking AI to analyze user's shopping patterns
        prompt = f"""
        Analyze user's tracked products and provide smart suggestions:
        Products: {json.dumps(products_info)}
        
        Provide suggestions in JSON:
        {{
            "tracking_optimization": "how_to_improve_tracking",
            "budget_insights": "spending_pattern_analysis",
            "seasonal_advice": "best_times_to_buy_these_categories",
            "diversification_tips": "platform_and_category_suggestions"
        }}
        """
        
        try:
            # Get AI-generated personalized suggestions
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except:
            # Fallback suggestions if AI fails
            return {
                "tracking_optimization": "Consider tracking products from multiple platforms",
                "budget_insights": "Your tracked products show diverse price ranges",
                "seasonal_advice": "Monitor for seasonal sales and festivals",
                "diversification_tips": "Try exploring different product categories"
            }