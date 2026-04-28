from sqlmodel import Session, SQLModel, select

from auth import hash_password
from database import engine
from models import Company, Job, Tag, User, UserProfile


JOB_SEEKERS = [
    {
        "username": "aisha_rahman",
        "email": "aisha.rahman@example.com",
        "password": "Aisha@2026",
        "profile": {
            "full_name": "Aisha Rahman",
            "phone": "+1-416-555-0137",
            "location": "Toronto, Canada",
            "bio": "Backend engineer who builds reliable APIs for healthcare and civic products.",
            "skills": "Python, FastAPI, PostgreSQL, Docker, Redis, API design, testing",
            "experience": "4 years building REST APIs, payment integrations, and queue-based services.",
            "education": "BSc Computer Science, University of Toronto",
        },
    },
    {
        "username": "miguel_santos",
        "email": "miguel.santos@example.com",
        "password": "Miguel@2026",
        "profile": {
            "full_name": "Miguel Santos",
            "phone": "+55-11-5555-0198",
            "location": "Sao Paulo, Brazil",
            "bio": "Data analyst focused on marketplace growth, retention, and operational dashboards.",
            "skills": "SQL, Python, pandas, Tableau, Looker, dbt, cohort analysis",
            "experience": "5 years translating product and sales data into executive reporting.",
            "education": "BA Economics, Universidade de Sao Paulo",
        },
    },
    {
        "username": "mei_lin",
        "email": "mei.lin@example.com",
        "password": "Mei@2026",
        "profile": {
            "full_name": "Mei Lin",
            "phone": "+65-5555-0144",
            "location": "Singapore",
            "bio": "Frontend engineer who enjoys accessible, high-performance interfaces for fintech teams.",
            "skills": "React, TypeScript, Next.js, CSS, accessibility, Playwright, design systems",
            "experience": "3 years shipping dashboards, onboarding flows, and component libraries.",
            "education": "Diploma in Software Engineering, Nanyang Polytechnic",
        },
    },
    {
        "username": "kwame_mensah",
        "email": "kwame.mensah@example.com",
        "password": "Kwame@2026",
        "profile": {
            "full_name": "Kwame Mensah",
            "phone": "+233-30-555-0162",
            "location": "Accra, Ghana",
            "bio": "Cloud engineer helping startups build secure, observable infrastructure.",
            "skills": "AWS, Terraform, Kubernetes, Linux, CI/CD, monitoring, incident response",
            "experience": "6 years managing production cloud platforms and release automation.",
            "education": "BEng Computer Engineering, University of Ghana",
        },
    },
    {
        "username": "sofia_kowalska",
        "email": "sofia.kowalska@example.com",
        "password": "Sofia@2026",
        "profile": {
            "full_name": "Sofia Kowalska",
            "phone": "+48-22-555-0181",
            "location": "Warsaw, Poland",
            "bio": "UX researcher with a strong habit of turning messy interviews into crisp product decisions.",
            "skills": "User interviews, usability testing, Figma, journey mapping, research synthesis",
            "experience": "4 years researching SaaS workflows, developer tools, and public-sector services.",
            "education": "MA Human-Computer Interaction, University of Warsaw",
        },
    },
    {
        "username": "omar_haddad",
        "email": "omar.haddad@example.com",
        "password": "Omar@2026",
        "profile": {
            "full_name": "Omar Haddad",
            "phone": "+971-4-555-0150",
            "location": "Dubai, UAE",
            "bio": "Product manager for logistics and commerce platforms with a bias toward measurable outcomes.",
            "skills": "Product strategy, roadmapping, analytics, stakeholder management, agile delivery",
            "experience": "7 years launching B2B products across supply chain, retail, and payments.",
            "education": "MBA, American University in Dubai",
        },
    },
    {
        "username": "elena_garcia",
        "email": "elena.garcia@example.com",
        "password": "Elena@2026",
        "profile": {
            "full_name": "Elena Garcia",
            "phone": "+34-91-555-0177",
            "location": "Madrid, Spain",
            "bio": "Machine learning engineer building multilingual NLP systems and model evaluation pipelines.",
            "skills": "Python, PyTorch, NLP, vector search, MLflow, evaluation, data labeling",
            "experience": "5 years delivering search, classification, and recommendation systems.",
            "education": "MSc Artificial Intelligence, Universidad Politecnica de Madrid",
        },
    },
    {
        "username": "arjun_iyer",
        "email": "arjun.iyer@example.com",
        "password": "Arjun@2026",
        "profile": {
            "full_name": "Arjun Iyer",
            "phone": "+91-80-5555-0126",
            "location": "Bengaluru, India",
            "bio": "Mobile engineer who ships polished Android and cross-platform experiences for consumer apps.",
            "skills": "Kotlin, Android, Flutter, Firebase, GraphQL, mobile performance, release management",
            "experience": "4 years building booking, learning, and payments apps for high-growth products.",
            "education": "BTech Information Technology, PES University",
        },
    },
]


