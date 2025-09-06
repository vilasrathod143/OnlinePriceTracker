import { Brain, Shield, Zap, Users, TrendingUp, Bell } from 'lucide-react';

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="gradient-bg text-white py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-5xl font-bold mb-6">About Price Tracker Agent</h1>
          <p className="text-xl text-gray-200 leading-relaxed">
            We're revolutionizing online shopping with AI-powered price tracking that saves you time and money. 
            Our intelligent agent monitors prices across multiple platforms and provides personalized insights 
            to help you make smarter purchasing decisions.
          </p>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-20 bg-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-6">Our Mission</h2>
            <p className="text-xl text-gray-600 leading-relaxed">
              To democratize smart shopping by making AI-powered price intelligence accessible to everyone. 
              We believe that every consumer deserves to get the best deals without spending hours comparing prices manually.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Brain className="h-8 w-8 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold mb-3">AI-First Approach</h3>
              <p className="text-gray-600">
                Leveraging cutting-edge artificial intelligence to provide intelligent insights and predictions
              </p>
            </div>

            <div className="text-center">
              <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Users className="h-8 w-8 text-green-600" />
              </div>
              <h3 className="text-xl font-semibold mb-3">User-Centric Design</h3>
              <p className="text-gray-600">
                Building intuitive experiences that make price tracking effortless for users of all technical levels
              </p>
            </div>

            <div className="text-center">
              <div className="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Shield className="h-8 w-8 text-purple-600" />
              </div>
              <h3 className="text-xl font-semibold mb-3">Privacy & Security</h3>
              <p className="text-gray-600">
                Protecting user data with enterprise-grade security while maintaining complete transparency
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Technology Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-6">Powered by Advanced Technology</h2>
            <p className="text-xl text-gray-600">
              Our platform combines multiple cutting-edge technologies to deliver superior price tracking
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="card text-center">
              <div className="bg-indigo-100 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4">
                <Brain className="h-6 w-6 text-indigo-600" />
              </div>
              <h3 className="text-lg font-semibold mb-3">Gemini AI Integration</h3>
              <p className="text-gray-600 text-sm">
                Google's advanced Gemini AI provides intelligent price analysis, trend predictions, and personalized recommendations
              </p>
            </div>

            <div className="card text-center">
              <div className="bg-blue-100 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4">
                <Zap className="h-6 w-6 text-blue-600" />
              </div>
              <h3 className="text-lg font-semibold mb-3">Real-time Scraping</h3>
              <p className="text-gray-600 text-sm">
                Advanced web scraping technology monitors prices across multiple e-commerce platforms in real-time
              </p>
            </div>

            <div className="card text-center">
              <div className="bg-green-100 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4">
                <Bell className="h-6 w-6 text-green-600" />
              </div>
              <h3 className="text-lg font-semibold mb-3">Smart Notifications</h3>
              <p className="text-gray-600 text-sm">
                Intelligent alert system sends personalized notifications with beautiful HTML emails when prices drop
              </p>
            </div>

            <div className="card text-center">
              <div className="bg-yellow-100 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4">
                <TrendingUp className="h-6 w-6 text-yellow-600" />
              </div>
              <h3 className="text-lg font-semibold mb-3">Predictive Analytics</h3>
              <p className="text-gray-600 text-sm">
                Machine learning algorithms analyze historical data to predict future price movements and optimal buying times
              </p>
            </div>

            <div className="card text-center">
              <div className="bg-red-100 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4">
                <Shield className="h-6 w-6 text-red-600" />
              </div>
              <h3 className="text-lg font-semibold mb-3">Secure Architecture</h3>
              <p className="text-gray-600 text-sm">
                Built with FastAPI backend, JWT authentication, and encrypted data storage for maximum security
              </p>
            </div>

            <div className="card text-center">
              <div className="bg-purple-100 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4">
                <Users className="h-6 w-6 text-purple-600" />
              </div>
              <h3 className="text-lg font-semibold mb-3">Modern Frontend</h3>
              <p className="text-gray-600 text-sm">
                Responsive Next.js interface with Tailwind CSS provides a seamless user experience across all devices
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Features Deep Dive */}
      <section className="py-20 bg-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-6">What Makes Us Different</h2>
          </div>

          <div className="space-y-16">
            <div className="flex flex-col lg:flex-row items-center space-y-8 lg:space-y-0 lg:space-x-12">
              <div className="lg:w-1/2">
                <h3 className="text-2xl font-bold text-gray-900 mb-4">Intelligent Price Analysis</h3>
                <p className="text-gray-600 mb-6">
                  Our AI agent doesn't just track prices—it understands them. Using advanced machine learning, 
                  we analyze price patterns, seasonal trends, and market dynamics to provide actionable insights 
                  that help you make informed purchasing decisions.
                </p>
                <ul className="space-y-2 text-gray-600">
                  <li className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-primary-600 rounded-full"></div>
                    <span>Trend analysis and price predictions</span>
                  </li>
                  <li className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-primary-600 rounded-full"></div>
                    <span>Optimal buying time recommendations</span>
                  </li>
                  <li className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-primary-600 rounded-full"></div>
                    <span>Personalized deal alerts</span>
                  </li>
                </ul>
              </div>
              <div className="lg:w-1/2">
                <div className="bg-gradient-to-br from-blue-50 to-purple-50 p-8 rounded-2xl">
                  <div className="text-center">
                    <Brain className="h-16 w-16 text-primary-600 mx-auto mb-4" />
                    <h4 className="text-lg font-semibold text-gray-900 mb-2">AI-Powered Insights</h4>
                    <p className="text-gray-600 text-sm">
                      Get intelligent recommendations based on your shopping patterns and market analysis
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <div className="flex flex-col lg:flex-row-reverse items-center space-y-8 lg:space-y-0 lg:space-x-12 lg:space-x-reverse">
              <div className="lg:w-1/2">
                <h3 className="text-2xl font-bold text-gray-900 mb-4">Multi-Platform Coverage</h3>
                <p className="text-gray-600 mb-6">
                  Track products across all major e-commerce platforms including Amazon, Flipkart, Myntra, and more. 
                  Our intelligent scraping technology adapts to different website structures and provides consistent, 
                  reliable price monitoring across the entire ecosystem.
                </p>
                <ul className="space-y-2 text-gray-600">
                  <li className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-green-600 rounded-full"></div>
                    <span>Support for 10+ major platforms</span>
                  </li>
                  <li className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-green-600 rounded-full"></div>
                    <span>Automatic platform detection</span>
                  </li>
                  <li className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-green-600 rounded-full"></div>
                    <span>Cross-platform price comparison</span>
                  </li>
                </ul>
              </div>
              <div className="lg:w-1/2">
                <div className="bg-gradient-to-br from-green-50 to-blue-50 p-8 rounded-2xl">
                  <div className="text-center">
                    <TrendingUp className="h-16 w-16 text-green-600 mx-auto mb-4" />
                    <h4 className="text-lg font-semibold text-gray-900 mb-2">Universal Tracking</h4>
                    <p className="text-gray-600 text-sm">
                      Monitor prices across all your favorite shopping platforms from one dashboard
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold text-gray-900 mb-6">Built for Smart Shoppers</h2>
          <p className="text-xl text-gray-600 mb-12">
            Price Tracker Agent is designed by developers who understand the frustration of missing great deals. 
            We've combined our expertise in AI, web scraping, and user experience design to create a platform 
            that truly serves the modern consumer.
          </p>

          <div className="bg-white p-8 rounded-2xl shadow-sm">
            <h3 className="text-2xl font-semibold text-gray-900 mb-4">Our Commitment</h3>
            <p className="text-gray-600 leading-relaxed">
              We're committed to continuously improving our platform based on user feedback and advancing AI technology. 
              Our goal is to make smart shopping accessible to everyone, regardless of their technical expertise or 
              the time they have available for price comparison.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}