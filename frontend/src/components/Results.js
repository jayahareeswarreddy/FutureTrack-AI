import React from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import { Sparkles, TrendingUp, BookOpen, DollarSign, Target, ArrowRight, CheckCircle } from 'lucide-react';

const Results = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { recommendations, profile } = location.state || {};

  if (!recommendations || !recommendations.recommendations) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600 mb-4">No recommendations found.</p>
          <Link to="/profile" className="text-blue-600 hover:underline">
            Go back to create profile
          </Link>
        </div>
      </div>
    );
  }

  const topRecommendations = recommendations.recommendations;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 py-12">
      <div className="container mx-auto px-4 max-w-6xl">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex justify-center mb-4">
            <Sparkles className="h-12 w-12 text-purple-600" />
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Your AI Career Recommendations
          </h1>
          <p className="text-xl text-gray-600">
            {recommendations.user_profile_summary}
          </p>
        </div>

        {/* Recommendations */}
        <div className="space-y-6 mb-12">
          {topRecommendations.map((rec, index) => (
            <div
              key={index}
              className="bg-white rounded-xl shadow-lg p-8 hover:shadow-xl transition-shadow"
            >
              <div className="flex items-start justify-between mb-6">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-3">
                    <div className="bg-gradient-to-br from-blue-500 to-purple-500 text-white px-4 py-2 rounded-lg font-bold text-lg">
                      #{index + 1}
                    </div>
                    <h2 className="text-3xl font-bold text-gray-900">{rec.career}</h2>
                    <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full font-semibold">
                      {Math.round(rec.match_score * 100)}% Match
                    </span>
                  </div>
                  
                  {/* Reasoning */}
                  <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded mb-6">
                    <p className="text-gray-700 leading-relaxed">{rec.reasoning}</p>
                  </div>
                </div>
              </div>

              {/* Details Grid */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                <div className="bg-green-50 p-4 rounded-lg">
                  <DollarSign className="h-6 w-6 text-green-600 mb-2" />
                  <p className="text-sm text-gray-600 mb-1">Salary Range</p>
                  <p className="text-lg font-semibold text-gray-900">
                    ${(rec.salary_range.min / 1000).toFixed(0)}k - ${(rec.salary_range.max / 1000).toFixed(0)}k
                  </p>
                </div>
                
                <div className="bg-purple-50 p-4 rounded-lg">
                  <TrendingUp className="h-6 w-6 text-purple-600 mb-2" />
                  <p className="text-sm text-gray-600 mb-1">Growth Potential</p>
                  <p className="text-lg font-semibold text-gray-900">{rec.growth_potential}%</p>
                </div>
                
                <div className="bg-blue-50 p-4 rounded-lg">
                  <Target className="h-6 w-6 text-blue-600 mb-2" />
                  <p className="text-sm text-gray-600 mb-1">Required Skills</p>
                  <p className="text-lg font-semibold text-gray-900">{rec.required_skills.length} skills</p>
                </div>
              </div>

              {/* Required Skills */}
              <div className="mb-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-3">Required Skills:</h3>
                <div className="flex flex-wrap gap-2">
                  {rec.required_skills.map((skill, idx) => (
                    <span
                      key={idx}
                      className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>

              {/* Learning Path Preview */}
              <div className="mb-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center gap-2">
                  <BookOpen className="h-5 w-5 text-purple-600" />
                  Learning Roadmap (Preview)
                </h3>
                <ul className="space-y-2">
                  {rec.learning_path.slice(0, 3).map((step, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-gray-700">
                      <CheckCircle className="h-5 w-5 text-green-500 mt-0.5 flex-shrink-0" />
                      <span>{step}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Actions */}
              <div className="flex gap-4">
                <Link
                  to={`/careers/${rec.career.toLowerCase().replace(/\s+/g, '-')}`}
                  className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all text-center flex items-center justify-center gap-2"
                >
                  View Full Roadmap
                  <ArrowRight className="h-5 w-5" />
                </Link>
                <button
                  onClick={() => navigate('/careers')}
                  className="px-6 py-3 border-2 border-gray-300 text-gray-700 rounded-lg font-semibold hover:border-gray-400 transition-colors"
                >
                  Browse All Careers
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Actions */}
        <div className="text-center space-y-4">
          <button
            onClick={() => navigate('/profile')}
            className="text-blue-600 hover:underline font-semibold"
          >
            Update Profile & Get New Recommendations
          </button>
        </div>
      </div>
    </div>
  );
};

export default Results;
