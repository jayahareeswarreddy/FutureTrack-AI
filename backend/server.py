"""
FastAPI backend for the FutureTrack AI career recommender.

Match scores are computed deterministically in Python. An LLM (Groq by
default, OpenAI optionally) writes the explanations, roadmap detail and
skill-gap summaries, and every generation is JSON-schema validated with
retries before it reaches a client. With no key configured the service falls
back to rule-based text and stays fully functional.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import motor.motor_asyncio
from datetime import datetime, timezone
import os
import re
from dotenv import load_dotenv

import ai_client
from ai_client import AIUnavailable
from resources import get_resources_for_career, get_resources_for_skill
from schemas import REASONING_SCHEMA, ROADMAP_SCHEMA, SKILL_GAP_SCHEMA

load_dotenv()

app = FastAPI(
    title="AI Career Path Recommender API",
    description="AI-powered career guidance platform with OpenAI GPT-4o-mini",
    version="1.0.0"
)

# CORS middleware
# Origins allowed out of the box: local dev plus the published Pages site.
# ALLOWED_ORIGINS (comma-separated) *extends* this rather than replacing it,
# so setting it in a hosting dashboard cannot accidentally lock out the
# deployed frontend.
DEFAULT_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:3001",
    "https://jayahareeswarreddy.github.io",
]
ALLOWED_ORIGINS = DEFAULT_ORIGINS + [
    o.strip()
    for o in os.getenv("ALLOWED_ORIGINS", "").split(",")
    if o.strip() and o.strip() not in DEFAULT_ORIGINS
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    # Preview deployments get a generated subdomain per build.
    allow_origin_regex=r"https://.*\.(vercel\.app|onrender\.com|github\.io)",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection (optional - will use in-memory data if not available)
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
client = None
db = None
careers_collection = None
users_collection = None

try:
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL, serverSelectionTimeoutMS=2000)
    db = client.career_path_db
    careers_collection = db.careers
    users_collection = db.users
    print("[ok] MongoDB connection initialized")
except Exception as e:
    print(f"[warn] MongoDB not available, using in-memory data: {e}")
    client = None

# Pydantic models
class UserProfile(BaseModel):
    skills: List[str] = []
    interests: List[str] = []
    education_level: str = ""
    experience_years: int = 0
    goals: str = ""
    current_role: Optional[str] = None
    location: Optional[str] = None

class CareerRecommendation(BaseModel):
    career: str
    career_id: str
    match_score: float
    reasoning: str
    required_skills: List[str]
    learning_path: List[str]
    salary_range: dict
    growth_potential: int

class RecommendationResponse(BaseModel):
    recommendations: List[CareerRecommendation]
    user_profile_summary: str

class SkillGapRequest(BaseModel):
    career_id: str
    skills: List[str] = []
    experience_years: int = 0

class SkillGapResponse(BaseModel):
    career: str
    career_id: str
    coverage: float
    skills_matched: List[str]
    skills_missing: List[str]
    preferred_skills_matched: List[str]
    priority_order: List[str]
    estimated_months: float
    summary: str
    ai_generated: bool

# Profiles saved without a database live here for the life of the process.
PROFILE_CACHE: dict = {}

# Comprehensive Career Database (24+ Paths)
CAREER_DATABASE = [
    # Software Development
    {
        "id": "frontend-developer",
        "title": "Frontend Developer",
        "category": "Software Development",
        "description": "Build user-facing web applications using modern frameworks like React, Vue, or Angular",
        "required_skills": ["HTML", "CSS", "JavaScript", "React", "TypeScript", "Responsive Design"],
        "preferred_skills": ["Vue.js", "Angular", "Next.js", "GraphQL", "Webpack"],
        "salary_range": {"min": 60000, "max": 120000, "currency": "USD"},
        "growth_potential": 90,
        "learning_path": [
            "Master HTML5 and CSS3 fundamentals",
            "Learn JavaScript ES6+ and modern frameworks",
            "Build projects with React or Vue.js",
            "Learn state management (Redux, Vuex)",
            "Master responsive design and accessibility",
            "Build portfolio with 5+ projects"
        ]
    },
    {
        "id": "backend-developer",
        "title": "Backend Developer",
        "category": "Software Development",
        "description": "Develop server-side logic, APIs, and database systems",
        "required_skills": ["Python", "Node.js", "SQL", "REST APIs", "Database Design"],
        "preferred_skills": ["Django", "Flask", "Express", "PostgreSQL", "MongoDB", "GraphQL"],
        "salary_range": {"min": 70000, "max": 130000, "currency": "USD"},
        "growth_potential": 88,
        "learning_path": [
            "Learn Python or Node.js fundamentals",
            "Master database design and SQL",
            "Build RESTful APIs",
            "Learn authentication and security",
            "Understand microservices architecture",
            "Deploy applications to cloud platforms"
        ]
    },
    {
        "id": "fullstack-developer",
        "title": "Full-Stack Developer",
        "category": "Software Development",
        "description": "Work on both frontend and backend development",
        "required_skills": ["JavaScript", "React", "Node.js", "SQL", "REST APIs"],
        "preferred_skills": ["TypeScript", "Next.js", "MongoDB", "Docker", "AWS"],
        "salary_range": {"min": 75000, "max": 140000, "currency": "USD"},
        "growth_potential": 92,
        "learning_path": [
            "Master frontend frameworks (React, Vue)",
            "Learn backend development (Node.js, Python)",
            "Understand database systems",
            "Learn DevOps and deployment",
            "Build full-stack applications",
            "Master version control and collaboration"
        ]
    },
    {
        "id": "mobile-developer",
        "title": "Mobile Developer",
        "category": "Software Development",
        "description": "Develop native or cross-platform mobile applications",
        "required_skills": ["React Native", "Swift", "Kotlin", "Mobile UI/UX"],
        "preferred_skills": ["Flutter", "iOS Development", "Android Development", "Firebase"],
        "salary_range": {"min": 70000, "max": 130000, "currency": "USD"},
        "growth_potential": 85,
        "learning_path": [
            "Learn React Native or Flutter",
            "Understand mobile app architecture",
            "Master mobile UI/UX design principles",
            "Learn app store deployment",
            "Build and publish mobile apps",
            "Understand push notifications and analytics"
        ]
    },
    # AI/ML
    {
        "id": "data-scientist",
        "title": "Data Scientist",
        "category": "AI/ML",
        "description": "Analyze data and build ML models to solve business problems",
        "required_skills": ["Python", "SQL", "Machine Learning", "Statistics", "Data Analysis"],
        "preferred_skills": ["TensorFlow", "PyTorch", "Pandas", "NumPy", "Tableau", "AWS"],
        "salary_range": {"min": 80000, "max": 150000, "currency": "USD"},
        "growth_potential": 95,
        "learning_path": [
            "Master Python for data science",
            "Learn statistics and probability",
            "Study machine learning algorithms",
            "Practice with real datasets",
            "Learn data visualization tools",
            "Build ML models and deploy them"
        ]
    },
    {
        "id": "ml-engineer",
        "title": "ML Engineer",
        "category": "AI/ML",
        "description": "Design and deploy machine learning systems at scale",
        "required_skills": ["Python", "TensorFlow", "PyTorch", "MLOps", "Cloud Computing"],
        "preferred_skills": ["Kubernetes", "Docker", "AWS", "MLflow", "Airflow"],
        "salary_range": {"min": 100000, "max": 180000, "currency": "USD"},
        "growth_potential": 98,
        "learning_path": [
            "Master deep learning frameworks",
            "Learn MLOps and model deployment",
            "Understand cloud platforms (AWS, GCP)",
            "Learn containerization (Docker, Kubernetes)",
            "Build end-to-end ML pipelines",
            "Master model monitoring and optimization"
        ]
    },
    {
        "id": "nlp-engineer",
        "title": "NLP Engineer",
        "category": "AI/ML",
        "description": "Develop natural language processing systems and applications",
        "required_skills": ["Python", "NLP", "Transformers", "Deep Learning", "Text Processing"],
        "preferred_skills": ["BERT", "GPT", "Hugging Face", "spaCy", "NLTK"],
        "salary_range": {"min": 95000, "max": 170000, "currency": "USD"},
        "growth_potential": 96,
        "learning_path": [
            "Learn NLP fundamentals",
            "Master transformer architectures",
            "Work with pre-trained models",
            "Build NLP applications",
            "Learn model fine-tuning",
            "Deploy NLP systems to production"
        ]
    },
    {
        "id": "computer-vision-engineer",
        "title": "Computer Vision Engineer",
        "category": "AI/ML",
        "description": "Develop computer vision and image processing systems",
        "required_skills": ["Python", "OpenCV", "Deep Learning", "Image Processing", "CNN"],
        "preferred_skills": ["TensorFlow", "PyTorch", "YOLO", "Image Classification"],
        "salary_range": {"min": 95000, "max": 170000, "currency": "USD"},
        "growth_potential": 94,
        "learning_path": [
            "Learn computer vision fundamentals",
            "Master OpenCV and image processing",
            "Study CNN architectures",
            "Build image classification models",
            "Learn object detection",
            "Deploy CV systems to production"
        ]
    },
    {
        "id": "ai-researcher",
        "title": "AI Researcher",
        "category": "AI/ML",
        "description": "Conduct research in artificial intelligence and machine learning",
        "required_skills": ["Python", "Research", "Mathematics", "Deep Learning", "Publications"],
        "preferred_skills": ["PyTorch", "TensorFlow", "Research Papers", "PhD"],
        "salary_range": {"min": 120000, "max": 200000, "currency": "USD"},
        "growth_potential": 99,
        "learning_path": [
            "Pursue advanced degree (Master's/PhD)",
            "Read and understand research papers",
            "Contribute to open-source projects",
            "Publish research papers",
            "Attend conferences and workshops",
            "Build cutting-edge AI systems"
        ]
    },
    {
        "id": "deep-learning-engineer",
        "title": "Deep Learning Engineer",
        "category": "AI/ML",
        "description": "Specialize in deep learning architectures and neural networks",
        "required_skills": ["Python", "Deep Learning", "Neural Networks", "TensorFlow", "PyTorch"],
        "preferred_skills": ["CNN", "RNN", "GAN", "Transfer Learning", "GPU Computing"],
        "salary_range": {"min": 105000, "max": 185000, "currency": "USD"},
        "growth_potential": 97,
        "learning_path": [
            "Master neural network fundamentals",
            "Learn deep learning frameworks",
            "Study advanced architectures",
            "Work with GPUs and distributed training",
            "Build complex DL models",
            "Optimize and deploy models"
        ]
    },
    {
        "id": "mlops-engineer",
        "title": "MLOps Engineer",
        "category": "AI/ML",
        "description": "Operationalize machine learning models and pipelines",
        "required_skills": ["Python", "MLOps", "Docker", "Kubernetes", "CI/CD"],
        "preferred_skills": ["MLflow", "Kubeflow", "Airflow", "AWS SageMaker", "Monitoring"],
        "salary_range": {"min": 110000, "max": 180000, "currency": "USD"},
        "growth_potential": 95,
        "learning_path": [
            "Learn DevOps fundamentals",
            "Master containerization (Docker)",
            "Learn orchestration (Kubernetes)",
            "Understand ML pipeline tools",
            "Build automated ML workflows",
            "Master model monitoring and versioning"
        ]
    },
    # Data
    {
        "id": "data-analyst",
        "title": "Data Analyst",
        "category": "Data",
        "description": "Analyze data to provide insights and support business decisions",
        "required_skills": ["SQL", "Excel", "Python", "Data Visualization", "Statistics"],
        "preferred_skills": ["Tableau", "Power BI", "Pandas", "R", "Business Intelligence"],
        "salary_range": {"min": 60000, "max": 100000, "currency": "USD"},
        "growth_potential": 85,
        "learning_path": [
            "Master SQL and database queries",
            "Learn data visualization tools",
            "Study statistics and analytics",
            "Practice with real business data",
            "Build dashboards and reports",
            "Understand business metrics"
        ]
    },
    {
        "id": "data-engineer",
        "title": "Data Engineer",
        "category": "Data",
        "description": "Design and build data pipelines and infrastructure",
        "required_skills": ["Python", "SQL", "ETL", "Big Data", "Data Pipelines"],
        "preferred_skills": ["Apache Spark", "Airflow", "Kafka", "AWS", "Hadoop"],
        "salary_range": {"min": 85000, "max": 140000, "currency": "USD"},
        "growth_potential": 90,
        "learning_path": [
            "Master SQL and databases",
            "Learn ETL processes",
            "Understand big data technologies",
            "Build data pipelines",
            "Learn cloud data services",
            "Master data warehousing"
        ]
    },
    {
        "id": "business-intelligence-developer",
        "title": "Business Intelligence Developer",
        "category": "Data",
        "description": "Create BI solutions and dashboards for business insights",
        "required_skills": ["SQL", "BI Tools", "Data Warehousing", "ETL", "Analytics"],
        "preferred_skills": ["Tableau", "Power BI", "Qlik", "SSAS", "Data Modeling"],
        "salary_range": {"min": 70000, "max": 120000, "currency": "USD"},
        "growth_potential": 87,
        "learning_path": [
            "Master SQL and data modeling",
            "Learn BI tools (Tableau, Power BI)",
            "Understand data warehousing",
            "Build interactive dashboards",
            "Learn ETL processes",
            "Understand business requirements"
        ]
    },
    # Cloud/DevOps
    {
        "id": "devops-engineer",
        "title": "DevOps Engineer",
        "category": "Cloud/DevOps",
        "description": "Automate infrastructure and deployment processes",
        "required_skills": ["Linux", "Docker", "Kubernetes", "CI/CD", "AWS"],
        "preferred_skills": ["Terraform", "Ansible", "Jenkins", "GitLab CI", "Monitoring"],
        "salary_range": {"min": 85000, "max": 140000, "currency": "USD"},
        "growth_potential": 92,
        "learning_path": [
            "Master Linux and shell scripting",
            "Learn containerization (Docker)",
            "Understand orchestration (Kubernetes)",
            "Build CI/CD pipelines",
            "Learn infrastructure as code",
            "Master cloud platforms"
        ]
    },
    {
        "id": "cloud-architect",
        "title": "Cloud Architect",
        "category": "Cloud/DevOps",
        "description": "Design and implement cloud infrastructure solutions",
        "required_skills": ["AWS", "Azure", "GCP", "Architecture", "Cloud Security"],
        "preferred_skills": ["Terraform", "CloudFormation", "Kubernetes", "Serverless"],
        "salary_range": {"min": 100000, "max": 160000, "currency": "USD"},
        "growth_potential": 93,
        "learning_path": [
            "Get cloud certifications (AWS, Azure, GCP)",
            "Learn infrastructure as code",
            "Understand cloud architecture patterns",
            "Master security and compliance",
            "Design scalable systems",
            "Lead cloud migration projects"
        ]
    },
    {
        "id": "site-reliability-engineer",
        "title": "Site Reliability Engineer",
        "category": "Cloud/DevOps",
        "description": "Ensure system reliability and performance",
        "required_skills": ["Linux", "Monitoring", "Incident Response", "Automation", "SRE"],
        "preferred_skills": ["Prometheus", "Grafana", "Kubernetes", "Python", "Go"],
        "salary_range": {"min": 95000, "max": 150000, "currency": "USD"},
        "growth_potential": 91,
        "learning_path": [
            "Master system administration",
            "Learn monitoring and observability",
            "Understand incident management",
            "Build automation tools",
            "Learn SRE principles",
            "Master reliability engineering"
        ]
    },
    # Cybersecurity
    {
        "id": "security-engineer",
        "title": "Security Engineer",
        "category": "Cybersecurity",
        "description": "Protect systems and networks from security threats",
        "required_skills": ["Cybersecurity", "Network Security", "Security Tools", "Risk Assessment"],
        "preferred_skills": ["Penetration Testing", "SIEM", "Firewalls", "Encryption", "Compliance"],
        "salary_range": {"min": 80000, "max": 140000, "currency": "USD"},
        "growth_potential": 94,
        "learning_path": [
            "Learn cybersecurity fundamentals",
            "Study network security",
            "Master security tools",
            "Get security certifications",
            "Practice ethical hacking",
            "Build security systems"
        ]
    },
    {
        "id": "penetration-tester",
        "title": "Penetration Tester",
        "category": "Cybersecurity",
        "description": "Test systems for security vulnerabilities",
        "required_skills": ["Penetration Testing", "Ethical Hacking", "Security Tools", "Vulnerability Assessment"],
        "preferred_skills": ["Kali Linux", "Metasploit", "OWASP", "Certifications", "Reporting"],
        "salary_range": {"min": 75000, "max": 130000, "currency": "USD"},
        "growth_potential": 89,
        "learning_path": [
            "Learn ethical hacking fundamentals",
            "Master penetration testing tools",
            "Get certifications (CEH, OSCP)",
            "Practice on vulnerable systems",
            "Learn reporting and documentation",
            "Build security testing skills"
        ]
    },
    # Other
    {
        "id": "ui-ux-designer",
        "title": "UI/UX Designer",
        "category": "Other",
        "description": "Design user interfaces and user experiences",
        "required_skills": ["UI Design", "UX Design", "Design Tools", "User Research", "Prototyping"],
        "preferred_skills": ["Figma", "Sketch", "Adobe XD", "User Testing", "Design Systems"],
        "salary_range": {"min": 65000, "max": 120000, "currency": "USD"},
        "growth_potential": 88,
        "learning_path": [
            "Learn design principles",
            "Master design tools (Figma, Sketch)",
            "Study user research methods",
            "Build design portfolio",
            "Learn prototyping",
            "Understand design systems"
        ]
    },
    {
        "id": "product-manager",
        "title": "Product Manager",
        "category": "Other",
        "description": "Manage product development and strategy",
        "required_skills": ["Product Management", "Strategy", "Analytics", "Communication", "Roadmapping"],
        "preferred_skills": ["Agile", "Scrum", "User Stories", "A/B Testing", "Stakeholder Management"],
        "salary_range": {"min": 90000, "max": 160000, "currency": "USD"},
        "growth_potential": 90,
        "learning_path": [
            "Learn product management fundamentals",
            "Master agile methodologies",
            "Understand analytics and metrics",
            "Build product strategy skills",
            "Learn stakeholder management",
            "Get product management certification"
        ]
    },
    {
        "id": "qa-engineer",
        "title": "QA Engineer",
        "category": "Other",
        "description": "Test software for quality and bugs",
        "required_skills": ["Testing", "Test Automation", "QA", "Bug Tracking", "Test Planning"],
        "preferred_skills": ["Selenium", "Cypress", "Jest", "API Testing", "Performance Testing"],
        "salary_range": {"min": 60000, "max": 110000, "currency": "USD"},
        "growth_potential": 86,
        "learning_path": [
            "Learn testing fundamentals",
            "Master test automation tools",
            "Understand testing methodologies",
            "Build test frameworks",
            "Learn API and performance testing",
            "Get QA certifications"
        ]
    },
    {
        "id": "blockchain-developer",
        "title": "Blockchain Developer",
        "category": "Other",
        "description": "Develop blockchain and cryptocurrency applications",
        "required_skills": ["Blockchain", "Solidity", "Smart Contracts", "Web3", "Cryptography"],
        "preferred_skills": ["Ethereum", "DeFi", "NFT", "Truffle", "Hardhat"],
        "salary_range": {"min": 90000, "max": 160000, "currency": "USD"},
        "growth_potential": 93,
        "learning_path": [
            "Learn blockchain fundamentals",
            "Master Solidity programming",
            "Build smart contracts",
            "Understand DeFi protocols",
            "Learn Web3 development",
            "Deploy blockchain applications"
        ]
    },
    {
        "id": "game-developer",
        "title": "Game Developer",
        "category": "Other",
        "description": "Develop video games and interactive experiences",
        "required_skills": ["Game Development", "Unity", "C#", "Game Design", "3D Graphics"],
        "preferred_skills": ["Unreal Engine", "Game Physics", "Animation", "Multiplayer", "VR/AR"],
        "salary_range": {"min": 65000, "max": 120000, "currency": "USD"},
        "growth_potential": 87,
        "learning_path": [
            "Learn game development fundamentals",
            "Master Unity or Unreal Engine",
            "Study game design principles",
            "Build game projects",
            "Learn 3D graphics and animation",
            "Publish games to app stores"
        ]
    }
]

@app.get("/")
async def root():
    return {
        "message": "AI Career Path Recommender API",
        "version": "1.0.0",
        "status": "running"
    }

@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Seed the career collection on boot, then hand control to the app."""
    """Initialize database with career data"""
    try:
        if careers_collection is not None:
            count = await careers_collection.count_documents({})
            if count == 0:
                await careers_collection.insert_many(CAREER_DATABASE)
                print(f"[ok] Initialized {len(CAREER_DATABASE)} careers in database")
            else:
                print(f"[ok] Database already has {count} careers")
        else:
            print(f"[ok] Using in-memory career database ({len(CAREER_DATABASE)} careers)")
    except Exception as e:
        print(f"[warn] Database initialization error, using in-memory data: {e}")
    yield