RECRUITERS = [
    {"username": "priya_nair", "email": "priya.nair@recruiter.example.com", "password": "Priya@2026"},
    {"username": "james_okafor", "email": "james.okafor@recruiter.example.com", "password": "James@2026"},
    {"username": "hana_kim", "email": "hana.kim@recruiter.example.com", "password": "Hana@2026"},
    {"username": "lucas_moreau", "email": "lucas.moreau@recruiter.example.com", "password": "Lucas@2026"},
    {"username": "fatima_al_zahra", "email": "fatima.alzahra@recruiter.example.com", "password": "Fatima@2026"},
    {"username": "noah_williams", "email": "noah.williams@recruiter.example.com", "password": "Noah@2026"},
    {"username": "anika_bose", "email": "anika.bose@recruiter.example.com", "password": "Anika@2026"},
    {"username": "diego_morales", "email": "diego.morales@recruiter.example.com", "password": "Diego@2026"},
]


COMPANIES = [
    {
        "name": "Nimbus HealthTech",
        "description": "Cloud software for patient engagement, clinic operations, and healthcare compliance.",
        "location": "Boston, USA",
        "website": "https://nimbushealthtech.example.com",
    },
    {
        "name": "GreenGrid Energy",
        "description": "Renewable energy analytics platform for distributed solar, batteries, and grid forecasting.",
        "location": "Berlin, Germany",
        "website": "https://greengridenergy.example.com",
    },
    {
        "name": "Kairo FinLabs",
        "description": "Payments intelligence company building fraud detection and credit products for emerging markets.",
        "location": "Nairobi, Kenya",
        "website": "https://kairofinlabs.example.com",
    },
    {
        "name": "Aurora Learn",
        "description": "Adaptive learning platform for schools, language programs, and workforce training.",
        "location": "Melbourne, Australia",
        "website": "https://auroralearn.example.com",
    },
    {
        "name": "BlueHarbor Logistics",
        "description": "Logistics orchestration tools for ports, freight forwarders, and last-mile delivery teams.",
        "location": "Rotterdam, Netherlands",
        "website": "https://blueharborlogistics.example.com",
    },
    {
        "name": "Saffron AI Labs",
        "description": "Applied AI studio creating multilingual assistants and retrieval systems for enterprises.",
        "location": "Bengaluru, India",
        "website": "https://saffronailabs.example.com",
    },
    {
        "name": "Atlas Remote Works",
        "description": "Remote-work platform for global hiring, payroll, compliance, and team operations.",
        "location": "Lisbon, Portugal",
        "website": "https://atlasremoteworks.example.com",
    },
    {
        "name": "Cedar Cyber Defense",
        "description": "Security operations and threat detection software for mid-market companies.",
        "location": "Tel Aviv, Israel",
        "website": "https://cedarcyberdefense.example.com",
    },
    {
        "name": "Mosaic Retail Cloud",
        "description": "Retail commerce suite for inventory planning, store operations, and customer loyalty.",
        "location": "Mexico City, Mexico",
        "website": "https://mosaicretailcloud.example.com",
    },
    {
        "name": "PolarWave Robotics",
        "description": "Robotics company building autonomous inspection systems for cold-chain and industrial sites.",
        "location": "Reykjavik, Iceland",
        "website": "https://polarwaverobotics.example.com",
    },
]


