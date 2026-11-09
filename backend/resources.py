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
        _fcc("Java"),
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


def get_resources_for_skill(skill: str) -> list[dict]:
    """
    Resources for one skill, best-effort.

    Exact match first, then a loose containment match so "Machine Learning
    Basics" still finds "machine learning". Anything unmatched gets a
    generated search bundle rather than an empty list.
    """
    key = skill.strip().lower()
    if key in CATALOGUE:
        return CATALOGUE[key]

    for name, items in CATALOGUE.items():
        if name in key or key in name:
            return items

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