app.router.lifespan_context = lifespan


@app.get("/careers")
async def get_all_careers():
    """Get all available career paths"""
    try:
        # Try to get from database first
        if careers_collection is not None:
            try:
                careers = await careers_collection.find({}).to_list(length=100)
                if careers and len(careers) > 0:
                    # Remove MongoDB _id field
                    for career in careers:
                        if '_id' in career:
                            career.pop('_id', None)
                    print(f"[ok] Returning {len(careers)} careers from database")
                    return careers
            except Exception as db_error:
                print(f"[warn] Database error, using in-memory data: {db_error}")
        
        # Fallback to in-memory database
        print(f"[ok] Returning {len(CAREER_DATABASE)} careers from in-memory database")
        return CAREER_DATABASE
    except Exception as e:
        print(f"[error] Error fetching careers: {e}")
        import traceback
        traceback.print_exc()
        # Always return in-memory data as fallback
        return CAREER_DATABASE

@app.get("/careers/search")
async def search_careers(q: str = ""):
    """Search careers by query"""
    try:
        careers = []
        # A raw query string is not a safe regex: "C++" or "(" would raise.
        safe_q = re.escape(q) if q else ""
        if careers_collection is not None:
            query = {
                "$or": [
                    {"title": {"$regex": safe_q, "$options": "i"}},
                    {"description": {"$regex": safe_q, "$options": "i"}},
                    {"category": {"$regex": safe_q, "$options": "i"}},
                    {"required_skills": {"$regex": safe_q, "$options": "i"}}
                ]
            } if q else {}
            careers = await careers_collection.find(query).to_list(length=50)
            # Mongo's ObjectId is not JSON serialisable, so drop it before
            # the response is encoded.
            for c in careers:
                c.pop("_id", None)

        if not careers:
            # Fallback search
            careers = [c for c in CAREER_DATABASE if q.lower() in c["title"].lower() or 
                      q.lower() in c["description"].lower() or 
                      q.lower() in c["category"].lower()]
        return careers
    except Exception as e:
        # Fallback to in-memory search
        print(f"Error searching careers, falling back to in-memory: {e}")
        return [c for c in CAREER_DATABASE if q.lower() in c["title"].lower() or 
                q.lower() in c["description"].lower()]