JOBS = [
    ("Nimbus HealthTech", "Backend API Engineer", "Build secure FastAPI services for appointment, billing, and care-team workflows.", "Boston, USA", 122000, True, ["python", "fastapi", "postgresql", "healthtech"]),
    ("Nimbus HealthTech", "Healthcare Data Integration Specialist", "Connect EHR, claims, and scheduling data pipelines with quality checks.", "Remote - USA", 112000, True, ["hl7", "fhir", "etl", "sql"]),
    ("Nimbus HealthTech", "Compliance Product Manager", "Own HIPAA-ready product requirements and audit-friendly release practices.", "Boston, USA", 135000, False, ["product", "compliance", "healthcare", "analytics"]),
    ("Nimbus HealthTech", "Patient Experience UX Designer", "Design accessible care journeys for patients, coordinators, and clinicians.", "Toronto, Canada", 98000, True, ["ux", "figma", "accessibility", "research"]),
    ("Nimbus HealthTech", "Site Reliability Engineer", "Improve uptime, observability, and deployment safety for clinical SaaS systems.", "Remote - North America", 145000, True, ["sre", "kubernetes", "terraform", "observability"]),
    ("GreenGrid Energy", "Renewable Energy Software Engineer", "Develop APIs that forecast solar generation and battery dispatch.", "Berlin, Germany", 105000, False, ["python", "iot", "energy", "cloud"]),
    ("GreenGrid Energy", "Grid Forecasting Data Scientist", "Model load, weather, and battery behavior for utility-scale planning.", "Munich, Germany", 118000, True, ["machine-learning", "forecasting", "python", "energy"]),
    ("GreenGrid Energy", "IoT Platform Engineer", "Scale device ingestion and telemetry pipelines for distributed energy assets.", "Remote - Europe", 110000, True, ["iot", "kafka", "golang", "timeseries"]),
    ("GreenGrid Energy", "Climate Partnerships Lead", "Grow partnerships with cities, utilities, and renewable infrastructure operators.", "Berlin, Germany", 99000, False, ["partnerships", "climate", "sales", "strategy"]),
    ("Kairo FinLabs", "Fraud Detection Machine Learning Engineer", "Build anomaly detection systems for card, wallet, and bank transfer fraud.", "Nairobi, Kenya", 96000, True, ["python", "ml", "fraud", "payments"]),
    ("Kairo FinLabs", "Senior Payments Backend Developer", "Own ledger, settlement, and reconciliation services for high-volume payments.", "Lagos, Nigeria", 102000, True, ["java", "postgresql", "payments", "microservices"]),
    ("Kairo FinLabs", "Credit Risk Analyst", "Create risk scorecards and portfolio dashboards for small-business lending.", "Nairobi, Kenya", 78000, False, ["sql", "risk", "analytics", "credit"]),
    ("Kairo FinLabs", "Mobile Wallet QA Engineer", "Test wallet flows across Android devices, networks, and payment providers.", "Accra, Ghana", 64000, True, ["qa", "android", "payments", "automation"]),
    ("Aurora Learn", "Adaptive Learning Frontend Engineer", "Craft student and teacher interfaces with accessible React components.", "Melbourne, Australia", 108000, True, ["react", "typescript", "accessibility", "edtech"]),
    ("Aurora Learn", "Learning Experience Designer", "Create evidence-based courses, assessments, and learning loops.", "Sydney, Australia", 88000, False, ["instructional-design", "ux", "education", "content"]),
    ("Aurora Learn", "Education Data Analyst", "Measure engagement, mastery, and intervention outcomes for school programs.", "Remote - APAC", 82000, True, ["sql", "tableau", "education", "analytics"]),
    ("Aurora Learn", "Backend Engineer for Assessment Systems", "Build scalable grading, rubric, and personalized feedback services.", "Melbourne, Australia", 112000, False, ["python", "django", "postgresql", "edtech"]),
    ("BlueHarbor Logistics", "Logistics Optimization Engineer", "Design routing and scheduling algorithms for multimodal freight operations.", "Rotterdam, Netherlands", 116000, False, ["optimization", "python", "logistics", "algorithms"]),
    ("BlueHarbor Logistics", "Supply Chain Product Analyst", "Analyze port, warehouse, and carrier data to improve delivery reliability.", "Remote - Europe", 89000, True, ["sql", "supply-chain", "analytics", "product"]),
    ("BlueHarbor Logistics", "Freight Platform Backend Engineer", "Build APIs for shipment tracking, customs documents, and partner integrations.", "Rotterdam, Netherlands", 109000, False, ["node.js", "apis", "logistics", "postgresql"]),
    ("BlueHarbor Logistics", "Customer Success Manager - Enterprise Logistics", "Guide enterprise freight customers through onboarding, adoption, and expansion.", "Dubai, UAE", 92000, True, ["customer-success", "logistics", "enterprise", "saas"]),
    ("BlueHarbor Logistics", "Data Engineering Manager", "Lead the team building clean, reliable freight and telemetry data models.", "Amsterdam, Netherlands", 142000, False, ["data-engineering", "leadership", "dbt", "airflow"]),
    ("Saffron AI Labs", "LLM Application Engineer", "Build retrieval-augmented assistants for enterprise knowledge workflows.", "Bengaluru, India", 78000, True, ["llm", "rag", "python", "vector-search"]),
    ("Saffron AI Labs", "Multilingual NLP Research Engineer", "Improve evaluation, tokenization, and language coverage for production NLP systems.", "Hyderabad, India", 92000, True, ["nlp", "pytorch", "evaluation", "research"]),
    ("Saffron AI Labs", "AI Product Designer", "Design trustworthy AI workflows for analysts, support agents, and managers.", "Bengaluru, India", 76000, False, ["product-design", "ai", "ux", "figma"]),
    ("Saffron AI Labs", "MLOps Engineer", "Automate model deployment, monitoring, and feedback loops for client projects.", "Remote - India", 86000, True, ["mlops", "kubernetes", "mlflow", "python"]),
    ("Saffron AI Labs", "Technical AI Program Manager", "Coordinate client delivery across data science, engineering, and security teams.", "Mumbai, India", 84000, True, ["program-management", "ai", "delivery", "stakeholders"]),
    ("Atlas Remote Works", "Global Payroll Operations Specialist", "Manage payroll workflows across countries, currencies, and compliance rules.", "Lisbon, Portugal", 74000, True, ["payroll", "operations", "compliance", "hrtech"]),
    ("Atlas Remote Works", "Distributed Systems Engineer", "Build resilient services for hiring, contracts, payroll, and country operations.", "Remote - Worldwide", 128000, True, ["distributed-systems", "golang", "postgresql", "saas"]),
    ("Atlas Remote Works", "Employment Compliance Counsel", "Advise product and operations teams on global employment compliance.", "London, UK", 132000, True, ["legal", "employment", "compliance", "hrtech"]),
    ("Atlas Remote Works", "Growth Marketing Analyst", "Run funnel analysis, attribution experiments, and lifecycle campaign reporting.", "Remote - EMEA", 81000, True, ["marketing", "analytics", "sql", "experimentation"]),
    ("Cedar Cyber Defense", "Security Operations Analyst", "Investigate alerts, tune detections, and document response playbooks.", "Tel Aviv, Israel", 98000, False, ["security", "soc", "siem", "incident-response"]),
    ("Cedar Cyber Defense", "Threat Detection Engineer", "Create detections for cloud, identity, endpoint, and network signals.", "Remote - Europe", 124000, True, ["detection", "python", "security", "cloud"]),
    ("Cedar Cyber Defense", "Cloud Security Architect", "Design secure cloud baselines and advisory patterns for customer environments.", "Prague, Czech Republic", 138000, True, ["aws", "azure", "security", "architecture"]),
    ("Cedar Cyber Defense", "Security Technical Writer", "Write clear detection guides, release notes, and analyst education content.", "Remote - Worldwide", 79000, True, ["technical-writing", "security", "docs", "training"]),
    ("Cedar Cyber Defense", "Detection Platform Backend Engineer", "Build high-throughput ingestion and query services for security events.", "Tel Aviv, Israel", 131000, False, ["backend", "kafka", "security", "go"]),
    ("Mosaic Retail Cloud", "Retail Inventory Data Scientist", "Forecast demand and replenishment needs across stores, channels, and seasons.", "Mexico City, Mexico", 91000, True, ["data-science", "forecasting", "retail", "python"]),
    ("Mosaic Retail Cloud", "Commerce Platform Engineer", "Build catalog, cart, promotion, and loyalty services for omnichannel retail.", "Guadalajara, Mexico", 97000, False, ["backend", "commerce", "node.js", "postgresql"]),
    ("Mosaic Retail Cloud", "Store Operations Implementation Consultant", "Help retailers launch workflows for inventory, returns, and staff operations.", "Bogota, Colombia", 72000, True, ["implementation", "retail", "consulting", "saas"]),
    ("Mosaic Retail Cloud", "Customer Loyalty Product Manager", "Own loyalty, offers, and personalization features for regional retailers.", "Mexico City, Mexico", 104000, False, ["product", "retail", "loyalty", "analytics"]),
    ("PolarWave Robotics", "Robotics Perception Engineer", "Develop perception models for autonomous inspection in harsh industrial environments.", "Reykjavik, Iceland", 119000, False, ["robotics", "computer-vision", "python", "ros"]),
    ("PolarWave Robotics", "Embedded Systems Developer", "Build firmware and sensor integrations for robotic inspection platforms.", "Oslo, Norway", 111000, False, ["embedded", "c++", "sensors", "robotics"]),
    ("PolarWave Robotics", "Field Robotics QA Lead", "Plan field testing, reliability metrics, and validation for autonomous robots.", "Reykjavik, Iceland", 99000, False, ["qa", "robotics", "field-testing", "hardware"]),
    ("PolarWave Robotics", "Industrial Partnerships Manager", "Develop partnerships with logistics, manufacturing, and cold-chain operators.", "Copenhagen, Denmark", 94000, True, ["partnerships", "robotics", "sales", "industrial"]),
    ("PolarWave Robotics", "Robotics Cloud Telemetry Engineer", "Build cloud pipelines for robot health, mission logs, and fleet diagnostics.", "Remote - Europe", 115000, True, ["cloud", "iot", "telemetry", "robotics"]),
    ("Atlas Remote Works", "People Analytics Engineer", "Model workforce data and build trusted analytics for distributed teams.", "Remote - Worldwide", 103000, True, ["analytics-engineering", "dbt", "hrtech", "sql"]),
    ("GreenGrid Energy", "Energy Market Data Engineer", "Maintain pipelines for market prices, weather feeds, and grid constraints.", "Remote - Europe", 107000, True, ["data-engineering", "airflow", "energy", "python"]),
    ("Aurora Learn", "Mobile Learning App Engineer", "Build offline-first learning experiences for Android and iOS students.", "Remote - APAC", 99000, True, ["mobile", "flutter", "firebase", "edtech"]),
]


