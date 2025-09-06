import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os
from dotenv import load_dotenv
import requests
from typing import Dict

load_dotenv()

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.username = os.getenv("SMTP_USERNAME")
        self.password = os.getenv("SMTP_PASSWORD")
    
    def create_price_alert_html(self, product_data: Dict, alert_content: Dict) -> str:
        """Create professional HTML email template"""
        
        price_change = product_data['new_price'] - product_data['old_price']
        change_percentage = (price_change / product_data['old_price']) * 100
        is_decrease = price_change < 0
        
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Price Alert</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: white; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }}
                .content {{ padding: 30px; }}
                .product-card {{ border: 1px solid #e0e0e0; border-radius: 10px; padding: 20px; margin: 20px 0; }}
                .price-section {{ display: flex; justify-content: space-between; align-items: center; margin: 20px 0; }}
                .price {{ font-size: 24px; font-weight: bold; }}
                .old-price {{ text-decoration: line-through; color: #888; }}
                .new-price {{ color: {'#27ae60' if is_decrease else '#e74c3c'}; }}
                .change {{ padding: 5px 10px; border-radius: 5px; color: white; background-color: {'#27ae60' if is_decrease else '#e74c3c'}; }}
                .cta-button {{ display: inline-block; padding: 15px 30px; background-color: #3498db; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ background-color: #34495e; color: white; padding: 20px; text-align: center; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔔 Price Alert</h1>
                    <p>{alert_content.get('greeting', 'Hello!')}</p>
                </div>
                
                <div class="content">
                    <div class="product-card">
                        <h2>{product_data['name']}</h2>
                        <p><strong>Platform:</strong> {product_data['platform']}</p>
                        
                        <div class="price-section">
                            <div>
                                <div class="price old-price">₹{product_data['old_price']}</div>
                                <div class="price new-price">₹{product_data['new_price']}</div>
                            </div>
                            <div class="change">
                                {'+' if change_percentage > 0 else ''}{change_percentage:.1f}%
                            </div>
                        </div>
                        
                        <p>{alert_content.get('main_message', '')}</p>
                        
                        <a href="{product_data['url']}" class="cta-button">
                            {alert_content.get('call_to_action', 'View Product')}
                        </a>
                    </div>
                    
                    <div style="background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <h3>💡 AI Insights</h3>
                        <p>This price change represents a <strong>{'great opportunity' if is_decrease else 'price increase'}</strong>. 
                        {'Consider purchasing now!' if is_decrease else 'You might want to wait for a better deal.'}</p>
                    </div>
                </div>
                
                <div class="footer">
                    <p>Happy Shopping! 🛒</p>
                    <p>Price Tracker Agent - Your Smart Shopping Assistant</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_template
    
    def send_price_alert(self, to_email: str, product_data: Dict, alert_content: Dict) -> bool:
        """Send price alert email"""
        
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.username
            msg['To'] = to_email
            msg['Subject'] = alert_content.get('subject', f"Price Alert: {product_data['name']}")
            
            # Create HTML content
            html_content = self.create_price_alert_html(product_data, alert_content)
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def send_welcome_email(self, to_email: str, user_name: str) -> bool:
        """Send welcome email to new users"""
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: white; border-radius: 10px; overflow: hidden; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; text-align: center; }}
                .content {{ padding: 30px; }}
                .feature {{ margin: 20px 0; padding: 15px; background-color: #f8f9fa; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 Welcome to Price Tracker Agent!</h1>
                    <p>Hello {user_name}!</p>
                </div>
                <div class="content">
                    <p>Thank you for joining our smart price tracking platform. Here's what you can do:</p>
                    
                    <div class="feature">
                        <h3>📊 Smart Price Tracking</h3>
                        <p>Track prices from Amazon, Flipkart, Myntra and more!</p>
                    </div>
                    
                    <div class="feature">
                        <h3>🤖 AI-Powered Insights</h3>
                        <p>Get intelligent recommendations and price predictions</p>
                    </div>
                    
                    <div class="feature">
                        <h3>📧 Instant Alerts</h3>
                        <p>Receive email notifications when prices drop</p>
                    </div>
                    
                    <p>Start tracking your first product today!</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = to_email
            msg['Subject'] = "Welcome to Price Tracker Agent! 🎉"
            
            msg.attach(MIMEText(html_content, 'html'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            print(f"Error sending welcome email: {e}")
            return False