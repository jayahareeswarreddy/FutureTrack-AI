import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Search, Filter, ArrowRight, TrendingUp, DollarSign } from 'lucide-react';
import { getCareers, searchCareers } from '../lib/api';

const CareerBrowser = () => {
  const [careers, setCareers] = useState([]);
  const [filteredCareers, setFilteredCareers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');

  const categories = ['all', 'Software Development', 'AI/ML', 'Data', 'Cloud/DevOps', 'Cybersecurity', 'Other'];

  useEffect(() => {
    loadCareers();
  }, []);

  useEffect(() => {
    filterCareers();
  }, [searchQuery, selectedCategory, careers]);

  const loadCareers = async () => {
    try {
      setLoading(true);
      const data = await getCareers();
      console.log('Loaded careers:', data?.length || 0);
      if (data && Array.isArray(data) && data.length > 0) {
        setCareers(data);
        setFilteredCareers(data);
      } else {
        console.error('No careers data received');
        // Retry once after a delay
        setTimeout(async () => {
          try {
            const retryData = await getCareers();
            if (retryData && Array.isArray(retryData) && retryData.length > 0) {
              setCareers(retryData);
              setFilteredCareers(retryData);
            }
          } catch (retryError) {
            console.error('Retry failed:', retryError);
          }
        }, 2000);
      }
    } catch (error) {
      console.error('Error loading careers:', error);
      alert('Failed to load careers. Please check if backend server is running on http://localhost:8000');
    } finally {
      setLoading(false);
    }
  };

  const filterCareers = () => {
    let filtered = careers;

    // Filter by category
    if (selectedCategory !== 'all') {
      filtered = filtered.filter(career => career.category === selectedCategory);
    }

    // Filter by search query
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(career =>
        career.title.toLowerCase().includes(query) ||
        career.description.toLowerCase().includes(query) ||
        career.category.toLowerCase().includes(query) ||
        career.required_skills.some(skill => skill.toLowerCase().includes(query))
      );
    }

    setFilteredCareers(filtered);
  };

  const getCategoryColor = (category) => {
    const colors = {
      'Software Development': 'bg-blue-100 text-blue-800',
      'AI/ML': 'bg-purple-100 text-purple-800',
      'Data': 'bg-green-100 text-green-800',
      'Cloud/DevOps': 'bg-orange-100 text-orange-800',
      'Cybersecurity': 'bg-red-100 text-red-800',
      'Other': 'bg-indigo-100 text-indigo-800'
    };
    return colors[category] || 'bg-gray-100 text-gray-800';
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading careers...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 py-12">
      <div className="container mx-auto px-4 max-w-7xl">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Explore Career Paths</h1>
          <p className="text-xl text-gray-600">
            Discover {careers.length} career opportunities in technology
          </p>
        </div>

        {/* Search and Filter */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search careers by name, skills, or category..."
                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div className="flex items-center gap-2">
              <Filter className="h-5 w-5 text-gray-400" />
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                {categories.map(cat => (
                  <option key={cat} value={cat}>
                    {cat === 'all' ? 'All Categories' : cat}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Results Count */}
        <div className="mb-6">
          <p className="text-gray-600">
            Showing <span className="font-semibold text-gray-900">{filteredCareers.length}</span> career paths
          </p>
        </div>

        {/* Careers Grid */}
        {filteredCareers.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-xl shadow-lg">
            <p className="text-gray-600 text-lg">No careers found matching your criteria.</p>
            <button
              onClick={() => {
                setSearchQuery('');
                setSelectedCategory('all');
              }}
              className="mt-4 text-blue-600 hover:underline"
            >
              Clear filters
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredCareers.map((career) => (
              <div
                key={career.id}
                className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-all hover:scale-105"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <h3 className="text-xl font-bold text-gray-900 mb-2">{career.title}</h3>
                    <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${getCategoryColor(career.category)}`}>
                      {career.category}
                    </span>
                  </div>
                </div>

                <p className="text-gray-600 mb-4 line-clamp-2">{career.description}</p>

                <div className="grid grid-cols-2 gap-3 mb-4">
                  <div className="bg-green-50 p-3 rounded-lg">
                    <DollarSign className="h-4 w-4 text-green-600 mb-1" />
                    <p className="text-xs text-gray-600">Salary</p>
                    <p className="text-sm font-semibold text-gray-900">
                      ${(career.salary_range.min / 1000).toFixed(0)}k-${(career.salary_range.max / 1000).toFixed(0)}k
                    </p>
                  </div>
                  <div className="bg-purple-50 p-3 rounded-lg">
                    <TrendingUp className="h-4 w-4 text-purple-600 mb-1" />
                    <p className="text-xs text-gray-600">Growth</p>
                    <p className="text-sm font-semibold text-gray-900">{career.growth_potential}%</p>
                  </div>
                </div>

                <div className="mb-4">
                  <p className="text-sm text-gray-600 mb-2">Key Skills:</p>
                  <div className="flex flex-wrap gap-1">
                    {career.required_skills.slice(0, 3).map((skill, idx) => (
                      <span
                        key={idx}
                        className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs"
                      >
                        {skill}
                      </span>
                    ))}
                    {career.required_skills.length > 3 && (
                      <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">
                        +{career.required_skills.length - 3}
                      </span>
                    )}
                  </div>
                </div>

                <Link
                  to={`/careers/${career.id}`}
                  className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white px-4 py-2 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all flex items-center justify-center gap-2"
                >
                  View Details
                  <ArrowRight className="h-4 w-4" />
                </Link>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default CareerBrowser;
