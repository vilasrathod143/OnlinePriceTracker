# 🛒 Price Tracker Agent - AI-Powered Smart Shopping Platform

A comprehensive price tracking system that monitors product prices across multiple e-commerce platforms (Amazon, Flipkart, Myntra, etc.) with intelligent AI analysis, price predictions, and automated email alerts.

## 🌟 Features

### 🤖 AI-Powered Intelligence
- **Gemini AI Integration**: Advanced price analysis and trend predictions
- **Smart Recommendations**: Personalized buying suggestions based on price patterns
- **Alternative Product Discovery**: AI suggests similar products across platforms
- **Price Prediction**: Machine learning-based future price forecasting

### 📊 Comprehensive Price Tracking
- **Multi-Platform Support**: Amazon, Flipkart, Myntra, and more
- **Real-time Monitoring**: Automated price checking every 6 hours
- **Price History Visualization**: Interactive charts showing price trends
- **Instant Alerts**: Beautiful HTML email notifications for price changes

### 🎨 Modern User Interface
- **Responsive Design**: Clean, modern UI built with Next.js and Tailwind CSS
- **Dashboard Analytics**: Comprehensive overview of savings and tracked products
- **Interactive Charts**: Visual price history with Recharts
- **Mobile-First**: Optimized for all device sizes

### 🔐 Security & Authentication
- **JWT Authentication**: Secure token-based user authentication
- **Password Encryption**: Bcrypt hashing for secure password storage
- **API Security**: Protected endpoints with bearer token validation
- **Data Privacy**: Encrypted user data and secure API communications

## 🏗️ Architecture

### Backend (FastAPI + Python)
```
backend/
├── main.py              # FastAPI application entry point
├── database.py          # SQLAlchemy models and database configuration
├── auth.py              # JWT authentication and security
├── scraper.py           # Web scraping for multiple e-commerce platforms
├── agent.py             # Gemini AI integration for intelligent analysis
├── email_service.py     # Professional HTML email notifications
├── requirements.txt     # Python dependencies
└── .env                 # Environment configuration
```

### Frontend (Next.js + TypeScript)
```
frontend/
├── src/
│   ├── app/             # Next.js 14 App Router pages
│   │   ├── page.tsx     # Homepage with modern design
│   │   ├── auth/        # Login and registration pages
│   │   ├── dashboard/   # User dashboard with analytics
│   │   ├── track/       # Product tracking interface
│   │   ├── product/     # Detailed product analysis pages
│   │   ├── profile/     # User profile and settings
│   │   └── about/       # About page
│   ├── components/      # Reusable React components
│   ├── lib/            # API client and utilities
│   └── types/          # TypeScript type definitions
├── package.json
└── tailwind.config.js
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- Chrome/Chromium browser (for web scraping)

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Edit .env file with your credentials
   SECRET_KEY=your-secret-key-here
   GEMINI_API_KEY=your-gemini-api-key
   SMTP_USERNAME=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   ```

5. **Run the backend server**
   ```bash
   python main.py
   ```
   Backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run the development server**
   ```bash
   npm run dev
   ```
   Frontend will be available at `http://localhost:3000`

## 📋 API Documentation

### Authentication Endpoints
- `POST /auth/register` - User registration
- `POST /auth/login` - User login

### Product Tracking Endpoints
- `POST /products/track` - Start tracking a product
- `GET /products/my-products` - Get user's tracked products
- `GET /products/{product_id}` - Get detailed product information
- `DELETE /products/{product_id}` - Stop tracking a product

### Dashboard Endpoints
- `GET /dashboard/insights` - Get AI-powered dashboard insights

## 🤖 AI Agent Capabilities

### Price Analysis
- **Trend Detection**: Identifies increasing, decreasing, or stable price patterns
- **Recommendation Engine**: Suggests optimal buying times (buy_now, wait, good_deal)
- **Price Predictions**: Forecasts future price ranges based on historical data

### Smart Alternatives
- **Cross-Platform Discovery**: Finds similar products on different platforms
- **Brand Alternatives**: Suggests comparable products from different brands
- **Price Comparison**: Compares alternatives with similarity scoring

### Personalized Insights
- **Shopping Pattern Analysis**: Understands user preferences and behavior
- **Budget Optimization**: Provides spending insights and recommendations
- **Seasonal Advice**: Suggests best times to buy based on seasonal trends

## 📧 Email Notifications

### Professional HTML Templates
- **Price Drop Alerts**: Beautiful notifications when prices decrease
- **Price Increase Warnings**: Alerts for significant price increases
- **Welcome Emails**: Onboarding emails for new users
- **Weekly Summaries**: Comprehensive reports of tracked products

### Email Features
- **Responsive Design**: Mobile-optimized email templates
- **Rich Content**: Product images, price charts, and call-to-action buttons
- **Personalization**: AI-generated personalized content
- **Urgency Indicators**: Smart urgency levels based on price changes

## 🛡️ Security Features

### Authentication Security
- **JWT Tokens**: Secure, stateless authentication
- **Password Hashing**: Bcrypt encryption for user passwords
- **Token Expiration**: Configurable token lifetime
- **Secure Headers**: CORS and security middleware

### Data Protection
- **Input Validation**: Comprehensive request validation
- **SQL Injection Prevention**: SQLAlchemy ORM protection
- **Rate Limiting**: API endpoint protection
- **Environment Variables**: Secure configuration management

## 🎨 UI/UX Features

### Modern Design
- **Gradient Backgrounds**: Beautiful color gradients
- **Glass Morphism**: Modern glass effect components
- **Smooth Animations**: CSS transitions and animations
- **Responsive Layout**: Mobile-first design approach

### User Experience
- **Intuitive Navigation**: Clear, accessible navigation
- **Loading States**: Smooth loading indicators
- **Error Handling**: User-friendly error messages
- **Form Validation**: Real-time form validation

## 📊 Supported Platforms

### E-commerce Platforms
- **Amazon**: Full product scraping and price tracking
- **Flipkart**: Complete integration with product details
- **Myntra**: Fashion and lifestyle product tracking
- **Generic Sites**: Fallback scraper for other platforms

### Platform Features
- **Auto-Detection**: Automatic platform identification from URLs
- **Product Extraction**: Name, price, image, and seller information
- **Price History**: Historical price data storage and analysis
- **Alternative Discovery**: Cross-platform product suggestions

## 🔧 Configuration

### Environment Variables
```env
# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=sqlite:///./price_tracker.db

# AI Integration
GEMINI_API_KEY=your-gemini-api-key-here

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### Customization Options
- **Scraping Intervals**: Configurable price checking frequency
- **Email Templates**: Customizable HTML email designs
- **AI Prompts**: Adjustable AI analysis parameters
- **Platform Support**: Easy addition of new e-commerce platforms

## 🚀 Deployment

### Backend Deployment
```bash
# Production server
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Docker deployment
docker build -t price-tracker-backend .
docker run -p 8000:8000 price-tracker-backend
```

### Frontend Deployment
```bash
# Build for production
npm run build

# Start production server
npm start

# Deploy to Vercel
vercel deploy
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** for intelligent price analysis
- **FastAPI** for the robust backend framework
- **Next.js** for the modern frontend framework
- **Tailwind CSS** for beautiful, responsive design
- **Recharts** for interactive data visualization

## 📞 Support

For support, email support@pricetracker.com or join our Discord community.

---

**Built with ❤️ for smart shoppers everywhere**