@app.get("/careers/{career_id}")
async def get_career(career_id: str):
    """Get specific career details"""
    try:
        career = None
        if careers_collection is not None:
            try:
                career = await careers_collection.find_one({"id": career_id})
                if career and '_id' in career:
                    career.pop('_id', None)
            except Exception as db_error:
                print(f"[warn] Database error in get_career, falling back to in-memory: {db_error}")

        if career is None:
            # Fallback to in-memory database
            print(f"Searching for career {career_id} in-memory")
            career = next((c for c in CAREER_DATABASE if c["id"] == career_id), None)

        if career is None:
            print(f"[error] Career with id {career_id} not found anywhere.")
            raise HTTPException(status_code=404, detail="Career not found")
        
        print(f"[ok] Successfully found career: {career.get('title')}")
        return career
    except HTTPException:
        raise
    except Exception as e:
        print(f"[error] Unexpected error in get_career: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@app.post("/recommendations", response_model=RecommendationResponse)
async def get_recommendations(profile: UserProfile):
    """
    Get AI-powered career recommendations using OpenAI GPT-4o-mini
    """
    try:
        # Calculate match scores for all careers
        all_careers = CAREER_DATABASE  # Default to in-memory
        if careers_collection is not None:
            try:
                db_careers = await careers_collection.find({}).to_list(length=100)
                if db_careers and len(db_careers) > 0:
                    # Remove MongoDB _id fields
                    for c in db_careers:
                        if '_id' in c:
                            c.pop('_id', None)
                    all_careers = db_careers
            except Exception as db_error:
                print(f"Database error, using in-memory data: {db_error}")
        
        recommendations = []
        
        for career in all_careers:
            match_score = calculate_match_score(profile, career)
            if match_score > 0.2:  # Only include relevant careers
                # Generate AI reasoning if OpenAI is available
                try:
                    reasoning = await generate_ai_reasoning(profile, career, match_score)
                except Exception as ai_error:
                    print(f"AI reasoning error, using rule-based: {ai_error}")
                    reasoning = generate_rule_based_reasoning(profile, career, match_score)
                
                recommendations.append({
                    "career": career["title"],
                    "career_id": career["id"],
                    "match_score": match_score,
                    "reasoning": reasoning,
                    "required_skills": career.get("required_skills", []),
                    "learning_path": career.get("learning_path", []),
                    "salary_range": career.get("salary_range", {}),
                    "growth_potential": career.get("growth_potential", 0)
                })
        
        # Sort by match score
        recommendations.sort(key=lambda x: x["match_score"], reverse=True)
        
        # Get top 3 recommendations (or all if less than 3)
        top_recommendations = recommendations[:3] if len(recommendations) >= 3 else recommendations
        
        # If no recommendations, return top careers anyway
        if not top_recommendations:
            top_recommendations = [
                {
                    "career": career["title"],
                    "career_id": career["id"],
                    "match_score": 0.5,
                    "reasoning": f"This is a popular career path in {career['category']} that you might be interested in.",
                    "required_skills": career.get("required_skills", []),
                    "learning_path": career.get("learning_path", []),
                    "salary_range": career.get("salary_range", {}),
                    "growth_potential": career.get("growth_potential", 0)
                }
                for career in all_careers[:3]
            ]
        
        # Generate user profile summary
        profile_summary = f"Profile with {len(profile.skills)} skills, {profile.experience_years} years experience, interested in {', '.join(profile.interests[:3]) if profile.interests else 'various fields'}"
        
        return {
            "recommendations": top_recommendations,
            "user_profile_summary": profile_summary
        }
    except Exception as e:
        print(f"Error in get_recommendations: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

async def generate_ai_reasoning(profile: UserProfile, career: dict, score: float) -> str:
    """
    Personalised reasoning from the configured LLM, schema-validated with retries.

    Falls back to the deterministic rule-based explanation when the key is
    absent or every retry is exhausted, so this never fails a request.
    """
    if not ai_client.is_configured():
        return generate_rule_based_reasoning(profile, career, score)

    system = (
        "You are a career guidance expert. You explain why a specific career "
        "path fits a candidate, concretely and without flattery."
    )
    user = f"""Explain in 2-3 sentences why this career matches this profile.

User profile
- Skills: {', '.join(profile.skills[:10]) or 'none given'}
- Interests: {', '.join(profile.interests[:5]) or 'none given'}
- Experience: {profile.experience_years} years
- Education: {profile.education_level or 'not given'}
- Goals: {profile.goals or 'not given'}

Career: {career['title']} ({career['category']})
Required skills: {', '.join(career.get('required_skills', [])[:6])}
Computed match score: {score:.0%}

Reference the candidate's actual skills. Do not invent experience they did
not list."""

    ai_client.stats.calls += 1
    try:
        result = await ai_client.generate_validated(
            system=system,
            user=user,
            schema=REASONING_SCHEMA,
            on_attempt=lambda n, err: ai_client.stats.record_attempt(err),
        )
        return result["reasoning"].strip()
    except AIUnavailable as exc:
        ai_client.stats.failures += 1
        print(f"AI reasoning unavailable, using rule-based: {exc}")
        return generate_rule_based_reasoning(profile, career, score)


def generate_rule_based_reasoning(profile: UserProfile, career: dict, score: float) -> str:
    """Generate rule-based reasoning when AI is not available"""
    matching_skills = [s for s in career.get("required_skills", []) 
                       if any(s.lower() in skill.lower() or skill.lower() in s.lower() 
                             for skill in profile.skills)]
    
    reasons = []
    if matching_skills:
        reasons.append(f"Your skills in {', '.join(matching_skills[:2])} align well with this role")
    if profile.experience_years > 0:
        reasons.append(f"Your {profile.experience_years} years of experience are valuable")
    if profile.interests and any(interest.lower() in career["category"].lower() for interest in profile.interests):
        reasons.append(f"This matches your interest in {career['category']}")
    
    if not reasons:
        reasons.append(f"This career path offers strong growth potential in {career['category']}")
    
    return ". ".join(reasons) + f" Match score: {score:.0%}"

def calculate_match_score(profile: UserProfile, career: dict) -> float:
    """Calculate match score between user profile and career"""
    score = 0.0
    max_score = 0.0
    
    user_skills_lower = [s.lower() for s in profile.skills]
    required_skills = career.get("required_skills", [])
    preferred_skills = career.get("preferred_skills", [])
    
    # Required skills matching (50% weight)
    if required_skills:
        matching_required = sum(1 for skill in required_skills 
                               if any(us in skill.lower() or skill.lower() in us 
                                     for us in user_skills_lower))
        skill_match = matching_required / len(required_skills)
        score += skill_match * 0.5
        max_score += 0.5
    
    # Preferred skills matching (20% weight)
    if preferred_skills:
        matching_preferred = sum(1 for skill in preferred_skills 
                                if any(us in skill.lower() or skill.lower() in us 
                                      for us in user_skills_lower))
        preferred_match = matching_preferred / len(preferred_skills)
        score += preferred_match * 0.2
        max_score += 0.2
    
    # Experience level (15% weight)
    exp_score = min(profile.experience_years / 5, 1.0)
    score += exp_score * 0.15
    max_score += 0.15
    
    # Interest matching (15% weight)
    if profile.interests:
        category_lower = career["category"].lower()
        interest_match = any(interest.lower() in category_lower or 
                            category_lower in interest.lower() 
                            for interest in profile.interests)
        if interest_match:
            score += 0.15
        max_score += 0.15
    
    return min(score / max_score if max_score > 0 else 0, 1.0)

@app.get("/careers/{career_id}/roadmap")
async def get_learning_roadmap(career_id: str):
    """Get learning roadmap for a specific career"""
    try:
        career = None
        if careers_collection is not None:
            try:
                career = await careers_collection.find_one({"id": career_id})
                if career and '_id' in career:
                    career.pop('_id', None)
            except Exception as db_error:
                print(f"Database error, using in-memory: {db_error}")
        
        if career is None:
            # Fallback to in-memory database
            career = next((c for c in CAREER_DATABASE if c["id"] == career_id), None)
        
        if career is None:
            raise HTTPException(status_code=404, detail=f"Career with id '{career_id}' not found")
        
        # Get enhanced roadmap using ChatGPT if API key is available
        roadmap_steps = career.get("learning_path", [])
        
        if ai_client.is_configured() and roadmap_steps:
            try:
                enhanced_roadmap = await enhance_roadmap_with_ai(career, roadmap_steps)
                roadmap_steps = enhanced_roadmap
            except Exception as ai_error:
                print(f"AI enhancement failed, using default roadmap: {ai_error}")
        
        return {
            "career": career["title"],
            "roadmap": roadmap_steps,
            "required_skills": career.get("required_skills", []),
            "preferred_skills": career.get("preferred_skills", []),
            "estimated_time": "6-12 months",
            "difficulty": "Intermediate to Advanced"
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_learning_roadmap: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generating roadmap: {str(e)}")

async def enhance_roadmap_with_ai(career: dict, base_roadmap: list) -> list:
    """
    Expand a roadmap into structured, validated steps.

    Returns a list of dicts with step/title/description/duration/resources.
    On any failure the plain-string base roadmap is returned unchanged, so the
    endpoint's response shape stays predictable for the client.
    """
    if not ai_client.is_configured():
        return base_roadmap

    system = (
        "You are an educational expert who turns coarse learning paths into "
        "detailed, actionable, correctly ordered steps."
    )
    steps_text = chr(10).join(f"- {s}" for s in base_roadmap)
    user = f"""Expand this learning roadmap for a {career['title']} in {career['category']}.

Base steps:
{steps_text}

Keep the same overall progression. For each step give a title, a one-sentence
description, a realistic duration, and up to three concrete resource types."""

    ai_client.stats.calls += 1
    try:
        result = await ai_client.generate_validated(
            system=system,
            user=user,
            schema=ROADMAP_SCHEMA,
            on_attempt=lambda n, err: ai_client.stats.record_attempt(err),
        )
        return result["steps"]
    except AIUnavailable as exc:
        ai_client.stats.failures += 1
        print(f"AI roadmap enhancement unavailable, using base roadmap: {exc}")
        return base_roadmap


# ==========================================================================
# Endpoints 7-12. The six above cover careers and recommendations; these add
# observability, taxonomy, skill-gap analysis and profile persistence.
# ==========================================================================

async def _find_career(career_id: str):
    """Look up one career: MongoDB first, then the in-memory catalogue."""
    if careers_collection is not None:
        try:
            found = await careers_collection.find_one({"id": career_id})
            if found:
                found.pop("_id", None)
                return found
        except Exception as exc:
            print(f"Database error during career lookup, using in-memory: {exc}")
    return next((c for c in CAREER_DATABASE if c["id"] == career_id), None)


@app.get("/careers/{career_id}/resources")
async def get_career_resources(career_id: str):
    """
    Curated learning material for a career, grouped by required skill.

    Official documentation, free books and courses are exact URLs; video
    entries are YouTube searches rather than pinned video IDs, so they do not
    rot when an uploader removes a video.
    """
    career = await _find_career(career_id)
    if career is None:
        raise HTTPException(
            status_code=404, detail=f"Career with id '{career_id}' not found"
        )
    return get_resources_for_career(career)


@app.get("/resources")
async def get_resources(skill: str):
    """Resources for a single named skill, for the skill-gap panel."""
    if not skill.strip():
        raise HTTPException(status_code=422, detail="skill must not be empty")
    return {"skill": skill, "resources": get_resources_for_skill(skill)}


@app.get("/health")
async def health_check():
    """
    Readiness probe. Reports which optional dependencies actually resolved,
    plus AI retry counters, so a deployed instance can be diagnosed from
    outside without reading logs.
    """
    mongo_ok = False
    mongo_detail = "not configured"
    if client is not None:
        try:
            await client.admin.command("ping")
            mongo_ok = True
            mongo_detail = "connected"
        except Exception as exc:
            mongo_detail = f"unreachable: {type(exc).__name__}"

    return {
        "status": "healthy",
        "version": app.version,
        "dependencies": {
            "mongodb": {"ok": mongo_ok, "detail": mongo_detail},
            "ai": {
                "ok": ai_client.is_configured(),
                **ai_client.describe_provider(),
                "detail": "configured" if ai_client.is_configured()
                          else f"{ai_client.provider_config()['env_key']} not set "
                               "- rule-based fallback active",
            },
        },
        "careers_available": len(CAREER_DATABASE),
        "ai_metrics": ai_client.stats.as_dict(),
    }


@app.get("/categories")
async def list_categories():
    """Career categories with counts, for building filter UI."""
    counts: dict = {}
    for career in CAREER_DATABASE:
        category = career.get("category", "Uncategorised")
        counts.setdefault(category, []).append(career["title"])

    return {
        "total_categories": len(counts),
        "categories": [
            {"name": name, "career_count": len(titles), "careers": sorted(titles)}
            for name, titles in sorted(counts.items())
        ],
    }


@app.get("/skills")
async def list_skills(limit: int = 100):
    """
    Skill catalogue aggregated across every career, most in-demand first.
    Powers autocomplete on the profile form.
    """
    if limit < 1 or limit > 500:
        raise HTTPException(status_code=422, detail="limit must be between 1 and 500")

    demand: dict = {}
    for career in CAREER_DATABASE:
        for skill in career.get("required_skills", []):
            entry = demand.setdefault(skill, {"required_by": 0, "preferred_by": 0})
            entry["required_by"] += 1
        for skill in career.get("preferred_skills", []):
            entry = demand.setdefault(skill, {"required_by": 0, "preferred_by": 0})
            entry["preferred_by"] += 1

    ranked = sorted(
        (
            {
                "skill": name,
                "required_by": v["required_by"],
                "preferred_by": v["preferred_by"],
                "demand_score": v["required_by"] * 2 + v["preferred_by"],
            }
            for name, v in demand.items()
        ),
        key=lambda s: (-s["demand_score"], s["skill"]),
    )

    return {"total_skills": len(ranked), "skills": ranked[:limit]}


@app.post("/skill-gap", response_model=SkillGapResponse)
async def analyse_skill_gap(request: SkillGapRequest):
    """
    Compare a profile's skills against one career's requirements and return
    what is already covered, what is missing, and a prioritised plan.
    """
    career = next(
        (c for c in CAREER_DATABASE if c["id"] == request.career_id), None
    )
    if career is None:
        raise HTTPException(
            status_code=404, detail=f"Career with id '{request.career_id}' not found"
        )

    owned = {s.strip().lower() for s in request.skills if s.strip()}
    required = career.get("required_skills", [])
    preferred = career.get("preferred_skills", [])

    have = [s for s in required if s.lower() in owned]
    missing = [s for s in required if s.lower() not in owned]
    bonus = [s for s in preferred if s.lower() in owned]

    coverage = len(have) / len(required) if required else 0.0

    summary = (
        f"You cover {len(have)} of {len(required)} required skills for "
        f"{career['title']} ({coverage:.0%}). "
        + (
            f"The gap is: {', '.join(missing)}."
            if missing
            else "You meet every listed requirement."
        )
    )
    priority = missing[:]
    estimated_months = round(len(missing) * 1.5, 1)

    # Optional AI pass. Deterministic numbers above are never overwritten,
    # only the prose summary and ordering are improved.
    if ai_client.is_configured() and missing:
        ai_client.stats.calls += 1
        try:
            result = await ai_client.generate_validated(
                system=(
                    "You are a technical mentor. You advise on the order to "
                    "learn missing skills and how long it realistically takes."
                ),
                user=(
                    f"Target career: {career['title']} ({career['category']})\n"
                    f"Already has: {', '.join(have) or 'nothing from the list'}\n"
                    f"Missing: {', '.join(missing)}\n"
                    f"Experience: {request.experience_years} years\n\n"
                    "Give a short summary, the missing skills in the order they "
                    "should be learned, and an estimate in months."
                ),
                schema=SKILL_GAP_SCHEMA,
                on_attempt=lambda n, err: ai_client.stats.record_attempt(err),
            )
            summary = result["summary"].strip()
            ai_order = [s for s in result.get("priority_order", []) if s in missing]
            if ai_order:
                priority = ai_order + [s for s in missing if s not in ai_order]
            if result.get("estimated_months"):
                estimated_months = float(result["estimated_months"])
        except AIUnavailable as exc:
            ai_client.stats.failures += 1
            print(f"AI skill-gap unavailable, using rule-based: {exc}")

    return {
        "career": career["title"],
        "career_id": career["id"],
        "coverage": round(coverage, 3),
        "skills_matched": have,
        "skills_missing": missing,
        "preferred_skills_matched": bonus,
        "priority_order": priority,
        "estimated_months": estimated_months,
        "summary": summary,
        "ai_generated": ai_client.is_configured() and bool(missing),
    }


@app.post("/profiles", status_code=201)
async def save_profile(profile: UserProfile):
    """
    Persist a profile so a result can be revisited by id. Writes to MongoDB
    when it is reachable and to an in-process store otherwise, so the demo
    works on a host with no database attached.
    """
    import uuid

    profile_id = uuid.uuid4().hex[:12]
    record = {
        "profile_id": profile_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "profile": profile.model_dump(),
    }

    stored_in = "memory"
    if users_collection is not None:
        try:
            await users_collection.insert_one(dict(record))
            stored_in = "mongodb"
        except Exception as exc:
            print(f"Profile write to MongoDB failed, keeping in memory: {exc}")

    PROFILE_CACHE[profile_id] = record
    return {"profile_id": profile_id, "stored_in": stored_in, **record}


@app.get("/profiles/{profile_id}")
async def get_profile(profile_id: str):
    """Retrieve a saved profile together with fresh recommendations."""
    record = PROFILE_CACHE.get(profile_id)

    if record is None and users_collection is not None:
        try:
            found = await users_collection.find_one({"profile_id": profile_id})
            if found:
                found.pop("_id", None)
                record = found
        except Exception as exc:
            print(f"Profile read from MongoDB failed: {exc}")

    if record is None:
        raise HTTPException(
            status_code=404, detail=f"Profile '{profile_id}' not found"
        )

    recommendations = await get_recommendations(UserProfile(**record["profile"]))
    return {**record, "recommendations": recommendations["recommendations"]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))