JOB_SEEKERS.extend([
    {
        "username": "leila_benkirane",
        "email": "leila.benkirane@example.com",
        "password": "Leila@2026",
        "profile": {
            "full_name": "Leila Benkirane",
            "phone": "+212-522-555-018",
            "location": "Casablanca, Morocco",
            "bio": "Cybersecurity analyst focused on identity security, audit readiness, and practical risk reduction.",
            "skills": "SIEM, IAM, risk assessment, ISO 27001, Python scripting, vulnerability management",
            "experience": "5 years supporting security operations and compliance programs for financial services teams.",
            "education": "MSc Cybersecurity, Mohammed V University",
        },
    },
    {
        "username": "tomasz_nowak",
        "email": "tomasz.nowak@example.com",
        "password": "Tomasz@2026",
        "profile": {
            "full_name": "Tomasz Nowak",
            "phone": "+48-12-555-0142",
            "location": "Krakow, Poland",
            "bio": "Robotics software engineer who enjoys navigation, sensor fusion, and dependable field deployments.",
            "skills": "C++, ROS, SLAM, sensor fusion, Linux, robotics testing, simulation",
            "experience": "6 years developing autonomous navigation and controls software for industrial robots.",
            "education": "MEng Robotics, AGH University of Science and Technology",
        },
    },
    {
        "username": "nadia_petrov",
        "email": "nadia.petrov@example.com",
        "password": "Nadia@2026",
        "profile": {
            "full_name": "Nadia Petrov",
            "phone": "+359-2-555-0173",
            "location": "Sofia, Bulgaria",
            "bio": "Technical writer who turns complex developer platforms into clear docs, tutorials, and release notes.",
            "skills": "Technical writing, API docs, Markdown, OpenAPI, developer education, docs-as-code",
            "experience": "7 years documenting cloud APIs, SDKs, observability tools, and migration guides.",
            "education": "BA Linguistics, Sofia University",
        },
    },
    {
        "username": "kenji_watanabe",
        "email": "kenji.watanabe@example.com",
        "password": "Kenji@2026",
        "profile": {
            "full_name": "Kenji Watanabe",
            "phone": "+81-3-5555-0128",
            "location": "Tokyo, Japan",
            "bio": "DevOps engineer specializing in regulated infrastructure, cost control, and delivery automation.",
            "skills": "AWS, GitHub Actions, Terraform, Kubernetes, FinOps, observability, incident response",
            "experience": "8 years running cloud platforms for fintech, manufacturing, and public-sector software.",
            "education": "BSc Information Systems, Waseda University",
        },
    },
    {
        "username": "isabella_rossi",
        "email": "isabella.rossi@example.com",
        "password": "Isabella@2026",
        "profile": {
            "full_name": "Isabella Rossi",
            "phone": "+39-06-555-0191",
            "location": "Rome, Italy",
            "bio": "Customer success leader with a background in enterprise onboarding, renewals, and product feedback loops.",
            "skills": "Customer success, SaaS onboarding, account strategy, CRM, renewal planning, product feedback",
            "experience": "9 years helping enterprise customers adopt analytics, ecommerce, and workflow platforms.",
            "education": "MSc Business Management, LUISS Guido Carli",
        },
    },
])


