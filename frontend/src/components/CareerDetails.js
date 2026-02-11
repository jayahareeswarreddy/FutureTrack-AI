import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, BookOpen, DollarSign, TrendingUp, CheckCircle, Target, Clock } from 'lucide-react';
import { getCareerById, getLearningRoadmap } from '../lib/api';

const CareerDetails = () => {
  const { id } = useParams();
  const [career, setCareer] = useState(null);
  const [roadmap, setRoadmap] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadCareerDetails();
  }, [id]);

  const loadCareerDetails = async () => {
    try {
      setLoading(true);
      const careerData = await getCareerById(id);
      console.log('Career data:', careerData);
      setCareer(careerData);
      
      // Use career's learning_path as a fallback roadmap first
      if (careerData && careerData.learning_path) {
        setRoadmap({
          career: careerData.title,
          roadmap: careerData.learning_path,
          required_skills: careerData.required_skills || [],
          preferred_skills: careerData.preferred_skills || [],
          estimated_time: "6-12 months",
          difficulty: "Intermediate to Advanced"
        });
      }

      // Then, try to fetch the enhanced roadmap from the API
      try {
        const roadmapData = await getLearningRoadmap(id);
        console.log('Roadmap data:', roadmapData);
        setRoadmap(roadmapData); // This will overwrite the fallback if successful
      } catch (roadmapError) {
        console.error('Could not load enhanced roadmap, using default.', roadmapError);
      }

    } catch (error) {
      console.error('Error loading career details:', error);
      alert(`Error loading career: ${error.message || 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading career details...</p>
        </div>
      </div>
    );
  }

  if (!career) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600 mb-4">Career not found.</p>
          <Link to="/careers" className="text-blue-600 hover:underline">
            Browse all careers
          </Link>
        </div>
      </div>
    );
  }

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

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 py-12">
      <div className="container mx-auto px-4 max-w-5xl">
        {/* Back Button */}
        <Link
          to="/careers"
          className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 mb-6"
        >
          <ArrowLeft className="h-5 w-5" />
          Back to Careers
        </Link>

        {/* Career Header */}
        <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
          <div className="flex items-start justify-between mb-6">
            <div className="flex-1">
              <h1 className="text-4xl font-bold text-gray-900 mb-4">{career.title}</h1>
              <span className={`inline-block px-4 py-2 rounded-full text-sm font-semibold ${getCategoryColor(career.category)}`}>
                {career.category}
              </span>
            </div>
          </div>

          <p className="text-lg text-gray-700 mb-8 leading-relaxed">{career.description}</p>

          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-green-50 p-6 rounded-lg">
              <DollarSign className="h-8 w-8 text-green-600 mb-3" />
              <p className="text-sm text-gray-600 mb-1">Salary Range</p>
              <p className="text-2xl font-bold text-gray-900">
                ${(career.salary_range.min / 1000).toFixed(0)}k - ${(career.salary_range.max / 1000).toFixed(0)}k
              </p>
            </div>

            <div className="bg-purple-50 p-6 rounded-lg">
              <TrendingUp className="h-8 w-8 text-purple-600 mb-3" />
              <p className="text-sm text-gray-600 mb-1">Growth Potential</p>
              <p className="text-2xl font-bold text-gray-900">{career.growth_potential}%</p>
            </div>

            <div className="bg-blue-50 p-6 rounded-lg">
              <Target className="h-8 w-8 text-blue-600 mb-3" />
              <p className="text-sm text-gray-600 mb-1">Required Skills</p>
              <p className="text-2xl font-bold text-gray-900">{career.required_skills.length}</p>
            </div>
          </div>
        </div>

        {/* Required Skills */}
        <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Required Skills</h2>
          <div className="flex flex-wrap gap-3">
            {career.required_skills.map((skill, idx) => (
              <span
                key={idx}
                className="px-4 py-2 bg-blue-100 text-blue-800 rounded-lg font-medium"
              >
                {skill}
              </span>
            ))}
          </div>
        </div>

        {/* Preferred Skills */}
        {career.preferred_skills && career.preferred_skills.length > 0 && (
          <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Preferred Skills</h2>
            <div className="flex flex-wrap gap-3">
              {career.preferred_skills.map((skill, idx) => (
                <span
                  key={idx}
                  className="px-4 py-2 bg-purple-100 text-purple-800 rounded-lg font-medium"
                >
                  {skill}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Learning Roadmap */}
        {roadmap && (
          <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
            <div className="flex items-center gap-3 mb-6">
              <BookOpen className="h-8 w-8 text-purple-600" />
              <div>
                <h2 className="text-2xl font-bold text-gray-900">Learning Roadmap</h2>
                <p className="text-gray-600">
                  {roadmap.estimated_time} • {roadmap.difficulty}
                </p>
              </div>
            </div>

            <div className="space-y-4">
              {roadmap.roadmap.map((step, idx) => (
                <div key={idx} className="flex items-start gap-4 p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg">
                  <div className="flex-shrink-0 w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white font-bold">
                    {idx + 1}
                  </div>
                  <div className="flex-1">
                    <p className="text-gray-900 font-medium">{step}</p>
                  </div>
                  <CheckCircle className="h-5 w-5 text-green-500 flex-shrink-0" />
                </div>
              ))}
            </div>
          </div>
        )}

        {/* CTA */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl shadow-lg p-8 text-center">
          <h2 className="text-2xl font-bold mb-4">Ready to Start This Career Path?</h2>
          <p className="text-blue-100 mb-6">
            Get personalized recommendations and start your learning journey today
          </p>
          <Link
            to="/profile"
            className="inline-block bg-white text-purple-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
          >
            Create Your Profile
          </Link>
        </div>
      </div>
    </div>
  );
};

export default CareerDetails;
