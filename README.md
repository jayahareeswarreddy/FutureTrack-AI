
# 🚀 AI-Powered Career Path Recommender

A comprehensive career guidance platform using OpenAI GPT-4o-mini with FastAPI backend and React frontend.

## ✨ Features

- **AI-Powered Recommendations**: Personalized career suggestions using OpenAI GPT-4o-mini
- **24+ Career Paths**: Comprehensive database covering Software Development, AI/ML, Data, Cloud/DevOps, Cybersecurity, and more
- **Learning Roadmaps**: Step-by-step learning paths for each career
- **Career Browser**: Search and filter through all available careers
- **Modern UI/UX**: Beautiful, responsive design with Tailwind CSS

## 🏗️ Project Structure

```
careerpath/
├── backend/          # FastAPI backend
│   ├── server.py     # Main API server
│   └── requirements.txt
├── frontend/         # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── lib/
│   │   └── App.js
│   └── package.json
└── tests/            # Test files
```

## 🚀 Getting Started

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create .env file
MONGODB_URL=mongodb://localhost:27017
OPENAI_API_KEY=your_openai_api_key_here
```

4. Run the server:
```bash
python server.py
# or
uvicorn server:app --reload
```

Backend will run on `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
# or
yarn install
```

3. Set environment variable (optional):
```bash
# Create .env file
REACT_APP_API_URL=http://localhost:8000
```

4. Start the development server:
```bash
npm start
# or
yarn start
```

Frontend will run on `http://localhost:3000`

## 📚 API Endpoints

- `GET /` - API info
- `GET /careers` - Get all career paths
- `GET /careers/{career_id}` - Get specific career details
- `GET /careers/search?q=query` - Search careers
- `POST /recommendations` - Get AI-powered career recommendations
- `GET /careers/{career_id}/roadmap` - Get learning roadmap

## 🛠️ Technology Stack

- **Backend**: FastAPI, Python, Motor (MongoDB), OpenAI
- **Frontend**: React 19, Tailwind CSS, Axios, React Router
- **Database**: MongoDB
- **AI**: OpenAI GPT-4o-mini

## 📝 License

MIT