import React from 'react';
import { Link } from 'react-router-dom';
import { Sparkles, Target, BookOpen, TrendingUp, ArrowRight, Brain, Users, Award } from 'lucide-react';

const Home = () => {
  const features = [
    {
      icon: Brain,
      title: 'AI-Powered Recommendations',
      description: 'Get personalized career suggestions using OpenAI GPT-4o-mini'
    },
    {
      icon: Target,
      title: '24+ Career Paths',
      description: 'Explore comprehensive career options in tech, AI/ML, data, and more'
    },
    {
      icon: BookOpen,
      title: 'Learning Roadmaps',
      description: 'Get step-by-step learning paths for your chosen career'
    },
    {
      icon: TrendingUp,
      title: 'Career Insights',
      description: 'Understand salary ranges, growth potential, and required skills'
    }
  ];

  const categories = [
    { name: 'Software Development', count: 4, color: 'bg-blue-500' },
    { name: 'AI/ML', count: 7, color: 'bg-purple-500' },
    { name: 'Data', count: 3, color: 'bg-green-500' },
    { name: 'Cloud/DevOps', count: 3, color: 'bg-orange-500' },
    { name: 'Cybersecurity', count: 2, color: 'bg-red-500' },
    { name: 'Other', count: 5, color: 'bg-indigo-500' }
  ];

  const testimonials = [
    {
      quote: 'This platform is a game-changer! The AI recommendations were spot-on and helped me discover a career path I had never considered.',
      name: 'Alex Johnson',
      title: 'Aspiring Data Scientist'
    },
    {
      quote: 'The learning roadmaps are incredibly detailed and actionable. I finally have a clear plan to transition into a new role.',
      name: 'Samantha Lee',
      title: 'Marketing Professional'
    },
    {
      quote: 'I was feeling lost in my career, but this tool gave me the clarity and confidence I needed to move forward. Highly recommended!',
      name: 'Michael Chen',
      title: 'Recent Graduate'
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div className="relative bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white overflow-hidden">
        <div className="absolute inset-0 bg-grid-pattern opacity-10"></div>
        <div className="container mx-auto px-4 py-24 relative z-10">
          <div className="max-w-4xl mx-auto text-center">
            <div className="flex justify-center mb-6">
              <Sparkles className="h-16 w-16 text-yellow-400 animate-pulse" />
            </div>
            <h1 className="text-5xl md:text-7xl font-extrabold mb-6 tracking-tight">
              Find Your Future in Tech
            </h1>
            <p className="text-xl md:text-2xl mb-10 text-gray-300 max-w-3xl mx-auto">
              Navigate the complexities of the tech industry with AI-driven career guidance and personalized learning roadmaps.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/profile"
                className="bg-indigo-600 text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-indigo-700 transition-all transform hover:scale-105 shadow-lg flex items-center justify-center gap-2"
              >
                Get Your Free Analysis
                <ArrowRight className="h-5 w-5" />
              </Link>
              <Link
                to="/careers"
                className="bg-transparent border-2 border-gray-400 text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-white hover:text-gray-900 transition-all"
              >
                Explore Careers
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="container mx-auto px-4 py-20">
        <h2 className="text-4xl font-bold text-center mb-16 text-gray-900">
          A Smarter Way to Plan Your Career
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <div
                key={index}
                className="bg-white p-8 rounded-xl shadow-lg hover:shadow-2xl transition-all transform hover:-translate-y-2"
              >
                <div className="bg-gradient-to-br from-indigo-500 to-purple-600 w-14 h-14 rounded-xl flex items-center justify-center mb-5">
                  <Icon className="h-7 w-7 text-white" />
                </div>
                <h3 className="text-xl font-semibold mb-3 text-gray-900">{feature.title}</h3>
                <p className="text-gray-600 leading-relaxed">{feature.description}</p>
              </div>
            );
          })}
        </div>
      </div>

      {/* Categories Section */}
      <div className="bg-white py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-16 text-gray-900">
            Explore Career Categories
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
            {categories.map((category, index) => (
              <Link
                key={index}
                to="/careers"
                className="group block text-center p-4 rounded-xl transition-all transform hover:scale-110 hover:bg-gray-100"
              >
                <div className={`w-16 h-16 rounded-full mx-auto mb-4 flex items-center justify-center ${category.color} transition-all group-hover:shadow-lg`}>
                  <span className="text-2xl font-bold text-white">{category.count}</span>
                </div>
                <h3 className="text-lg font-semibold text-gray-800 group-hover:text-indigo-600">{category.name}</h3>
              </Link>
            ))}
          </div>
        </div>
      </div>

      {/* Testimonials Section */}
      <div className="bg-gray-50 py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-16 text-gray-900">What Our Users Say</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <div key={index} className="bg-white p-8 rounded-xl shadow-lg">
                <p className="text-gray-600 italic mb-6">"{testimonial.quote}"</p>
                <div className="flex items-center">
                  <div className="w-12 h-12 rounded-full bg-indigo-100 flex items-center justify-center mr-4">
                    <span className="text-xl font-bold text-indigo-600">{testimonial.name.charAt(0)}</span>
                  </div>
                  <div>
                    <p className="font-semibold text-gray-900">{testimonial.name}</p>
                    <p className="text-gray-500">{testimonial.title}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-gray-800 text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <Award className="h-16 w-16 mx-auto mb-6 text-yellow-400" />
          <h2 className="text-4xl font-bold mb-4">Ready to Unlock Your Potential?</h2>
          <p className="text-xl mb-8 text-gray-300 max-w-2xl mx-auto">
            Take the first step towards a fulfilling tech career. Get your personalized analysis today.
          </p>
          <Link
            to="/profile"
            className="bg-indigo-600 text-white px-10 py-4 rounded-lg font-semibold text-lg hover:bg-indigo-700 transition-all transform hover:scale-105 shadow-lg inline-flex items-center gap-2"
          >
            Start Your Journey
            <ArrowRight className="h-5 w-5" />
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Home;
