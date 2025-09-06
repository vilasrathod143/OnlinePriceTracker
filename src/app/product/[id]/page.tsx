'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { 
  ArrowLeft, Package, TrendingUp, TrendingDown, ExternalLink, 
  Brain, ShoppingCart, AlertTriangle, Trash2 
} from 'lucide-react';
import { auth } from '@/lib/auth';
import { productsAPI } from '@/lib/api';
import { ProductDetails } from '@/types';

export default function ProductDetailsPage() {
  const [productDetails, setProductDetails] = useState<ProductDetails | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const router = useRouter();
  const params = useParams();
  const productId = parseInt(params.id as string);

  useEffect(() => {
    if (!auth.isAuthenticated()) {
      router.push('/auth/login');
      return;
    }

    loadProductDetails();
  }, [productId]);

  const loadProductDetails = async () => {
    try {
      const data = await productsAPI.getProductDetails(productId);
      setProductDetails(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load product details');
    } finally {
      setIsLoading(false);
    }
  };

  const handleStopTracking = async () => {
    if (confirm('Are you sure you want to stop tracking this product?')) {
      try {
        await productsAPI.stopTracking(productId);
        router.push('/dashboard');
      } catch (err) {
        alert('Failed to stop tracking');
      }
    }
  };

  const formatChartData = () => {
    if (!productDetails?.price_history) return [];
    
    return productDetails.price_history
      .slice()
      .reverse()
      .map((item, index) => ({
        date: new Date(item.timestamp).toLocaleDateString(),
        price: item.price,
        index
      }));
  };

  const getRecommendationColor = (recommendation: string) => {
    switch (recommendation) {
      case 'buy_now': return 'text-green-600 bg-green-100';
      case 'wait': return 'text-yellow-600 bg-yellow-100';
      case 'good_deal': return 'text-blue-600 bg-blue-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'increasing': return <TrendingUp className="h-5 w-5 text-red-500" />;
      case 'decreasing': return <TrendingDown className="h-5 w-5 text-green-500" />;
      default: return <div className="h-5 w-5 bg-gray-400 rounded-full" />;
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error || !productDetails) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <AlertTriangle className="h-16 w-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Product Not Found</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <Link href="/dashboard" className="btn-primary">
            Back to Dashboard
          </Link>
        </div>
      </div>
    );
  }

  const { product, price_history, ai_analysis, alternatives } = productDetails;
  const priceChange = product.current_price - product.original_price;
  const priceChangePercent = ((priceChange / product.original_price) * 100);

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center space-x-4">
            <button
              onClick={() => router.back()}
              className="p-2 hover:bg-gray-200 rounded-lg transition-colors"
            >
              <ArrowLeft className="h-5 w-5" />
            </button>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Product Details</h1>
              <p className="text-gray-600">Track pricing and get AI insights</p>
            </div>
          </div>
          <button
            onClick={handleStopTracking}
            className="flex items-center space-x-2 text-red-600 hover:text-red-700 px-4 py-2 border border-red-300 rounded-lg hover:bg-red-50 transition-colors"
          >
            <Trash2 className="h-4 w-4" />
            <span>Stop Tracking</span>
          </button>
        </div>

        {/* Product Overview */}
        <div className="card mb-8">
          <div className="flex flex-col lg:flex-row lg:items-start space-y-6 lg:space-y-0 lg:space-x-8">
            {/* Product Image */}
            <div className="w-full lg:w-1/3">
              <div className="aspect-square bg-gray-200 rounded-lg overflow-hidden">
                {product.image_url ? (
                  <img 
                    src={product.image_url} 
                    alt={product.product_name}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div className="w-full h-full flex items-center justify-center">
                    <Package className="h-24 w-24 text-gray-400" />
                  </div>
                )}
              </div>
            </div>

            {/* Product Info */}
            <div className="flex-1">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">{product.product_name}</h2>
              
              <div className="grid grid-cols-2 gap-4 mb-6">
                <div>
                  <p className="text-sm text-gray-600">Platform</p>
                  <p className="font-semibold">{product.platform}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Seller</p>
                  <p className="font-semibold">{product.seller}</p>
                </div>
              </div>

              {/* Price Info */}
              <div className="bg-gray-50 p-6 rounded-lg mb-6">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <p className="text-sm text-gray-600">Current Price</p>
                    <p className="text-3xl font-bold text-gray-900">₹{product.current_price}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Original Price</p>
                    <p className="text-xl font-semibold text-gray-600">₹{product.original_price}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Price Change</p>
                    <div className="flex items-center space-x-2">
                      {priceChange < 0 ? (
                        <TrendingDown className="h-5 w-5 text-green-500" />
                      ) : priceChange > 0 ? (
                        <TrendingUp className="h-5 w-5 text-red-500" />
                      ) : null}
                      <span className={`text-xl font-semibold ${
                        priceChange < 0 ? 'text-green-600' : 
                        priceChange > 0 ? 'text-red-600' : 'text-gray-600'
                      }`}>
                        {priceChange >= 0 ? '+' : ''}₹{priceChange.toFixed(2)} ({priceChangePercent.toFixed(1)}%)
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              <a
                href={product.product_url}
                target="_blank"
                rel="noopener noreferrer"
                className="btn-primary inline-flex items-center space-x-2"
              >
                <ExternalLink className="h-4 w-4" />
                <span>View on {product.platform}</span>
              </a>
            </div>
          </div>
        </div>

        {/* AI Analysis */}
        <div className="card mb-8">
          <div className="flex items-center space-x-2 mb-6">
            <Brain className="h-6 w-6 text-purple-600" />
            <h2 className="text-xl font-semibold">AI Analysis</h2>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Price Trend</span>
                <div className="flex items-center space-x-2">
                  {getTrendIcon(ai_analysis.trend)}
                  <span className="font-medium capitalize">{ai_analysis.trend}</span>
                </div>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-gray-600">Recommendation</span>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${getRecommendationColor(ai_analysis.recommendation)}`}>
                  {ai_analysis.recommendation.replace('_', ' ').toUpperCase()}
                </span>
              </div>

              <div>
                <span className="text-gray-600">Price Prediction</span>
                <p className="font-medium">{ai_analysis.price_prediction}</p>
              </div>
            </div>

            <div className="space-y-4">
              <div>
                <span className="text-gray-600">Best Time to Buy</span>
                <p className="font-medium">{ai_analysis.best_time_to_buy}</p>
              </div>

              <div>
                <span className="text-gray-600">AI Insights</span>
                <p className="text-sm text-gray-700 mt-1">{ai_analysis.insights}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Price History Chart */}
        <div className="card mb-8">
          <h2 className="text-xl font-semibold mb-6">Price History</h2>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={formatChartData()}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip 
                  formatter={(value) => [`₹${value}`, 'Price']}
                  labelFormatter={(label) => `Date: ${label}`}
                />
                <Line 
                  type="monotone" 
                  dataKey="price" 
                  stroke="#3b82f6" 
                  strokeWidth={2}
                  dot={{ fill: '#3b82f6', strokeWidth: 2, r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Alternative Products */}
        {alternatives.length > 0 && (
          <div className="card">
            <h2 className="text-xl font-semibold mb-6">Alternative Products</h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              {alternatives.map((alt) => (
                <a 
                  key={alt.id} 
                  href={alt.url !== '#' ? alt.url : undefined}
                  target={alt.url !== '#' ? '_blank' : undefined}
                  rel={alt.url !== '#' ? 'noopener noreferrer' : undefined}
                  className={`block border border-gray-200 rounded-lg p-4 transition-shadow ${
                    alt.url !== '#' ? 'hover:shadow-md cursor-pointer' : 'cursor-default'
                  }`}
                >
                  <div className="flex items-start space-x-3">
                    <div className="w-16 h-16 bg-gray-200 rounded-lg flex items-center justify-center overflow-hidden">
                      {alt.image_url ? (
                        <img 
                          src={alt.image_url} 
                          alt={alt.name} 
                          className="w-full h-full object-cover rounded-lg"
                          onError={(e) => {
                            e.currentTarget.style.display = 'none';
                            e.currentTarget.nextElementSibling?.classList.remove('hidden');
                          }}
                        />
                      ) : null}
                      <Package className={`h-8 w-8 text-gray-400 ${alt.image_url ? 'hidden' : ''}`} />
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="font-medium text-gray-900 line-clamp-2 mb-1">{alt.name}</h3>
                      <p className="text-sm text-gray-500 mb-2">{alt.platform}</p>
                      <p className="text-lg font-semibold text-primary-600 mb-2">
                        {alt.price > 0 ? `₹${alt.price.toFixed(2)}` : 'Price not available'}
                      </p>
                      <div className="flex items-center justify-between">
                        <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                          {Math.round(alt.similarity_score * 100)}% match
                        </span>
                        {alt.url !== '#' && (
                          <span className="text-xs text-primary-600 font-medium">
                            View Product →
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                </a>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}