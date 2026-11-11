"""
Curated learning resources, keyed by skill.

Editorial rules, so this stays trustworthy rather than becoming link rot:

* `docs`, `book` and `course` entries are exact URLs to canonical, stable
  homes — official documentation, or a book the author publishes free online.
  Nothing here is a deep link into a page that gets restructured.
* `video` entries are YouTube *search* URLs, not video IDs. A hand-picked
  video ID dies when the uploader removes it and silently 404s for the user;
  a search for the same topic keeps working and surfaces whatever is current
  and well-rated today.
* Everything listed is free to access without an account.

`get_resources_for_skill` falls back to a generated search bundle for any
skill not in the catalogue, so a new career entry never yields an empty panel.
"""

import re
from urllib.parse import quote_plus

# Resource kinds, in the order they should be shown to a learner.
KIND_ORDER = ["docs", "course", "video", "book"]


def _youtube(query: str) -> dict:
    return {
        "kind": "video",
        "title": f"{query} — video tutorials",
        "url": f"https://www.youtube.com/results?search_query={quote_plus(query)}",
        "provider": "YouTube",
    }


def _fcc(query: str) -> dict:
    return {
        "kind": "course",
        "title": f"{query} — freeCodeCamp full course",
        "url": f"https://www.youtube.com/results?search_query={quote_plus(query + ' full course freeCodeCamp')}",
        "provider": "freeCodeCamp",
    }


# ---------------------------------------------------------------------------
# Skill -> curated resources. Keys are matched case-insensitively.
# ---------------------------------------------------------------------------

