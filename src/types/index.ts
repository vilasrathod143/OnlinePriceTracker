export interface User {
  id: number;
  email: string;
  created_at: string;
}

export interface TrackedProduct {
  id: number;
  product_name: string;
  current_price: number;
  original_price: number;
  image_url?: string;
  seller: string;
  platform: string;
  product_url: string;
  created_at: string;
}

export interface PriceHistory {
  id: number;
  price: number;
  timestamp: string;
}

export interface AlternativeProduct {
  id: number;
  name: string;
  price: number;
  url: string;
  platform: string;
  image_url?: string;
  similarity_score: number;
}

export interface AIAnalysis {
  trend: 'increasing' | 'decreasing' | 'stable';
  recommendation: 'buy_now' | 'wait' | 'good_deal' | 'monitor';
  price_prediction: string;
  best_time_to_buy: string;
  insights: string;
}

export interface ProductDetails {
  product: TrackedProduct;
  price_history: PriceHistory[];
  ai_analysis: AIAnalysis;
  alternatives: AlternativeProduct[];
}

export interface DashboardInsights {
  total_products: number;
  total_savings: number;
  ai_suggestions: {
    tracking_optimization: string;
    budget_insights: string;
    seasonal_advice: string;
    diversification_tips: string;
  };
  recent_products: TrackedProduct[];
}