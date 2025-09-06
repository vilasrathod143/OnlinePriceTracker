import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import Navbar from '@/components/Navbar';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Price Tracker Agent - Smart Shopping Assistant',
  description: 'Track prices across multiple e-commerce platforms with AI-powered insights and alerts',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Navbar />
        <main className="min-h-screen">
          {children}
        </main>
        <footer className="bg-gray-900 text-white py-8">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center">
              <p>&copy; 2024 Price Tracker Agent. All rights reserved.</p>
              <p className="text-gray-400 mt-2">Smart shopping with AI-powered insights</p>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}