CATALOGUE: dict[str, list[dict]] = {
    # ----------------------------------------------------------- languages
    "python": [
        {"kind": "docs", "title": "The Python Tutorial (official)", "url": "https://docs.python.org/3/tutorial/", "provider": "python.org"},
        {"kind": "book", "title": "Automate the Boring Stuff with Python (free online)", "url": "https://automatetheboringstuff.com/", "provider": "Al Sweigart"},
        {"kind": "course", "title": "Python for Everybody (free)", "url": "https://www.py4e.com/", "provider": "Dr. Chuck"},
        _youtube("Python tutorial for beginners"),
    ],
    "javascript": [
        {"kind": "docs", "title": "JavaScript guide", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide", "provider": "MDN"},
        {"kind": "book", "title": "Eloquent JavaScript (free online)", "url": "https://eloquentjavascript.net/", "provider": "Marijn Haverbeke"},
        {"kind": "book", "title": "You Don't Know JS Yet (free online)", "url": "https://github.com/getify/You-Dont-Know-JS", "provider": "Kyle Simpson"},
        _youtube("JavaScript tutorial for beginners"),
    ],
    "typescript": [
        {"kind": "docs", "title": "TypeScript Handbook", "url": "https://www.typescriptlang.org/docs/handbook/intro.html", "provider": "typescriptlang.org"},
        {"kind": "book", "title": "TypeScript Deep Dive (free online)", "url": "https://basarat.gitbook.io/typescript/", "provider": "Basarat Ali Syed"},
        _youtube("TypeScript tutorial"),
    ],
    "sql": [
        {"kind": "docs", "title": "PostgreSQL tutorial (official)", "url": "https://www.postgresql.org/docs/current/tutorial.html", "provider": "PostgreSQL"},
        {"kind": "course", "title": "SQLBolt — interactive SQL lessons", "url": "https://sqlbolt.com/", "provider": "SQLBolt"},
        {"kind": "course", "title": "Mode SQL Tutorial", "url": "https://mode.com/sql-tutorial/", "provider": "Mode"},
        _youtube("SQL tutorial for beginners"),
    ],
    "java": [
        {"kind": "docs", "title": "Java Tutorials (official)", "url": "https://dev.java/learn/", "provider": "Oracle"},
        {"kind": "docs", "title": "Java SE API documentation", "url": "https://docs.oracle.com/en/java/javase/21/docs/api/index.html", "provider": "Oracle"},
        {"kind": "course", "title": "Java Programming MOOC (free, University of Helsinki)", "url": "https://java-programming.mooc.fi/", "provider": "Univ. of Helsinki"},
        {"kind": "book", "title": "Introduction to Programming Using Java (free)", "url": "https://math.hws.edu/javanotes/", "provider": "David J. Eck"},
        _fcc("Java"),
        _youtube("Java tutorial for beginners"),
    ],
    "c#": [
        {"kind": "docs", "title": "C# documentation", "url": "https://learn.microsoft.com/en-us/dotnet/csharp/", "provider": "Microsoft Learn"},
        _youtube("C# tutorial for beginners"),
    ],
    "kotlin": [
        {"kind": "docs", "title": "Kotlin docs", "url": "https://kotlinlang.org/docs/home.html", "provider": "JetBrains"},
        _youtube("Kotlin Android tutorial"),
    ],
    "swift": [
        {"kind": "docs", "title": "The Swift Programming Language", "url": "https://docs.swift.org/swift-book/", "provider": "Apple"},
        _youtube("Swift iOS tutorial"),
    ],
    "go": [
        {"kind": "docs", "title": "A Tour of Go", "url": "https://go.dev/tour/", "provider": "go.dev"},
        {"kind": "docs", "title": "Effective Go", "url": "https://go.dev/doc/effective_go", "provider": "go.dev"},
    ],
    "rust": [
        {"kind": "book", "title": "The Rust Programming Language (free online)", "url": "https://doc.rust-lang.org/book/", "provider": "rust-lang.org"},
        {"kind": "course", "title": "Rustlings — exercises", "url": "https://github.com/rust-lang/rustlings", "provider": "rust-lang"},
    ],

    # ------------------------------------------------------------ frontend
    "html": [
        {"kind": "docs", "title": "HTML — Structuring the web", "url": "https://developer.mozilla.org/en-US/docs/Learn/HTML", "provider": "MDN"},
        {"kind": "course", "title": "web.dev — Learn HTML", "url": "https://web.dev/learn/html/", "provider": "Google"},
    ],
    "css": [
        {"kind": "docs", "title": "CSS — Styling the web", "url": "https://developer.mozilla.org/en-US/docs/Learn/CSS", "provider": "MDN"},
        {"kind": "course", "title": "web.dev — Learn CSS", "url": "https://web.dev/learn/css/", "provider": "Google"},
        {"kind": "course", "title": "Flexbox Froggy / Grid Garden", "url": "https://flexboxfroggy.com/", "provider": "Codepip"},
    ],
    "react": [
        {"kind": "docs", "title": "React — official docs & tutorial", "url": "https://react.dev/learn", "provider": "react.dev"},
        _fcc("React"),
        _youtube("React hooks tutorial"),
    ],
    "vue.js": [
        {"kind": "docs", "title": "Vue.js guide", "url": "https://vuejs.org/guide/introduction.html", "provider": "vuejs.org"},
    ],
    "angular": [
        {"kind": "docs", "title": "Angular docs", "url": "https://angular.dev/", "provider": "angular.dev"},
    ],
    "next.js": [
        {"kind": "docs", "title": "Next.js — Learn course", "url": "https://nextjs.org/learn", "provider": "Vercel"},
    ],
    "responsive design": [
        {"kind": "docs", "title": "Responsive design", "url": "https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design", "provider": "MDN"},
        {"kind": "course", "title": "web.dev — Learn Responsive Design", "url": "https://web.dev/learn/design/", "provider": "Google"},
    ],
    "accessibility": [
        {"kind": "docs", "title": "WCAG 2.2 quick reference", "url": "https://www.w3.org/WAI/WCAG22/quickref/", "provider": "W3C"},
        {"kind": "docs", "title": "ARIA Authoring Practices Guide", "url": "https://www.w3.org/WAI/ARIA/apg/", "provider": "W3C"},
    ],

    # ------------------------------------------------------------- backend
    "node.js": [
        {"kind": "docs", "title": "Node.js learn guides", "url": "https://nodejs.org/en/learn", "provider": "nodejs.org"},
        _fcc("Node.js and Express"),
    ],
    "rest apis": [
        {"kind": "docs", "title": "HTTP — MDN reference", "url": "https://developer.mozilla.org/en-US/docs/Web/HTTP", "provider": "MDN"},
        {"kind": "docs", "title": "OpenAPI Specification", "url": "https://spec.openapis.org/oas/latest.html", "provider": "OpenAPI Initiative"},
        {"kind": "docs", "title": "FastAPI tutorial", "url": "https://fastapi.tiangolo.com/tutorial/", "provider": "FastAPI"},
    ],
    "graphql": [
        {"kind": "docs", "title": "Introduction to GraphQL", "url": "https://graphql.org/learn/", "provider": "graphql.org"},
    ],
    "django": [
        {"kind": "docs", "title": "Django — write your first app", "url": "https://docs.djangoproject.com/en/stable/intro/tutorial01/", "provider": "Django"},
    ],
    "flask": [
        {"kind": "docs", "title": "Flask quickstart", "url": "https://flask.palletsprojects.com/en/stable/quickstart/", "provider": "Pallets"},
    ],
    "database design": [
        {"kind": "book", "title": "Database Design (free textbook)", "url": "https://opentextbc.ca/dbdesign01/", "provider": "BCcampus"},
        _youtube("database normalization tutorial"),
    ],
    "mongodb": [
        {"kind": "docs", "title": "MongoDB Manual", "url": "https://www.mongodb.com/docs/manual/", "provider": "MongoDB"},
        {"kind": "course", "title": "MongoDB University (free)", "url": "https://learn.mongodb.com/", "provider": "MongoDB"},
    ],
    "postgresql": [
        {"kind": "docs", "title": "PostgreSQL documentation", "url": "https://www.postgresql.org/docs/", "provider": "PostgreSQL"},
    ],

    # ------------------------------------------------------- data & ML
    "machine learning": [
        {"kind": "course", "title": "Machine Learning Crash Course", "url": "https://developers.google.com/machine-learning/crash-course", "provider": "Google"},
        {"kind": "book", "title": "An Introduction to Statistical Learning (free PDF)", "url": "https://www.statlearning.com/", "provider": "Springer"},
        {"kind": "course", "title": "fast.ai — Practical Deep Learning", "url": "https://course.fast.ai/", "provider": "fast.ai"},
        _youtube("machine learning full course"),
    ],
    "deep learning": [
        {"kind": "book", "title": "Deep Learning (free online book)", "url": "https://www.deeplearningbook.org/", "provider": "Goodfellow, Bengio, Courville"},
        {"kind": "book", "title": "Neural Networks and Deep Learning (free)", "url": "http://neuralnetworksanddeeplearning.com/", "provider": "Michael Nielsen"},
        {"kind": "video", "title": "Neural networks — visual explanation", "url": "https://www.youtube.com/results?search_query=3blue1brown+neural+networks", "provider": "3Blue1Brown"},
    ],
    "tensorflow": [
        {"kind": "docs", "title": "TensorFlow tutorials", "url": "https://www.tensorflow.org/tutorials", "provider": "TensorFlow"},
    ],
    "pytorch": [
        {"kind": "docs", "title": "PyTorch tutorials", "url": "https://pytorch.org/tutorials/", "provider": "PyTorch"},
        {"kind": "docs", "title": "Learn the Basics", "url": "https://pytorch.org/tutorials/beginner/basics/intro.html", "provider": "PyTorch"},
    ],
    "scikit-learn": [
        {"kind": "docs", "title": "scikit-learn user guide", "url": "https://scikit-learn.org/stable/user_guide.html", "provider": "scikit-learn"},
    ],
    "pandas": [
        {"kind": "docs", "title": "pandas — 10 minutes to pandas", "url": "https://pandas.pydata.org/docs/user_guide/10min.html", "provider": "pandas"},
    ],
    "numpy": [
        {"kind": "docs", "title": "NumPy — absolute beginner's guide", "url": "https://numpy.org/doc/stable/user/absolute_beginners.html", "provider": "NumPy"},
    ],
    "statistics": [
        {"kind": "course", "title": "Khan Academy — Statistics & Probability", "url": "https://www.khanacademy.org/math/statistics-probability", "provider": "Khan Academy"},
        {"kind": "book", "title": "OpenIntro Statistics (free PDF)", "url": "https://www.openintro.org/book/os/", "provider": "OpenIntro"},
        {"kind": "video", "title": "Statistics explained clearly", "url": "https://www.youtube.com/results?search_query=StatQuest+statistics+fundamentals", "provider": "StatQuest"},
    ],
    "mathematics": [
        {"kind": "video", "title": "Essence of Linear Algebra", "url": "https://www.youtube.com/results?search_query=3blue1brown+essence+of+linear+algebra", "provider": "3Blue1Brown"},
        {"kind": "book", "title": "Mathematics for Machine Learning (free PDF)", "url": "https://mml-book.github.io/", "provider": "Cambridge University Press"},
    ],
    "nlp": [
        {"kind": "course", "title": "Hugging Face NLP Course (free)", "url": "https://huggingface.co/learn/nlp-course", "provider": "Hugging Face"},
        {"kind": "book", "title": "Speech and Language Processing (free draft)", "url": "https://web.stanford.edu/~jurafsky/slp3/", "provider": "Jurafsky & Martin"},
    ],
    "data analysis": [
        {"kind": "course", "title": "Kaggle Learn — Data Analysis", "url": "https://www.kaggle.com/learn", "provider": "Kaggle"},
        _fcc("Data Analysis with Python"),
    ],
    "data visualization": [
        {"kind": "docs", "title": "Matplotlib tutorials", "url": "https://matplotlib.org/stable/tutorials/index.html", "provider": "Matplotlib"},
        {"kind": "book", "title": "Fundamentals of Data Visualization (free online)", "url": "https://clauswilke.com/dataviz/", "provider": "Claus Wilke"},
    ],
    "tableau": [
        {"kind": "course", "title": "Tableau free training videos", "url": "https://www.tableau.com/learn/training/", "provider": "Tableau"},
    ],
    "excel": [
        {"kind": "docs", "title": "Excel help & learning", "url": "https://support.microsoft.com/en-us/excel", "provider": "Microsoft"},
    ],
    "big data": [
        {"kind": "docs", "title": "Apache Spark documentation", "url": "https://spark.apache.org/docs/latest/", "provider": "Apache"},
    ],
    "etl": [
        {"kind": "docs", "title": "Apache Airflow — core concepts", "url": "https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/index.html", "provider": "Apache"},
    ],
    "airflow": [
        {"kind": "docs", "title": "Airflow tutorial", "url": "https://airflow.apache.org/docs/apache-airflow/stable/tutorial/index.html", "provider": "Apache"},
    ],
    "mlops": [
        {"kind": "course", "title": "MLOps Zoomcamp (free)", "url": "https://github.com/DataTalksClub/mlops-zoomcamp", "provider": "DataTalks.Club"},
        {"kind": "docs", "title": "MLflow documentation", "url": "https://mlflow.org/docs/latest/index.html", "provider": "MLflow"},
    ],
    "mlflow": [
        {"kind": "docs", "title": "MLflow documentation", "url": "https://mlflow.org/docs/latest/index.html", "provider": "MLflow"},
    ],
    "cnn": [
        {"kind": "course", "title": "CS231n — Convolutional Neural Networks", "url": "https://cs231n.github.io/", "provider": "Stanford"},
    ],
    "image processing": [
        {"kind": "docs", "title": "OpenCV-Python tutorials", "url": "https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html", "provider": "OpenCV"},
    ],

    # --------------------------------------------------- cloud & devops
    "docker": [
        {"kind": "docs", "title": "Docker — get started", "url": "https://docs.docker.com/get-started/", "provider": "Docker"},
        _fcc("Docker"),
    ],
    "kubernetes": [
        {"kind": "docs", "title": "Kubernetes basics tutorial", "url": "https://kubernetes.io/docs/tutorials/kubernetes-basics/", "provider": "Kubernetes"},
        {"kind": "course", "title": "Kubernetes the Hard Way", "url": "https://github.com/kelseyhightower/kubernetes-the-hard-way", "provider": "Kelsey Hightower"},
    ],
    "aws": [
        {"kind": "course", "title": "AWS Skill Builder (free tier)", "url": "https://skillbuilder.aws/", "provider": "AWS"},
        {"kind": "docs", "title": "AWS documentation", "url": "https://docs.aws.amazon.com/", "provider": "AWS"},
    ],
    "azure": [
        {"kind": "course", "title": "Microsoft Learn — Azure", "url": "https://learn.microsoft.com/en-us/training/azure/", "provider": "Microsoft"},
    ],
    "gcp": [
        {"kind": "course", "title": "Google Cloud Skills Boost", "url": "https://www.cloudskillsboost.google/", "provider": "Google Cloud"},
    ],
    "ci/cd": [
        {"kind": "docs", "title": "GitHub Actions documentation", "url": "https://docs.github.com/en/actions", "provider": "GitHub"},
        _youtube("CI CD pipeline tutorial"),
    ],
    "linux": [
        {"kind": "course", "title": "Linux Journey", "url": "https://linuxjourney.com/", "provider": "Linux Journey"},
        {"kind": "book", "title": "The Linux Command Line (free PDF)", "url": "https://linuxcommand.org/tlcl.php", "provider": "William Shotts"},
    ],
    "terraform": [
        {"kind": "docs", "title": "Terraform tutorials", "url": "https://developer.hashicorp.com/terraform/tutorials", "provider": "HashiCorp"},
    ],
    "monitoring": [
        {"kind": "docs", "title": "Prometheus documentation", "url": "https://prometheus.io/docs/introduction/overview/", "provider": "Prometheus"},
        {"kind": "book", "title": "Google SRE Book (free online)", "url": "https://sre.google/sre-book/table-of-contents/", "provider": "Google"},
    ],
    "git": [
        {"kind": "book", "title": "Pro Git (free book / PDF)", "url": "https://git-scm.com/book/en/v2", "provider": "git-scm.com"},
        {"kind": "course", "title": "Learn Git Branching (interactive)", "url": "https://learngitbranching.js.org/", "provider": "Peter Cottle"},
    ],

    # ------------------------------------------------------- security
    "cybersecurity": [
        {"kind": "docs", "title": "OWASP Top 10", "url": "https://owasp.org/www-project-top-ten/", "provider": "OWASP"},
        {"kind": "docs", "title": "NIST Cybersecurity Framework", "url": "https://www.nist.gov/cyberframework", "provider": "NIST"},
    ],
    "penetration testing": [
        {"kind": "docs", "title": "OWASP Web Security Testing Guide", "url": "https://owasp.org/www-project-web-security-testing-guide/", "provider": "OWASP"},
        {"kind": "course", "title": "TryHackMe (free rooms)", "url": "https://tryhackme.com/", "provider": "TryHackMe"},
        {"kind": "course", "title": "PortSwigger Web Security Academy (free)", "url": "https://portswigger.net/web-security", "provider": "PortSwigger"},
    ],
    "ethical hacking": [
        {"kind": "course", "title": "PortSwigger Web Security Academy (free)", "url": "https://portswigger.net/web-security", "provider": "PortSwigger"},
        {"kind": "course", "title": "Hack The Box", "url": "https://www.hackthebox.com/", "provider": "Hack The Box"},
    ],
    "cryptography": [
        {"kind": "course", "title": "Cryptopals challenges", "url": "https://cryptopals.com/", "provider": "Cryptopals"},
        {"kind": "book", "title": "A Graduate Course in Applied Cryptography (free PDF)", "url": "https://toc.cryptobook.us/", "provider": "Boneh & Shoup"},
    ],
    "cloud security": [
        {"kind": "docs", "title": "AWS Security Best Practices", "url": "https://docs.aws.amazon.com/security/", "provider": "AWS"},
    ],
    "incident response": [
        {"kind": "docs", "title": "NIST SP 800-61 — Incident Handling Guide (PDF)", "url": "https://csrc.nist.gov/pubs/sp/800/61/r2/final", "provider": "NIST"},
    ],
    "security tools": [
        {"kind": "docs", "title": "Nmap reference guide", "url": "https://nmap.org/book/man.html", "provider": "Nmap"},
        {"kind": "docs", "title": "Wireshark user guide", "url": "https://www.wireshark.org/docs/wsug_html_chunked/", "provider": "Wireshark"},
    ],

    # ----------------------------------------------------- design & mobile
    "design tools": [
        {"kind": "course", "title": "Figma — learn design", "url": "https://help.figma.com/hc/en-us/categories/360002051613", "provider": "Figma"},
        _youtube("Figma UI design tutorial"),
    ],
    "ui/ux design": [
        {"kind": "docs", "title": "Material Design 3 guidelines", "url": "https://m3.material.io/", "provider": "Google"},
        {"kind": "docs", "title": "Apple Human Interface Guidelines", "url": "https://developer.apple.com/design/human-interface-guidelines", "provider": "Apple"},
        {"kind": "course", "title": "Nielsen Norman Group — UX articles", "url": "https://www.nngroup.com/articles/", "provider": "NN/g"},
    ],
    "user research": [
        {"kind": "course", "title": "NN/g — user research articles", "url": "https://www.nngroup.com/topic/user-research/", "provider": "NN/g"},
    ],
    "prototyping": [
        {"kind": "course", "title": "Figma prototyping guide", "url": "https://help.figma.com/hc/en-us/articles/360040314193", "provider": "Figma"},
    ],
    "mobile ui/ux": [
        {"kind": "docs", "title": "Apple Human Interface Guidelines", "url": "https://developer.apple.com/design/human-interface-guidelines", "provider": "Apple"},
        {"kind": "docs", "title": "Material Design 3", "url": "https://m3.material.io/", "provider": "Google"},
    ],
    "react native": [
        {"kind": "docs", "title": "React Native — get started", "url": "https://reactnative.dev/docs/getting-started", "provider": "reactnative.dev"},
    ],
    "flutter": [
        {"kind": "docs", "title": "Flutter documentation", "url": "https://docs.flutter.dev/", "provider": "Google"},
    ],

    # ------------------------------------------------------------- other
    "game development": [
        {"kind": "docs", "title": "Unity Learn (free)", "url": "https://learn.unity.com/", "provider": "Unity"},
        {"kind": "docs", "title": "Godot documentation", "url": "https://docs.godotengine.org/en/stable/", "provider": "Godot"},
    ],
    "game design": [
        {"kind": "book", "title": "The Art of Game Design — companion site", "url": "https://www.schellgames.com/art-of-game-design", "provider": "Jesse Schell"},
        {"kind": "video", "title": "Game design analysis", "url": "https://www.youtube.com/results?search_query=game+makers+toolkit+game+design", "provider": "Game Maker's Toolkit"},
    ],
    "3d graphics": [
        {"kind": "book", "title": "Learn OpenGL (free online)", "url": "https://learnopengl.com/", "provider": "Joey de Vries"},
        {"kind": "docs", "title": "Three.js manual", "url": "https://threejs.org/manual/", "provider": "Three.js"},
    ],
    "blockchain": [
        {"kind": "docs", "title": "Ethereum developer docs", "url": "https://ethereum.org/en/developers/docs/", "provider": "ethereum.org"},
        {"kind": "course", "title": "CryptoZombies (interactive Solidity)", "url": "https://cryptozombies.io/", "provider": "Loom"},
    ],
    "automation": [
        {"kind": "book", "title": "Automate the Boring Stuff with Python (free)", "url": "https://automatetheboringstuff.com/", "provider": "Al Sweigart"},
    ],
    "selenium": [
        {"kind": "docs", "title": "Selenium documentation", "url": "https://www.selenium.dev/documentation/", "provider": "Selenium"},
    ],
    "architecture": [
        {"kind": "course", "title": "System Design Primer", "url": "https://github.com/donnemartin/system-design-primer", "provider": "Donne Martin"},
        {"kind": "docs", "title": "AWS Well-Architected Framework", "url": "https://aws.amazon.com/architecture/well-architected/", "provider": "AWS"},
    ],
    "communication": [
        {"kind": "docs", "title": "Google Technical Writing courses (free)", "url": "https://developers.google.com/tech-writing", "provider": "Google"},
    ],
    "agile": [
        {"kind": "docs", "title": "The Scrum Guide (free PDF)", "url": "https://scrumguides.org/", "provider": "Scrum.org"},
    ],
    "bug tracking": [
        {"kind": "docs", "title": "Jira — getting started", "url": "https://www.atlassian.com/software/jira/guides", "provider": "Atlassian"},
    ],
    "analytics": [
        {"kind": "course", "title": "Google Analytics Skillshop (free)", "url": "https://skillshop.withgoogle.com/", "provider": "Google"},
    ],
    "bi tools": [
        {"kind": "course", "title": "Power BI learning paths", "url": "https://learn.microsoft.com/en-us/training/powerplatform/power-bi", "provider": "Microsoft"},
    ],
    "data warehousing": [
        {"kind": "docs", "title": "dbt — docs & guides", "url": "https://docs.getdbt.com/", "provider": "dbt Labs"},
    ],
    "data pipelines": [
        {"kind": "course", "title": "Data Engineering Zoomcamp (free)", "url": "https://github.com/DataTalksClub/data-engineering-zoomcamp", "provider": "DataTalks.Club"},
    ],
    "cloud computing": [
        {"kind": "course", "title": "AWS Cloud Practitioner Essentials (free)", "url": "https://skillbuilder.aws/", "provider": "AWS"},
    ],
}


def _tokens(text: str) -> list[str]:
    """Lowercase word tokens, keeping +/# so c++ and c# survive."""
    return re.findall(r"[a-z0-9+#.]+", text.lower())


def get_resources_for_skill(skill: str) -> list[dict]:
    """
    Resources for one skill, best-effort.

    Exact match first. Otherwise the longest catalogue key whose whole tokens
    appear in the query wins — longest first, because a naive substring scan
    lets a one-letter key like "r" hijack "Ruby on Rails", and "c" hijack
    almost everything. Anything unmatched gets a generated search bundle
    rather than an empty list.
    """
    key = skill.strip().lower()
    if key in CATALOGUE:
        return CATALOGUE[key]

    query_tokens = set(_tokens(key))
    best = None
    for name in sorted(CATALOGUE, key=len, reverse=True):
        name_tokens = _tokens(name)
        if name_tokens and all(t in query_tokens for t in name_tokens):
            best = name
            break
    if best:
        return CATALOGUE[best]

    return [
        {
            "kind": "docs",
            "title": f"{skill} — search the web",
            "url": f"https://duckduckgo.com/?q={quote_plus(skill + ' official documentation')}",
            "provider": "Web search",
        },
        _youtube(f"{skill} tutorial"),
    ]


def get_resources_for_career(career: dict, per_skill: int = 3) -> dict:
    """
    Group resources by the skills a career requires.

    Each skill keeps at most `per_skill` entries, ordered docs → course →
    video → book, so the panel stays readable instead of dumping 60 links.
    """
    grouped = []
    seen_urls: set[str] = set()

    for skill in career.get("required_skills", []):
        items = sorted(
            get_resources_for_skill(skill),
            key=lambda r: KIND_ORDER.index(r["kind"]) if r["kind"] in KIND_ORDER else 99,
        )
        picked = []
        for item in items:
            # Do not repeat the same URL across skills within one career.
            if item["url"] in seen_urls:
                continue
            seen_urls.add(item["url"])
            picked.append(item)
            if len(picked) >= per_skill:
                break
        if picked:
            grouped.append({"skill": skill, "resources": picked})

    return {
        "career": career["title"],
        "career_id": career["id"],
        "total_resources": sum(len(g["resources"]) for g in grouped),
        "by_skill": grouped,
    }


# ---------------------------------------------------------------------------
# Second batch. Same editorial rules as above: exact canonical URLs for docs,
# books and courses; YouTube *searches* for video so nothing rots.
# ---------------------------------------------------------------------------

CATALOGUE.update({
    # ------------------------------------------------- systems languages
    "c++": [
        {"kind": "docs", "title": "cppreference — C++ reference", "url": "https://en.cppreference.com/w/cpp", "provider": "cppreference"},
        {"kind": "docs", "title": "C++ Core Guidelines", "url": "https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines", "provider": "Stroustrup & Sutter"},
        {"kind": "book", "title": "learncpp.com — full C++ course (free)", "url": "https://www.learncpp.com/", "provider": "learncpp.com"},
        _fcc("C++"),
        _youtube("modern C++ tutorial"),
    ],
    "c": [
        {"kind": "book", "title": "Beej's Guide to C Programming (free)", "url": "https://beej.us/guide/bgc/", "provider": "Brian Hall"},
        {"kind": "docs", "title": "C reference", "url": "https://en.cppreference.com/w/c", "provider": "cppreference"},
        {"kind": "course", "title": "CS50x — Introduction to Computer Science", "url": "https://cs50.harvard.edu/x/", "provider": "Harvard"},
    ],
    "rust programming": [
        {"kind": "book", "title": "The Rust Programming Language", "url": "https://doc.rust-lang.org/book/", "provider": "rust-lang.org"},
    ],
    "assembly": [
        {"kind": "book", "title": "Programming from the Ground Up (free)", "url": "https://savannah.nongnu.org/projects/pgubook/", "provider": "Jonathan Bartlett"},
    ],

    # ------------------------------------------------- other languages
    "r": [
        {"kind": "book", "title": "R for Data Science (free online)", "url": "https://r4ds.hadley.nz/", "provider": "Wickham & Grolemund"},
        {"kind": "docs", "title": "An Introduction to R (official)", "url": "https://cran.r-project.org/doc/manuals/r-release/R-intro.html", "provider": "CRAN"},
        {"kind": "book", "title": "Advanced R (free online)", "url": "https://adv-r.hadley.nz/", "provider": "Hadley Wickham"},
    ],
    "php": [
        {"kind": "docs", "title": "PHP Manual", "url": "https://www.php.net/manual/en/", "provider": "php.net"},
        {"kind": "course", "title": "PHP: The Right Way", "url": "https://phptherightway.com/", "provider": "Community"},
    ],
    "ruby": [
        {"kind": "docs", "title": "Ruby documentation", "url": "https://www.ruby-lang.org/en/documentation/", "provider": "ruby-lang.org"},
        {"kind": "book", "title": "Learn Ruby the Hard Way (free)", "url": "https://learnrubythehardway.org/book/", "provider": "Zed Shaw"},
    ],
    "scala": [
        {"kind": "docs", "title": "Scala 3 Book", "url": "https://docs.scala-lang.org/scala3/book/introduction.html", "provider": "scala-lang.org"},
    ],
    "dart": [
        {"kind": "docs", "title": "Dart language tour", "url": "https://dart.dev/language", "provider": "dart.dev"},
    ],
    "matlab": [
        {"kind": "course", "title": "MATLAB Onramp (free)", "url": "https://matlabacademy.mathworks.com/", "provider": "MathWorks"},
    ],
    "bash": [
        {"kind": "book", "title": "The Linux Command Line (free PDF)", "url": "https://linuxcommand.org/tlcl.php", "provider": "William Shotts"},
        {"kind": "docs", "title": "Bash Reference Manual", "url": "https://www.gnu.org/software/bash/manual/bash.html", "provider": "GNU"},
    ],
    "powershell": [
        {"kind": "docs", "title": "PowerShell documentation", "url": "https://learn.microsoft.com/en-us/powershell/", "provider": "Microsoft"},
    ],

    # ------------------------------------------------- web frameworks
    "express": [
        {"kind": "docs", "title": "Express guide", "url": "https://expressjs.com/en/guide/routing.html", "provider": "Express"},
    ],
    "webpack": [
        {"kind": "docs", "title": "Webpack concepts", "url": "https://webpack.js.org/concepts/", "provider": "webpack.js.org"},
    ],
    "firebase": [
        {"kind": "docs", "title": "Firebase documentation", "url": "https://firebase.google.com/docs", "provider": "Google"},
    ],
    "serverless": [
        {"kind": "docs", "title": "AWS Lambda developer guide", "url": "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html", "provider": "AWS"},
        {"kind": "docs", "title": "Serverless Framework docs", "url": "https://www.serverless.com/framework/docs", "provider": "Serverless Inc."},
    ],
    "design systems": [
        {"kind": "docs", "title": "Material Design 3", "url": "https://m3.material.io/", "provider": "Google"},
        {"kind": "book", "title": "Design Systems Handbook (free)", "url": "https://www.designbetter.co/design-systems-handbook", "provider": "InVision"},
    ],

    # ------------------------------------------------- mobile
    "android development": [
        {"kind": "docs", "title": "Android developer guides", "url": "https://developer.android.com/guide", "provider": "Google"},
        {"kind": "course", "title": "Android Basics with Compose (free)", "url": "https://developer.android.com/courses/android-basics-compose/course", "provider": "Google"},
    ],
    "ios development": [
        {"kind": "docs", "title": "Apple Developer documentation", "url": "https://developer.apple.com/documentation/", "provider": "Apple"},
        {"kind": "course", "title": "Develop in Swift tutorials", "url": "https://developer.apple.com/tutorials/develop-in-swift", "provider": "Apple"},
    ],

    # ------------------------------------------------- data engineering
    "apache spark": [
        {"kind": "docs", "title": "Spark SQL & DataFrames guide", "url": "https://spark.apache.org/docs/latest/sql-programming-guide.html", "provider": "Apache"},
    ],
    "hadoop": [
        {"kind": "docs", "title": "Apache Hadoop documentation", "url": "https://hadoop.apache.org/docs/stable/", "provider": "Apache"},
    ],
    "kafka": [
        {"kind": "docs", "title": "Apache Kafka documentation", "url": "https://kafka.apache.org/documentation/", "provider": "Apache"},
        {"kind": "course", "title": "Confluent Developer — Kafka courses", "url": "https://developer.confluent.io/courses/", "provider": "Confluent"},
    ],
    "data modeling": [
        {"kind": "book", "title": "The Data Warehouse Toolkit — Kimball techniques", "url": "https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/", "provider": "Kimball Group"},
    ],
    "business intelligence": [
        {"kind": "course", "title": "Power BI learning paths", "url": "https://learn.microsoft.com/en-us/training/powerplatform/power-bi", "provider": "Microsoft"},
    ],
    "power bi": [
        {"kind": "docs", "title": "Power BI documentation", "url": "https://learn.microsoft.com/en-us/power-bi/", "provider": "Microsoft"},
    ],
    "qlik": [
        {"kind": "course", "title": "Qlik free training", "url": "https://learning.qlik.com/", "provider": "Qlik"},
    ],
    "reporting": [
        {"kind": "course", "title": "Google Analytics Skillshop", "url": "https://skillshop.withgoogle.com/", "provider": "Google"},
    ],
    "a/b testing": [
        {"kind": "course", "title": "Trustworthy Online Controlled Experiments", "url": "https://experimentguide.com/", "provider": "Kohavi, Tang, Xu"},
        _youtube("A/B testing statistics explained"),
    ],

    # ------------------------------------------------- ML specifics
    "neural networks": [
        {"kind": "book", "title": "Neural Networks and Deep Learning (free)", "url": "http://neuralnetworksanddeeplearning.com/", "provider": "Michael Nielsen"},
        {"kind": "video", "title": "Neural networks — visual series", "url": "https://www.youtube.com/results?search_query=3blue1brown+neural+networks", "provider": "3Blue1Brown"},
    ],
    "transformers": [
        {"kind": "docs", "title": "Hugging Face Transformers docs", "url": "https://huggingface.co/docs/transformers/index", "provider": "Hugging Face"},
        {"kind": "docs", "title": "The Illustrated Transformer", "url": "https://jalammar.github.io/illustrated-transformer/", "provider": "Jay Alammar"},
    ],
    "bert": [
        {"kind": "docs", "title": "The Illustrated BERT", "url": "https://jalammar.github.io/illustrated-bert/", "provider": "Jay Alammar"},
    ],
    "gpt": [
        {"kind": "docs", "title": "OpenAI API documentation", "url": "https://platform.openai.com/docs", "provider": "OpenAI"},
        {"kind": "video", "title": "Build GPT from scratch", "url": "https://www.youtube.com/results?search_query=karpathy+let%27s+build+gpt", "provider": "Andrej Karpathy"},
    ],
    "hugging face": [
        {"kind": "course", "title": "Hugging Face course (free)", "url": "https://huggingface.co/learn", "provider": "Hugging Face"},
    ],
    "rnn": [
        {"kind": "docs", "title": "Understanding LSTM Networks", "url": "https://colah.github.io/posts/2015-08-Understanding-LSTMs/", "provider": "Christopher Olah"},
    ],
    "gan": [
        {"kind": "docs", "title": "Generative Adversarial Networks — TF tutorial", "url": "https://www.tensorflow.org/tutorials/generative/dcgan", "provider": "TensorFlow"},
    ],
    "transfer learning": [
        {"kind": "docs", "title": "Transfer learning guide", "url": "https://www.tensorflow.org/tutorials/images/transfer_learning", "provider": "TensorFlow"},
    ],
    "opencv": [
        {"kind": "docs", "title": "OpenCV-Python tutorials", "url": "https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html", "provider": "OpenCV"},
    ],
    "image classification": [
        {"kind": "course", "title": "CS231n — CNNs for Visual Recognition", "url": "https://cs231n.github.io/", "provider": "Stanford"},
    ],
    "yolo": [
        {"kind": "docs", "title": "Ultralytics YOLO docs", "url": "https://docs.ultralytics.com/", "provider": "Ultralytics"},
    ],
    "spacy": [
        {"kind": "course", "title": "Advanced NLP with spaCy (free course)", "url": "https://course.spacy.io/en/", "provider": "Explosion"},
        {"kind": "docs", "title": "spaCy usage docs", "url": "https://spacy.io/usage", "provider": "Explosion"},
    ],
    "nltk": [
        {"kind": "book", "title": "Natural Language Processing with Python (free)", "url": "https://www.nltk.org/book/", "provider": "NLTK"},
    ],
    "text processing": [
        {"kind": "docs", "title": "Python re — regular expressions", "url": "https://docs.python.org/3/howto/regex.html", "provider": "python.org"},
        {"kind": "course", "title": "RegexOne — interactive regex", "url": "https://regexone.com/", "provider": "RegexOne"},
    ],
    "aws sagemaker": [
        {"kind": "docs", "title": "Amazon SageMaker developer guide", "url": "https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html", "provider": "AWS"},
    ],
    "kubeflow": [
        {"kind": "docs", "title": "Kubeflow documentation", "url": "https://www.kubeflow.org/docs/", "provider": "Kubeflow"},
    ],
    "gpu computing": [
        {"kind": "docs", "title": "CUDA C++ Programming Guide", "url": "https://docs.nvidia.com/cuda/cuda-c-programming-guide/", "provider": "NVIDIA"},
    ],
    "research papers": [
        {"kind": "docs", "title": "arXiv — cs.LG preprints", "url": "https://arxiv.org/list/cs.LG/recent", "provider": "arXiv"},
        {"kind": "docs", "title": "Papers with Code", "url": "https://paperswithcode.com/", "provider": "Papers with Code"},
    ],
    "research": [
        {"kind": "docs", "title": "Papers with Code", "url": "https://paperswithcode.com/", "provider": "Papers with Code"},
        {"kind": "docs", "title": "Distill — explaining machine learning", "url": "https://distill.pub/", "provider": "Distill"},
    ],
    "publications": [
        {"kind": "docs", "title": "How to write a great research paper", "url": "https://www.microsoft.com/en-us/research/academic-program/write-great-research-paper/", "provider": "Simon Peyton Jones"},
    ],

    # ------------------------------------------------- devops / infra
    "jenkins": [
        {"kind": "docs", "title": "Jenkins user documentation", "url": "https://www.jenkins.io/doc/", "provider": "Jenkins"},
    ],
    "gitlab ci": [
        {"kind": "docs", "title": "GitLab CI/CD documentation", "url": "https://docs.gitlab.com/ee/ci/", "provider": "GitLab"},
    ],
    "ansible": [
        {"kind": "docs", "title": "Ansible documentation", "url": "https://docs.ansible.com/ansible/latest/", "provider": "Red Hat"},
    ],
    "cloudformation": [
        {"kind": "docs", "title": "AWS CloudFormation user guide", "url": "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html", "provider": "AWS"},
    ],
    "prometheus": [
        {"kind": "docs", "title": "Prometheus documentation", "url": "https://prometheus.io/docs/introduction/overview/", "provider": "Prometheus"},
    ],
    "grafana": [
        {"kind": "docs", "title": "Grafana documentation", "url": "https://grafana.com/docs/grafana/latest/", "provider": "Grafana Labs"},
    ],
    "sre": [
        {"kind": "book", "title": "Site Reliability Engineering (free online)", "url": "https://sre.google/sre-book/table-of-contents/", "provider": "Google"},
        {"kind": "book", "title": "The SRE Workbook (free online)", "url": "https://sre.google/workbook/table-of-contents/", "provider": "Google"},
    ],

    # ------------------------------------------------- security
    "owasp": [
        {"kind": "docs", "title": "OWASP Top 10", "url": "https://owasp.org/www-project-top-ten/", "provider": "OWASP"},
        {"kind": "docs", "title": "OWASP Cheat Sheet Series", "url": "https://cheatsheetseries.owasp.org/", "provider": "OWASP"},
    ],
    "network security": [
        {"kind": "docs", "title": "Nmap Network Scanning guide", "url": "https://nmap.org/book/", "provider": "Gordon Lyon"},
        {"kind": "course", "title": "TryHackMe — networking paths", "url": "https://tryhackme.com/", "provider": "TryHackMe"},
    ],
    "firewalls": [
        {"kind": "docs", "title": "nftables wiki", "url": "https://wiki.nftables.org/", "provider": "Netfilter"},
    ],
    "encryption": [
        {"kind": "course", "title": "Cryptopals crypto challenges", "url": "https://cryptopals.com/", "provider": "Cryptopals"},
        {"kind": "book", "title": "Crypto 101 (free PDF)", "url": "https://www.crypto101.io/", "provider": "Laurens Van Houtven"},
    ],
    "metasploit": [
        {"kind": "docs", "title": "Metasploit documentation", "url": "https://docs.metasploit.com/", "provider": "Rapid7"},
    ],
    "kali linux": [
        {"kind": "docs", "title": "Kali Linux documentation", "url": "https://www.kali.org/docs/", "provider": "Offensive Security"},
    ],
    "siem": [
        {"kind": "docs", "title": "Elastic Security documentation", "url": "https://www.elastic.co/guide/en/security/current/index.html", "provider": "Elastic"},
    ],
    "vulnerability assessment": [
        {"kind": "docs", "title": "NIST National Vulnerability Database", "url": "https://nvd.nist.gov/", "provider": "NIST"},
        {"kind": "docs", "title": "CVE Program", "url": "https://www.cve.org/", "provider": "MITRE"},
    ],
    "risk assessment": [
        {"kind": "docs", "title": "NIST SP 800-30 — Risk Assessments", "url": "https://csrc.nist.gov/pubs/sp/800/30/r1/final", "provider": "NIST"},
    ],
    "compliance": [
        {"kind": "docs", "title": "NIST Cybersecurity Framework", "url": "https://www.nist.gov/cyberframework", "provider": "NIST"},
    ],

    # ------------------------------------------------- testing / QA
    "testing": [
        {"kind": "docs", "title": "Google Testing Blog", "url": "https://testing.googleblog.com/", "provider": "Google"},
        {"kind": "docs", "title": "pytest documentation", "url": "https://docs.pytest.org/en/stable/", "provider": "pytest"},
    ],
    "test automation": [
        {"kind": "docs", "title": "Playwright documentation", "url": "https://playwright.dev/docs/intro", "provider": "Microsoft"},
        {"kind": "docs", "title": "Selenium documentation", "url": "https://www.selenium.dev/documentation/", "provider": "Selenium"},
    ],
    "api testing": [
        {"kind": "course", "title": "Postman Learning Center", "url": "https://learning.postman.com/", "provider": "Postman"},
    ],
    "performance testing": [
        {"kind": "docs", "title": "k6 documentation", "url": "https://grafana.com/docs/k6/latest/", "provider": "Grafana Labs"},
    ],
    "cypress": [
        {"kind": "docs", "title": "Cypress documentation", "url": "https://docs.cypress.io/", "provider": "Cypress"},
    ],
    "jest": [
        {"kind": "docs", "title": "Jest documentation", "url": "https://jestjs.io/docs/getting-started", "provider": "Jest"},
    ],
    "qa": [
        {"kind": "docs", "title": "Ministry of Testing — resources", "url": "https://www.ministryoftesting.com/", "provider": "Ministry of Testing"},
    ],
    "test planning": [
        {"kind": "docs", "title": "ISTQB syllabi (free PDFs)", "url": "https://www.istqb.org/certifications/certified-tester-foundation-level", "provider": "ISTQB"},
    ],

    # ------------------------------------------------- design tools
    "figma": [
        {"kind": "course", "title": "Figma learn & help centre", "url": "https://help.figma.com/hc/en-us", "provider": "Figma"},
        _youtube("Figma tutorial for beginners"),
    ],
    "sketch": [
        {"kind": "docs", "title": "Sketch documentation", "url": "https://www.sketch.com/docs/", "provider": "Sketch"},
    ],
    "adobe xd": [
        {"kind": "course", "title": "Adobe XD tutorials", "url": "https://helpx.adobe.com/xd/tutorials.html", "provider": "Adobe"},
    ],
    "ui design": [
        {"kind": "docs", "title": "Refactoring UI — tips", "url": "https://www.refactoringui.com/", "provider": "Wathan & Schoger"},
        {"kind": "docs", "title": "Material Design 3", "url": "https://m3.material.io/", "provider": "Google"},
    ],
    "ux design": [
        {"kind": "course", "title": "NN/g UX articles", "url": "https://www.nngroup.com/articles/", "provider": "NN/g"},
        {"kind": "course", "title": "Google UX Design basics", "url": "https://grow.google/certificates/ux-design/", "provider": "Google"},
    ],
    "user testing": [
        {"kind": "course", "title": "NN/g — usability testing", "url": "https://www.nngroup.com/topic/usability-testing/", "provider": "NN/g"},
    ],
    "animation": [
        {"kind": "docs", "title": "web.dev — Animations", "url": "https://web.dev/learn/css/animations/", "provider": "Google"},
        {"kind": "docs", "title": "GSAP documentation", "url": "https://gsap.com/docs/v3/", "provider": "GreenSock"},
    ],

    # ------------------------------------------------- game dev
    "unity": [
        {"kind": "course", "title": "Unity Learn (free)", "url": "https://learn.unity.com/", "provider": "Unity"},
    ],
    "unreal engine": [
        {"kind": "course", "title": "Unreal Engine learning", "url": "https://dev.epicgames.com/community/unreal-engine/learning", "provider": "Epic Games"},
    ],
    "game physics": [
        {"kind": "book", "title": "Game Physics Engine Development — notes", "url": "https://gafferongames.com/categories/game-physics/", "provider": "Glenn Fiedler"},
    ],
    "multiplayer": [
        {"kind": "docs", "title": "Networked physics & netcode articles", "url": "https://gafferongames.com/categories/networked-physics/", "provider": "Glenn Fiedler"},
    ],
    "vr/ar": [
        {"kind": "docs", "title": "WebXR Device API", "url": "https://immersiveweb.dev/", "provider": "Immersive Web"},
        {"kind": "docs", "title": "Unity XR documentation", "url": "https://docs.unity3d.com/Manual/XR.html", "provider": "Unity"},
    ],

    # ------------------------------------------------- web3
    "solidity": [
        {"kind": "docs", "title": "Solidity documentation", "url": "https://docs.soliditylang.org/", "provider": "Solidity"},
        {"kind": "course", "title": "CryptoZombies (interactive)", "url": "https://cryptozombies.io/", "provider": "Loom"},
    ],
    "smart contracts": [
        {"kind": "docs", "title": "OpenZeppelin Contracts docs", "url": "https://docs.openzeppelin.com/contracts/", "provider": "OpenZeppelin"},
    ],
    "ethereum": [
        {"kind": "docs", "title": "Ethereum developer docs", "url": "https://ethereum.org/en/developers/docs/", "provider": "ethereum.org"},
    ],
    "web3": [
        {"kind": "docs", "title": "ethers.js documentation", "url": "https://docs.ethers.org/", "provider": "ethers.js"},
    ],
    "hardhat": [
        {"kind": "docs", "title": "Hardhat documentation", "url": "https://hardhat.org/docs", "provider": "Nomic Foundation"},
    ],
    "truffle": [
        {"kind": "docs", "title": "Truffle Suite documentation", "url": "https://archive.trufflesuite.com/docs/", "provider": "ConsenSys"},
    ],
    "defi": [
        {"kind": "docs", "title": "Ethereum — DeFi overview", "url": "https://ethereum.org/en/defi/", "provider": "ethereum.org"},
    ],
    "nft": [
        {"kind": "docs", "title": "ERC-721 standard", "url": "https://eips.ethereum.org/EIPS/eip-721", "provider": "Ethereum"},
    ],

    # ------------------------------------------------- product / process
    "product management": [
        {"kind": "docs", "title": "Lenny's Newsletter — PM resources", "url": "https://www.lennysnewsletter.com/", "provider": "Lenny Rachitsky"},
        {"kind": "book", "title": "Shape Up (free online)", "url": "https://basecamp.com/shapeup", "provider": "Basecamp"},
    ],
    "roadmapping": [
        {"kind": "book", "title": "Shape Up — betting & scoping", "url": "https://basecamp.com/shapeup", "provider": "Basecamp"},
    ],
    "user stories": [
        {"kind": "docs", "title": "User stories — guide", "url": "https://www.atlassian.com/agile/project-management/user-stories", "provider": "Atlassian"},
    ],
    "scrum": [
        {"kind": "docs", "title": "The Scrum Guide (free PDF)", "url": "https://scrumguides.org/", "provider": "Scrum.org"},
    ],
    "stakeholder management": [
        {"kind": "docs", "title": "Atlassian Agile coach", "url": "https://www.atlassian.com/agile", "provider": "Atlassian"},
    ],
    "strategy": [
        {"kind": "book", "title": "Good Strategy / Bad Strategy — summary", "url": "https://hbr.org/2011/06/the-perils-of-bad-strategy", "provider": "HBR"},
    ],
    "certifications": [
        {"kind": "docs", "title": "AWS certification paths", "url": "https://aws.amazon.com/certification/", "provider": "AWS"},
        {"kind": "docs", "title": "Microsoft certifications", "url": "https://learn.microsoft.com/en-us/credentials/", "provider": "Microsoft"},
    ],
    "phd": [
        {"kind": "docs", "title": "How to write a great research paper", "url": "https://www.microsoft.com/en-us/research/academic-program/write-great-research-paper/", "provider": "Simon Peyton Jones"},
    ],
    "ssas": [
        {"kind": "docs", "title": "SQL Server Analysis Services docs", "url": "https://learn.microsoft.com/en-us/analysis-services/", "provider": "Microsoft"},
    ],
})
