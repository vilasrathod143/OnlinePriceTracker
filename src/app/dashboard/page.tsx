'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { TrendingUp, TrendingDown, Package, DollarSign, Plus, Eye } from 'lucide-react';
import { auth } from '@/lib/auth';
import { dashboardAPI, productsAPI } from '@/lib/api';
import { TrackedProduct, DashboardInsights } from '@/types';

export default function DashboardPage() {
  const [products, setProducts] = useState<TrackedProduct[]>([]);
  const [insights, setInsights] = useState<DashboardInsights | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    if (!auth.isAuthenticated()) {
      router.push('/auth/login');
      return;
    }

    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const [productsData, insightsData] = await Promise.all([
        productsAPI.getMyProducts(),
        dashboardAPI.getInsights()
      ]);
      
      setProducts(productsData);
      setInsights(insightsData);
    } catch (error) {
      console.error('Error loading dashboard:', error);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-2">Track your products and savings</p>
        </div>

        {/* Stats Cards */}
        {insights && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="card">
              <div className="flex items-center">
                <div className="bg-blue-100 p-3 rounded-full">
                  <Package className="h-6 w-6 text-blue-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm text-gray-600">Tracked Products</p>
                  <p className="text-2xl font-bold text-gray-900">{insights.total_products}</p>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center">
                <div className="bg-green-100 p-3 rounded-full">
                  <DollarSign className="h-6 w-6 text-green-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm text-gray-600">Total Savings</p>
                  <p className="text-2xl font-bold text-green-600">₹{(insights.total_savings || 0).toFixed(2)}</p>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center">
                <div className="bg-purple-100 p-3 rounded-full">
                  <TrendingUp className="h-6 w-6 text-purple-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm text-gray-600">Active Alerts</p>
                  <p className="text-2xl font-bold text-gray-900">{products.length}</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* AI Insights */}
        {insights?.ai_suggestions && (
          <div className="card mb-8">
            <h2 className="text-xl font-semibold mb-4">🤖 AI Insights</h2>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="bg-blue-50 p-4 rounded-lg">
                <h3 className="font-medium text-blue-900 mb-2">Tracking Optimization</h3>
                <p className="text-blue-800 text-sm">{insights.ai_suggestions.tracking_optimization}</p>
              </div>
              <div className="bg-green-50 p-4 rounded-lg">
                <h3 className="font-medium text-green-900 mb-2">Budget Insights</h3>
                <p className="text-green-800 text-sm">{insights.ai_suggestions.budget_insights}</p>
              </div>
              <div className="bg-yellow-50 p-4 rounded-lg">
                <h3 className="font-medium text-yellow-900 mb-2">Seasonal Advice</h3>
                <p className="text-yellow-800 text-sm">{insights.ai_suggestions.seasonal_advice}</p>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg">
                <h3 className="font-medium text-purple-900 mb-2">Diversification Tips</h3>
                <p className="text-purple-800 text-sm">{insights.ai_suggestions.diversification_tips}</p>
              </div>
            </div>
          </div>
        )}

        {/* Products Section */}
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Your Tracked Products</h2>
          <Link href="/track" className="btn-primary flex items-center space-x-2">
            <Plus className="h-4 w-4" />
            <span>Track New Product</span>
          </Link>
        </div>

        {products.length === 0 ? (
          <div className="card text-center py-12">
            <Package className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">No Products Tracked Yet</h3>
            <p className="text-gray-600 mb-6">Start tracking your first product to see price trends and get alerts</p>
            <Link href="/track" className="btn-primary">
              Track Your First Product
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {products.map((product) => (
              <div key={product.id} className="card hover:shadow-lg transition-shadow">
                <div className="flex items-start space-x-4">
                  <div className="w-16 h-16 bg-gray-200 rounded-lg flex items-center justify-center overflow-hidden">
                    {product.image_url ? (
                      <img 
                        src={product.image_url} 
                        alt={product.product_name}
                        className="w-full h-full object-cover"
                      />
                    ) : (
                      <Package className="h-8 w-8 text-gray-400" />
                    )}
                  </div>
                  <div className="flex-1 min-w-0">
                    <h3 className="font-medium text-gray-900 truncate" title={product.product_name}>
                      {product.product_name}
                    </h3>
                    <p className="text-sm text-gray-500">{product.platform}</p>
                    <div className="mt-2">
                      <div className="flex items-center space-x-2">
                        <span className="text-lg font-bold text-gray-900">
                          ₹{product.current_price}
                        </span>
                        {product.current_price < product.original_price ? (
                          <div className="flex items-center text-green-600">
                            <TrendingDown className="h-4 w-4" />
                            <span className="text-sm">
                              ₹{(product.original_price - product.current_price).toFixed(2)} saved
                            </span>
                          </div>
                        ) : product.current_price > product.original_price ? (
                          <div className="flex items-center text-red-600">
                            <TrendingUp className="h-4 w-4" />
                            <span className="text-sm">
                              ₹{(product.current_price - product.original_price).toFixed(2)} increase
                            </span>
                          </div>
                        ) : null}
                      </div>
                    </div>
                  </div>
                </div>
                <div className="mt-4 flex justify-between items-center">
                  <span className="text-xs text-gray-500">
                    Added {new Date(product.created_at).toLocaleDateString()}
                  </span>
                  <Link 
                    href={`/product/${product.id}`}
                    className="flex items-center space-x-1 text-primary-600 hover:text-primary-700 text-sm"
                  >
                    <Eye className="h-4 w-4" />
                    <span>View Details</span>
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}