RECRUITERS.extend([
    {"username": "samira_el_sayed", "email": "samira.elsayed@recruiter.example.com", "password": "Samira@2026"},
    {"username": "ethan_brooks", "email": "ethan.brooks@recruiter.example.com", "password": "Ethan@2026"},
    {"username": "marisol_vega", "email": "marisol.vega@recruiter.example.com", "password": "Marisol@2026"},
    {"username": "liam_chen", "email": "liam.chen@recruiter.example.com", "password": "Liam@2026"},
    {"username": "zara_mbeki", "email": "zara.mbeki@recruiter.example.com", "password": "Zara@2026"},
])


COMPANIES.extend([
    {
        "name": "Lumen Terra Biotech",
        "description": "Biotech company building software and wet-lab workflows for climate-resilient agriculture.",
        "location": "Cape Town, South Africa",
        "website": "https://lumenterrabiotech.example.com",
    },
    {
        "name": "Veridian Public Cloud",
        "description": "Cloud platform helping governments modernize public services, data sharing, and citizen support.",
        "location": "Ottawa, Canada",
        "website": "https://veridianpubliccloud.example.com",
    },
    {
        "name": "HarborLight Games",
        "description": "Independent game studio creating cooperative strategy games and creator tooling.",
        "location": "Seoul, South Korea",
        "website": "https://harborlightgames.example.com",
    },
    {
        "name": "Equator Mobility",
        "description": "Electric mobility company building fleet charging, route planning, and maintenance software.",
        "location": "Jakarta, Indonesia",
        "website": "https://equatormobility.example.com",
    },
    {
        "name": "Aster Legal Systems",
        "description": "Legal technology platform for contract review, matter management, and compliance workflows.",
        "location": "Dublin, Ireland",
        "website": "https://asterlegalsystems.example.com",
    },
])


