// Import HTTP client library
import axios from 'axios';
// Import cookie management library
import Cookies from 'js-cookie';
// Import TypeScript type definitions
import { TrackedProduct, ProductDetails, DashboardInsights } from '@/types';

// Backend API base URL
const API_BASE_URL = 'http://localhost:8000';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: API_BASE_URL,
});

// Interceptor to automatically add authentication token to all requests
api.interceptors.request.use((config) => {
  // Get JWT token from cookies
  const token = Cookies.get('token');
  if (token) {
    // Add Bearer token to Authorization header
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Authentication API endpoints
export const authAPI = {
  // User registration endpoint
  register: async (email: string, password: string) => {
    const response = await api.post('/auth/register', { email, password });
    return response.data;
  },
  
  // User login endpoint
  login: async (email: string, password: string) => {
    const response = await api.post('/auth/login', { email, password });
    return response.data;
  },
};

// Product tracking API endpoints
export const productsAPI = {
  // Start tracking a new product by URL
  trackProduct: async (url: string) => {
    const response = await api.post('/products/track', { url });
    return response.data;
  },
  
  // Get all products tracked by current user
  getMyProducts: async (): Promise<TrackedProduct[]> => {
    const response = await api.get('/products/my-products');
    return response.data;
  },
  
  // Get detailed information about a specific product
  getProductDetails: async (productId: number): Promise<ProductDetails> => {
    const response = await api.get(`/products/${productId}`);
    return response.data;
  },
  
  // Stop tracking a product
  stopTracking: async (productId: number) => {
    const response = await api.delete(`/products/${productId}`);
    return response.data;
  },
};

// Dashboard API
export const dashboardAPI = {
  getInsights: async (): Promise<DashboardInsights> => {
    const response = await api.get('/dashboard/insights');
    return response.data;
  },
};

export default api;