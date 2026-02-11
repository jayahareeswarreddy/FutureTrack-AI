import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { User, Plus, X, Loader2, ArrowRight, ArrowLeft, Briefcase, Target, GraduationCap, Lightbulb } from 'lucide-react';
import { getRecommendations } from '../lib/api';

const ProfileForm = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    skills: [],
    interests: [],
    education_level: '',
    experience_years: 0,
    goals: '',
    current_role: '',
    location: ''
  });

  const [skillInput, setSkillInput] = useState('');
  const [interestInput, setInterestInput] = useState('');

  const commonSkills = ['JavaScript', 'Python', 'Java', 'React', 'Node.js', 'SQL', 'AWS', 'Docker', 'Git', 'TypeScript', 'Machine Learning', 'Data Analysis'];
  const commonInterests = ['Software Development', 'AI/ML', 'Data Science', 'Cloud Computing', 'Cybersecurity', 'Web Development', 'Mobile Development', 'DevOps', 'UI/UX Design', 'Product Management'];

  const addSkill = (skill) => {
    if (skill && !formData.skills.includes(skill)) {
      setFormData({ ...formData, skills: [...formData.skills, skill] });
      setSkillInput('');
    }
  };

  const removeSkill = (skill) => {
    setFormData({ ...formData, skills: formData.skills.filter(s => s !== skill) });
  };

  const addInterest = (interest) => {
    if (interest && !formData.interests.includes(interest)) {
      setFormData({ ...formData, interests: [...formData.interests, interest] });
      setInterestInput('');
    }
  };

  const removeInterest = (interest) => {
    setFormData({ ...formData, interests: formData.interests.filter(i => i !== interest) });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const recommendations = await getRecommendations(formData);
      navigate('/results', { state: { recommendations, profile: formData } });
    } catch (error) {
      console.error('Error getting recommendations:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Failed to get recommendations. Please try again.';
      
      if (errorMessage.includes('Backend server is not running')) {
        alert('Backend server is not running!\n\nPlease:\n1. Open a terminal\n2. cd backend\n3. python server.py\n\nThen try again.');
      } else {
        alert(`Error: ${errorMessage}\n\nPlease check:\n1. Backend server is running on http://localhost:8000\n2. Check browser console for details`);
      }
    } finally {
      setLoading(false);
    }
  };

  const nextStep = () => setStep(prev => Math.min(prev + 1, 4));
  const prevStep = () => setStep(prev => Math.max(prev - 1, 1));

  const renderStep = () => {
    switch (step) {
      case 1:
        return (
          <div className="space-y-8 animate-fade-in">
            {/* Skills Section */}
            <div>
              <label className="block text-lg font-semibold text-gray-800 mb-4 flex items-center"><Briefcase className="h-5 w-5 mr-2 text-indigo-500"/>What are your technical skills?</label>
              <p className="text-gray-600 mb-4">List your programming languages, frameworks, and tools. This helps us match you with the right technologies.</p>
              <div className="flex gap-2 mb-3">
                <input
                  type="text"
                  value={skillInput}
                  onChange={(e) => setSkillInput(e.target.value)}
                  onKeyPress={(e) => {
                    if (e.key === 'Enter') {
                      e.preventDefault();
                      addSkill(skillInput);
                    }
                  }}
                  placeholder="e.g., Python, React, AWS"
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-shadow shadow-sm"
                />
                <button
                  type="button"
                  onClick={() => addSkill(skillInput)}
                  className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-all transform hover:scale-105 shadow-md"
                >
                  <Plus className="h-5 w-5" />
                </button>
              </div>
              <div className="flex flex-wrap gap-2 mb-4">
                {commonSkills.map(skill => (
                  <button
                    key={skill}
                    type="button"
                    onClick={() => addSkill(skill)}
                    className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm hover:bg-indigo-100 hover:text-indigo-700 transition-colors"
                  >
                    + {skill}
                  </button>
                ))}
              </div>
              <div className="flex flex-wrap gap-3 p-4 bg-gray-50 rounded-lg min-h-[50px]">
                {formData.skills.map(skill => (
                  <span
                    key={skill}
                    className="inline-flex items-center gap-2 px-3 py-1 bg-indigo-100 text-indigo-800 rounded-full text-sm font-medium shadow-sm"
                  >
                    {skill}
                    <button
                      type="button"
                      onClick={() => removeSkill(skill)}
                      className="hover:text-indigo-600"
                    >
                      <X className="h-4 w-4" />
                    </button>
                  </span>
                ))}
              </div>
            </div>
          </div>
        );
      case 2:
        return (
          <div className="space-y-8 animate-fade-in">
            {/* Interests Section */}
            <div>
              <label className="block text-lg font-semibold text-gray-800 mb-4 flex items-center"><Target className="h-5 w-5 mr-2 text-purple-500"/>What are your career interests?</label>
              <p className="text-gray-600 mb-4">Tell us which fields excite you the most. This helps us find roles you'll be passionate about.</p>
              <div className="flex gap-2 mb-3">
                <input
                  type="text"
                  value={interestInput}
                  onChange={(e) => setInterestInput(e.target.value)}
                  onKeyPress={(e) => {
                    if (e.key === 'Enter') {
                      e.preventDefault();
                      addInterest(interestInput);
                    }
                  }}
                  placeholder="e.g., AI/ML, Cybersecurity"
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-shadow shadow-sm"
                />
                <button
                  type="button"
                  onClick={() => addInterest(interestInput)}
                  className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-all transform hover:scale-105 shadow-md"
                >
                  <Plus className="h-5 w-5" />
                </button>
              </div>
              <div className="flex flex-wrap gap-2 mb-4">
                {commonInterests.map(interest => (
                  <button
                    key={interest}
                    type="button"
                    onClick={() => addInterest(interest)}
                    className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm hover:bg-purple-100 hover:text-purple-700 transition-colors"
                  >
                    + {interest}
                  </button>
                ))}
              </div>
              <div className="flex flex-wrap gap-3 p-4 bg-gray-50 rounded-lg min-h-[50px]">
                {formData.interests.map(interest => (
                  <span
                    key={interest}
                    className="inline-flex items-center gap-2 px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm font-medium shadow-sm"
                  >
                    {interest}
                    <button
                      type="button"
                      onClick={() => removeInterest(interest)}
                      className="hover:text-purple-600"
                    >
                      <X className="h-4 w-4" />
                    </button>
                  </span>
                ))}
              </div>
            </div>
          </div>
        );
      case 3:
        return (
          <div className="space-y-8 animate-fade-in">
            {/* Education & Experience */}
            <div>
              <label className="block text-lg font-semibold text-gray-800 mb-4 flex items-center"><GraduationCap className="h-5 w-5 mr-2 text-green-500"/>What's your background?</label>
              <p className="text-gray-600 mb-4">Your education and experience help us gauge the seniority of roles to recommend.</p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Education Level</label>
                  <select
                    name="education_level"
                    value={formData.education_level}
                    onChange={(e) => setFormData({ ...formData, education_level: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-shadow shadow-sm"
                  >
                    <option value="">Select level</option>
                    <option value="High School">High School</option>
                    <option value="Bachelor's">Bachelor's Degree</option>
                    <option value="Master's">Master's Degree</option>
                    <option value="PhD">PhD</option>
                    <option value="Bootcamp">Bootcamp/Certificate</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Years of Experience</label>
                  <input
                    type="number"
                    name="experience_years"
                    value={formData.experience_years}
                    onChange={(e) => setFormData({ ...formData, experience_years: parseInt(e.target.value, 10) })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-shadow shadow-sm"
                    placeholder="e.g., 5"
                  />
                </div>
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Current or Most Recent Role</label>
              <input
                type="text"
                name="current_role"
                value={formData.current_role}
                onChange={(e) => setFormData({ ...formData, current_role: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-shadow shadow-sm"
                placeholder="e.g., Software Engineer"
              />
            </div>
          </div>
        );
      case 4:
        return (
          <div className="space-y-8 animate-fade-in">
            {/* Goals & Location */}
            <div>
              <label className="block text-lg font-semibold text-gray-800 mb-4 flex items-center"><Lightbulb className="h-5 w-5 mr-2 text-yellow-500"/>What are your career goals?</label>
              <p className="text-gray-600 mb-4">Describe your aspirations. Are you looking for growth, a specific salary, or work-life balance?</p>
              <textarea
                name="goals"
                value={formData.goals}
                onChange={(e) => setFormData({ ...formData, goals: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent transition-shadow shadow-sm h-32"
                placeholder="e.g., Transition to a leadership role in AI, achieve a salary of $150k, find a fully remote job."
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Preferred Location (optional)</label>
              <input
                type="text"
                name="location"
                value={formData.location}
                onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent transition-shadow shadow-sm"
                placeholder="e.g., Remote, New York, USA"
              />
            </div>
          </div>
        );
      default:
        return null;
    }
  };

  const steps = ['Skills', 'Interests', 'Experience', 'Goals'];

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="container mx-auto px-4 max-w-3xl">
        <div className="bg-white rounded-2xl shadow-2xl p-8 md:p-12">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-900">Let's Build Your Career Profile</h1>
            <p className="text-gray-600 mt-2">A few questions will help us tailor the perfect recommendations for you.</p>
          </div>

          {/* Progress Bar */}
          <div className="mb-8">
            <div className="flex justify-between mb-2">
              {steps.map((name, index) => (
                <div key={name} className={`text-sm font-medium ${step > index ? 'text-indigo-600' : 'text-gray-400'}`}>
                  {name}
                </div>
              ))}
            </div>
            <div className="bg-gray-200 rounded-full h-2">
              <div
                className="bg-indigo-600 rounded-full h-2 transition-all duration-500"
                style={{ width: `${((step - 1) / (steps.length - 1)) * 100}%` }}
              ></div>
            </div>
          </div>

          <form onSubmit={handleSubmit}>
            {renderStep()}
            <div className="flex justify-between items-center mt-12">
              <button
                type="button"
                onClick={prevStep}
                disabled={step === 1}
                className="px-6 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                <ArrowLeft className="h-4 w-4"/>
                Back
              </button>

              {step < 4 ? (
                <button
                  type="button"
                  onClick={nextStep}
                  className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors flex items-center gap-2"
                >
                  Next
                  <ArrowRight className="h-4 w-4"/>
                </button>
              ) : (
                <button
                  type="submit"
                  disabled={loading}
                  className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors disabled:bg-green-400 flex items-center gap-2"
                >
                  {loading ? (
                    <>
                      <Loader2 className="h-5 w-5 animate-spin" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      Get Recommendations
                      <ArrowRight className="h-4 w-4"/>
                    </>
                  )}
                </button>
              )}
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ProfileForm;