ADDITIONAL_JOB_COMPANIES = [
    {
        "name": "Lumen Terra Biotech",
        "domain": "Agri-Biotech",
        "locations": ["Cape Town, South Africa", "Remote - Africa", "Nairobi, Kenya", "Remote - EMEA"],
        "tags": ["biotech", "agriculture", "climate"],
        "salary_offset": 0,
    },
    {
        "name": "Veridian Public Cloud",
        "domain": "Civic Cloud",
        "locations": ["Ottawa, Canada", "Remote - Canada", "Montreal, Canada", "Remote - North America"],
        "tags": ["govtech", "cloud", "public-sector"],
        "salary_offset": 9000,
    },
    {
        "name": "HarborLight Games",
        "domain": "Game Platform",
        "locations": ["Seoul, South Korea", "Remote - APAC", "Tokyo, Japan", "Remote - Worldwide"],
        "tags": ["games", "platform", "creative-tech"],
        "salary_offset": 4000,
    },
    {
        "name": "Equator Mobility",
        "domain": "Electric Mobility",
        "locations": ["Jakarta, Indonesia", "Remote - Southeast Asia", "Bangkok, Thailand", "Remote - APAC"],
        "tags": ["mobility", "ev", "fleet"],
        "salary_offset": 2000,
    },
    {
        "name": "Aster Legal Systems",
        "domain": "Legal Operations",
        "locations": ["Dublin, Ireland", "Remote - Europe", "London, UK", "Remote - EMEA"],
        "tags": ["legaltech", "workflow", "compliance"],
        "salary_offset": 7000,
    },
]


