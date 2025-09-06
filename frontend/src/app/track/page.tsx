'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { Link2, Package, AlertCircle, CheckCircle } from 'lucide-react';
import { auth } from '@/lib/auth';
import { productsAPI } from '@/lib/api';

interface TrackForm {
  url: string;
}

const PlatformLogo = ({ platform }: { platform: string }) => {
  switch (platform) {
    case 'Amazon':
      return (
        <svg className="w-8 h-8" viewBox="0 0 100 30" fill="#FF9900">
          <path d="M28.1 20.8c-5.5 4.1-13.5 6.3-20.4 6.3-9.6 0-18.3-3.6-24.9-9.5-.5-.5-.1-1.1.6-.7 7.1 4.1 15.9 6.6 25 6.6 6.1 0 12.9-1.3 19.1-3.9.9-.4 1.7.6.6 1.2z"/>
          <path d="M30.4 18.2c-.7-.9-4.6-.4-6.4-.2-.5.1-.6-.4-.1-.7 3.1-2.2 8.2-1.6 8.8-.8.6.8-.2 6.3-3.3 8.9-.5.4-.9.2-.7-.3.7-1.7 2.2-5.5 1.7-6.9z"/>
        </svg>
      );
    case 'Flipkart':
      return (
        <svg className="w-8 h-8" viewBox="0 0 24 24" fill="#047BD6">
          <rect width="24" height="24" rx="4" fill="#047BD6"/>
          <text x="12" y="16" textAnchor="middle" fill="white" fontSize="12" fontWeight="bold">F</text>
        </svg>
      );
    case 'Myntra':
      return (
        <svg className="w-8 h-8" viewBox="0 0 24 24" fill="#FF3F6C">
          <path d="M12 2L2 7v10c0 5.55 3.84 9.74 9 11 5.16-1.26 9-5.45 9-11V7l-10-5z"/>
          <text x="12" y="14" textAnchor="middle" fill="white" fontSize="8" fontWeight="bold">M</text>
        </svg>
      );
    default:
      return (
        <svg className="w-8 h-8" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
        </svg>
      );
  }
};

export default function TrackPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();

  const { register, handleSubmit, reset, formState: { errors } } = useForm<TrackForm>();

  useEffect(() => {
    if (!auth.isAuthenticated()) {
      router.push('/auth/login');
    }
  }, []);

  const onSubmit = async (data: TrackForm) => {
    setIsLoading(true);
    setError('');
    setSuccess(false);

    try {
      await productsAPI.trackProduct(data.url);
      setSuccess(true);
      reset();
      
      // Redirect to dashboard after 2 seconds
      setTimeout(() => {
        router.push('/dashboard');
      }, 2000);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to track product');
    } finally {
      setIsLoading(false);
    }
  };

  const supportedPlatforms = [
    { name: 'Amazon', color: 'bg-orange-100 text-orange-800' },
    { name: 'Flipkart', color: 'bg-blue-100 text-blue-800' },
    { name: 'Myntra', color: 'bg-pink-100 text-pink-800' },
    { name: 'Others', color: 'bg-gray-100 text-gray-800' },
  ];

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Track a New Product</h1>
          <p className="text-xl text-gray-600">
            Add any product URL and let our AI agent monitor prices for you
          </p>
        </div>

        {/* Supported Platforms */}
        <div className="card mb-8">
          <h2 className="text-lg font-semibold mb-4">Supported Platforms</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {supportedPlatforms.map((platform) => (
              <div key={platform.name} className={`p-3 rounded-lg text-center ${platform.color}`}>
                <div className="mb-2 flex justify-center">
                  <PlatformLogo platform={platform.name} />
                </div>
                <div className="font-medium">{platform.name}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Track Form */}
        <div className="card">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-center space-x-2">
                <AlertCircle className="h-5 w-5" />
                <span>{error}</span>
              </div>
            )}

            {success && (
              <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg flex items-center space-x-2">
                <CheckCircle className="h-5 w-5" />
                <span>Product added successfully! Redirecting to dashboard...</span>
              </div>
            )}

            <div>
              <label htmlFor="url" className="block text-sm font-medium text-gray-700 mb-2">
                Product URL
              </label>
              <div className="relative">
                <Link2 className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                <input
                  {...register('url', {
                    required: 'Product URL is required',
                    pattern: {
                      value: /^https?:\/\/.+/,
                      message: 'Please enter a valid URL starting with http:// or https://'
                    }
                  })}
                  type="url"
                  className="input-field pl-10"
                  placeholder="https://www.amazon.in/product-name/dp/..."
                  disabled={isLoading}
                />
              </div>
              {errors.url && (
                <p className="mt-1 text-sm text-red-600">{errors.url.message}</p>
              )}
              <p className="mt-2 text-sm text-gray-500">
                Copy and paste the product URL from any supported e-commerce platform
              </p>
            </div>

            <button
              type="submit"
              disabled={isLoading || success}
              className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
            >
              {isLoading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  <span>Analyzing Product...</span>
                </>
              ) : (
                <>
                  <Package className="h-4 w-4" />
                  <span>Start Tracking</span>
                </>
              )}
            </button>
          </form>
        </div>

        {/* How it works */}
        <div className="mt-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">How It Works</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-primary-600">1</span>
              </div>
              <h3 className="text-lg font-semibold mb-2">Paste URL</h3>
              <p className="text-gray-600">
                Simply paste the product URL from any supported platform
              </p>
            </div>

            <div className="text-center">
              <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-primary-600">2</span>
              </div>
              <h3 className="text-lg font-semibold mb-2">AI Analysis</h3>
              <p className="text-gray-600">
                Our AI agent extracts product details and starts monitoring
              </p>
            </div>

            <div className="text-center">
              <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-primary-600">3</span>
              </div>
              <h3 className="text-lg font-semibold mb-2">Get Alerts</h3>
              <p className="text-gray-600">
                Receive email notifications when prices drop or change
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}