ADDITIONAL_JOB_ROLES = [
    ("Backend Engineer", "Build durable services, data models, and APIs for mission-critical workflows.", 103000, True, ["backend", "apis", "python"]),
    ("Frontend Engineer", "Create accessible interfaces, dashboards, and review flows for expert users.", 98000, True, ["frontend", "react", "typescript"]),
    ("Data Engineer", "Design reliable ingestion, transformation, and warehouse models for operational analytics.", 108000, True, ["data-engineering", "airflow", "sql"]),
    ("Machine Learning Engineer", "Train, evaluate, and deploy models that support high-value domain decisions.", 121000, True, ["machine-learning", "python", "mlops"]),
    ("Product Manager", "Shape roadmap priorities, discovery practices, and measurable product outcomes.", 118000, False, ["product", "roadmap", "analytics"]),
    ("UX Researcher", "Run field research, usability studies, and synthesis for complex professional workflows.", 92000, True, ["ux-research", "interviews", "figma"]),
    ("DevOps Engineer", "Improve deployment automation, infrastructure reliability, monitoring, and cost controls.", 119000, True, ["devops", "terraform", "kubernetes"]),
    ("Security Engineer", "Harden identity, application security, cloud posture, and incident response practices.", 125000, True, ["security", "cloud", "incident-response"]),
    ("QA Automation Engineer", "Build regression suites, test data strategies, and quality gates for fast releases.", 87000, True, ["qa", "automation", "playwright"]),
    ("Technical Writer", "Document APIs, workflows, release changes, and onboarding paths for technical users.", 76000, True, ["technical-writing", "docs", "openapi"]),
    ("Customer Success Manager", "Guide onboarding, adoption, renewals, and feedback for enterprise customers.", 85000, True, ["customer-success", "saas", "enterprise"]),
    ("Solutions Architect", "Map customer needs to platform architecture, integrations, and rollout plans.", 132000, False, ["solutions", "architecture", "integrations"]),
    ("Data Analyst", "Build dashboards, investigate trends, and translate data into operating decisions.", 79000, True, ["analytics", "sql", "tableau"]),
    ("Mobile Engineer", "Deliver polished mobile workflows, offline states, notifications, and release automation.", 101000, True, ["mobile", "flutter", "android"]),
    ("Platform Reliability Engineer", "Own uptime, observability, capacity planning, and production readiness reviews.", 127000, True, ["sre", "observability", "linux"]),
    ("Implementation Consultant", "Lead customer configuration, migration planning, and workflow rollout projects.", 83000, False, ["implementation", "consulting", "project-management"]),
    ("Business Operations Analyst", "Improve internal systems, capacity planning, reporting, and cross-functional processes.", 78000, True, ["operations", "analytics", "process"]),
    ("Partnerships Manager", "Develop partnerships, commercial motions, and ecosystem programs in strategic markets.", 95000, False, ["partnerships", "sales", "strategy"]),
    ("Research Scientist", "Prototype domain models, evaluate evidence, and publish practical research findings.", 134000, False, ["research", "python", "experimentation"]),
    ("Engineering Manager", "Coach engineers, plan delivery, and improve technical execution across product teams.", 148000, True, ["leadership", "engineering", "delivery"]),
    ("Revenue Operations Specialist", "Maintain CRM hygiene, forecasting, sales process automation, and funnel reporting.", 81000, True, ["revops", "crm", "reporting"]),
    ("Compliance Analyst", "Track regulatory requirements, audits, controls, and evidence collection workflows.", 88000, True, ["compliance", "risk", "audit"]),
    ("Developer Advocate", "Create demos, guides, workshops, and community feedback loops for builders.", 97000, True, ["developer-relations", "content", "apis"]),
    ("Localization Program Manager", "Coordinate multilingual launches, translation quality, and regional content operations.", 89000, True, ["localization", "program-management", "content"]),
]


def build_additional_jobs() -> list[tuple]:
    jobs = []
    for company in ADDITIONAL_JOB_COMPANIES:
        for index, role in enumerate(ADDITIONAL_JOB_ROLES):
            title, description, base_salary, is_remote, role_tags = role
            location = company["locations"][index % len(company["locations"])]
            jobs.append((
                company["name"],
                f"{company['domain']} {title}",
                description,
                location,
                base_salary + company["salary_offset"] + (index * 750),
                is_remote,
                role_tags + company["tags"],
            ))
    return jobs


JOBS.extend(build_additional_jobs())


def upsert_user(session: Session, data: dict, role: str) -> User:
    user = session.exec(select(User).where(User.email == data["email"])).first()
    if user is None:
        user = User(email=data["email"])

    user.username = data["username"]
    user.password = hash_password(data["password"])
    user.role = role
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def upsert_profile(session: Session, user_id: int, data: dict) -> UserProfile:
    profile = session.exec(select(UserProfile).where(UserProfile.user_id == user_id)).first()
    if profile is None:
        profile = UserProfile(user_id=user_id)

    for key, value in data.items():
        setattr(profile, key, value)

    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile


def upsert_company(session: Session, data: dict, created_by: int) -> Company:
    company = session.exec(select(Company).where(Company.name == data["name"])).first()
    if company is None:
        company = Company(name=data["name"])

    company.description = data["description"]
    company.location = data["location"]
    company.website = data["website"]
    company.created_by = created_by
    session.add(company)
    session.commit()
    session.refresh(company)
    return company


def get_or_create_tag(session: Session, name: str) -> Tag:
    normalized_name = name.strip().lower()
    tag = session.exec(select(Tag).where(Tag.name == normalized_name)).first()
    if tag is None:
        tag = Tag(name=normalized_name)
        session.add(tag)
        session.commit()
        session.refresh(tag)
    return tag


def upsert_job(session: Session, data: tuple, company: Company, created_by: int) -> Job:
    _, title, description, location, salary, is_remote, tags = data
    job = session.exec(
        select(Job).where(Job.title == title, Job.company_id == company.id)
    ).first()
    if job is None:
        job = Job(title=title, company_id=company.id)

    job.description = description
    job.location = location
    job.salary = salary
    job.is_remote = is_remote
    job.created_by = created_by
    job.company_id = company.id
    unique_tags = list(dict.fromkeys(tag.strip().lower() for tag in tags))
    job.tags = [get_or_create_tag(session, tag) for tag in unique_tags]

    session.add(job)
    session.commit()
    session.refresh(job)
    return job


def write_dummy_credentials(job_seekers: list[User], recruiters: list[User]) -> None:
    job_seeker_passwords = {item["email"]: item["password"] for item in JOB_SEEKERS}
    recruiter_passwords = {item["email"]: item["password"] for item in RECRUITERS}

    lines = [
        "Job Seekers",
        "===========",
    ]

    for user in job_seekers:
        lines.append(f"id: {user.id} | email: {user.email} | username: {user.username} | password: {job_seeker_passwords[user.email]}")

    lines.extend(["", "Recruiters", "=========="])

    for user in recruiters:
        lines.append(f"id: {user.id} | email: {user.email} | username: {user.username} | password: {recruiter_passwords[user.email]}")

    with open("dummy.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(lines) + "\n")


def main() -> None:
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        job_seekers = []
        for data in JOB_SEEKERS:
            user = upsert_user(session, data, "job_seeker")
            upsert_profile(session, user.id, data["profile"])
            job_seekers.append(user)

        recruiters = [upsert_user(session, data, "recruiter") for data in RECRUITERS]

        companies = {}
        for index, data in enumerate(COMPANIES):
            recruiter = recruiters[index % len(recruiters)]
            companies[data["name"]] = upsert_company(session, data, recruiter.id)

        jobs = []
        for index, data in enumerate(JOBS):
            company = companies[data[0]]
            recruiter = recruiters[index % len(recruiters)]
            jobs.append(upsert_job(session, data, company, recruiter.id))

        write_dummy_credentials(job_seekers, recruiters)

    print(f"Seeded {len(job_seekers)} job seekers with profiles.")
    print(f"Seeded {len(recruiters)} recruiters.")
    print(f"Seeded {len(companies)} companies.")
    print(f"Seeded {len(jobs)} jobs.")
    print("Wrote dummy.txt.")


if __name__ == "__main__":
    main()
