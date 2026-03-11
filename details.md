# 🧬 MicroSculpt AI 2.0 — Complete Project Details

> **Version**: 2.0.0 | **Architecture**: Next.js + Flask (Full-Stack)  
> **Last Updated**: February 2026

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Problem Statement & Motivation](#2-problem-statement--motivation)
3. [System Architecture](#3-system-architecture)
4. [Technology Stack](#4-technology-stack)
5. [Project Structure](#5-project-structure)
6. [Backend Deep Dive](#6-backend-deep-dive)
7. [Frontend Deep Dive](#7-frontend-deep-dive)
8. [Phase-by-Phase Workflow](#8-phase-by-phase-workflow)
9. [AI & Machine Learning Pipeline](#9-ai--machine-learning-pipeline)
10. [API Reference](#10-api-reference)
11. [Deployment & Infrastructure](#11-deployment--infrastructure)
12. [Data Flow & State Management](#12-data-flow--state-management)
13. [Supported Languages](#13-supported-languages)
14. [Security & Configuration](#14-security--configuration)
15. [Migration History](#15-migration-history)
16. [Future Enhancements](#16-future-enhancements)

---

## 1. Project Overview

**MicroSculpt AI 2.0** is an intelligent, AI-powered platform that automatically transforms legacy monolithic codebases into modern, production-ready microservices architecture. The system leverages cutting-edge artificial intelligence, machine learning algorithms, and advanced code analysis techniques to automate the entire refactoring pipeline — from code parsing and bug detection to service grouping and Docker-ready code generation.

### What It Does (In One Line)

> Upload your monolithic code → AI analyzes, finds bugs, renames functions, maps dependencies, groups services → Download a ready-to-deploy microservices ZIP with Docker support.

### Key Capabilities

| Capability | Description |
|---|---|
| **Multi-Language Parsing** | Supports Python, JavaScript, TypeScript, Java, Go, and C# |
| **AI Bug Detection** | Finds bugs, security vulnerabilities, and code smells using Gemini/Groq |
| **Smart Function Naming** | AI suggests descriptive, business-logic function names |
| **Dependency Graph** | Interactive visualization of function call relationships |
| **Service Grouping** | ML-powered clustering of functions into logical microservices |
| **Code Generation** | Exports production-ready Flask/Express.js apps with Docker |

---

## 2. Problem Statement & Motivation

### The Problem

Many organizations are stuck with **legacy monolithic applications** that are:

- **Hard to scale** — You must scale the entire application, not individual features.
- **Risky to deploy** — A bug in one module can crash everything.
- **Slow to develop** — Large teams on a single codebase cause merge conflicts and bottlenecks.
- **Locked into one tech stack** — Difficult to adopt new technologies for specific features.
- **Expensive to refactor manually** — Manual migration takes months/years and is error-prone.

### The Solution

MicroSculpt AI 2.0 **automates the entire refactoring process** using AI:

- ⏱️ Reduces refactoring time from **months to hours**
- 🤖 Uses **AI-powered analysis** to find optimal service boundaries
- 🐛 Detects and fixes **bugs before migration**
- 📦 Generates **production-ready, Docker-containerized** microservices
- 🌐 Works with **6 major programming languages**

---

## 3. System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER'S BROWSER                           │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              FRONTEND (Next.js 16 + React 19)            │   │
│  │                                                          │   │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ │   │
│  │  │Input │ │ Bug  │ │Naming│ │Graph │ │Group │ │ Code │ │   │
│  │  │Module│→│Module│→│Module│→│Module│→│Module│→│ Gen  │ │   │
│  │  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘ └──────┘ │   │
│  └──────────────────────┬───────────────────────────────────┘   │
│                         │ REST API (HTTP/JSON)                  │
└─────────────────────────┼───────────────────────────────────────┘
                          │
┌─────────────────────────┼───────────────────────────────────────┐
│                  BACKEND (Flask + Python 3.11)                  │
│                         │                                       │
│  ┌──────────────────────▼───────────────────────────────────┐   │
│  │                    routes.py (API Layer)                  │   │
│  └──────────────────────┬───────────────────────────────────┘   │
│                         │                                       │
│  ┌──────────────────────▼───────────────────────────────────┐   │
│  │                   SERVICES LAYER                         │   │
│  │                                                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │   │
│  │  │ ParserSvc   │  │  AISvc      │  │ GraphSvc    │      │   │
│  │  │ (parse code)│  │ (bugs/names)│  │ (NetworkX)  │      │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘      │   │
│  │  ┌─────────────┐  ┌─────────────┐                        │   │
│  │  │ClusteringSvc│  │ CodegenSvc  │                        │   │
│  │  │ (K-Means)   │  │ (ZIP export)│                        │   │
│  │  └─────────────┘  └─────────────┘                        │   │
│  └──────────────────────────────────────────────────────────┘   │
│                         │                                       │
│  ┌──────────────────────▼───────────────────────────────────┐   │
│  │                   UTILITIES LAYER                        │   │
│  │                                                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │   │
│  │  │ APIManager  │  │ LangDetector│  │  Parsers/   │      │   │
│  │  │ (Gemini/    │  │ (auto-      │  │ (AST, Regex │      │   │
│  │  │  Groq/HF)   │  │  detect)    │  │  per-lang)  │      │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘      │   │
│  └──────────────────────────────────────────────────────────┘   │
│                         │                                       │
└─────────────────────────┼───────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────────┐
│                    EXTERNAL AI SERVICES                         │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Google Gemini│  │  Groq (Llama │  │ HuggingFace  │          │
│  │ (Primary)    │  │  3.3 70B)    │  │ (StarCoder)  │          │
│  │ gemini-1.5-  │  │ (Secondary)  │  │ (Tertiary)   │          │
│  │ flash        │  │              │  │              │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

### Architecture Pattern

- **Frontend**: Client-side rendering (CSR) with React state management
- **Backend**: Flask app factory pattern with Blueprints
- **Communication**: RESTful JSON API over HTTP
- **AI Integration**: Singleton APIManager with tri-level fallback
- **Deployment**: Docker Compose orchestration (2 containers)

---

## 4. Technology Stack

### Frontend Stack

| Technology | Version | Purpose |
|---|---|---|
| **Next.js** | 16.1.6 | React meta-framework for SSR/CSR |
| **React** | 19.2.3 | UI component library |
| **TypeScript** | ^5 | Type-safe JavaScript |
| **Tailwind CSS** | ^4 | Utility-first CSS framework |
| **Framer Motion** | ^12.34.0 | Animation library |
| **Recharts** | ^3.7.0 | Chart/data visualization |
| **Lucide React** | ^0.563.0 | Icon library |
| **clsx** | ^2.1.1 | Conditional CSS class utility |
| **tailwind-merge** | ^3.4.0 | Tailwind class merging |
| **Geist Font** | (built-in) | Typography (Geist Sans & Geist Mono) |

### Backend Stack

| Technology | Version | Purpose |
|---|---|---|
| **Python** | 3.11 | Core programming language |
| **Flask** | latest | Web framework (REST API) |
| **Flask-CORS** | latest | Cross-Origin Resource Sharing |
| **python-dotenv** | latest | Environment variable management |
| **requests** | latest | HTTP client for external APIs |
| **NetworkX** | latest | Graph algorithms & dependency analysis |
| **Matplotlib** | latest | Graph visualization & image generation |
| **NumPy** | <2.0.0 | Numerical computing for feature extraction |
| **scikit-learn** | latest | Machine learning (K-Means clustering, TF-IDF) |
| **Esprima** | latest | JavaScript/TypeScript code parsing |

### AI & ML Services

| Provider | Model | Role | API Type |
|---|---|---|---|
| **Google Gemini** | `gemini-1.5-flash` | Primary AI (bug detection, naming, service naming) | REST API |
| **Groq** | `llama-3.3-70b-versatile` | Secondary fallback | OpenAI-compatible API |
| **Hugging Face** | `bigcode/starcoder` | Tertiary fallback | Inference API |

### DevOps & Infrastructure

| Technology | Purpose |
|---|---|
| **Docker** | Container runtime |
| **Docker Compose** | Multi-container orchestration |
| **Git** | Version control |
| **.env files** | Secret management |

---

## 5. Project Structure

```
new Microsculpt/
│
├── 📄 .env                        # Environment variables (API keys) — NOT in Git
├── 📄 .env.example                 # Template for environment variables
├── 📄 .gitignore                   # Git ignore rules
├── 📄 docker-compose.yml           # Docker orchestration for both services
├── 📄 README.md                    # Project overview & quick start
├── 📄 MIGRATION_GUIDE.md           # Streamlit → Next.js migration docs
├── 📄 SETUP_GUIDE.md               # Step-by-step setup instructions
├── 📄 PROJECT_DETAILS.md           # Detailed project documentation (legacy)
├── 📄 details.md                   # This file — comprehensive project details
│
├── 📁 backend/                     # Flask Backend (Python)
│   ├── 📄 Dockerfile               # Python 3.11-slim container config
│   ├── 📄 requirements.txt         # Python dependencies
│   ├── 📄 config.py                # Configuration & API key management
│   ├── 📄 run.py                   # Application entry point
│   ├── 📁 uploads/                 # Temporary file upload storage
│   └── 📁 app/                     # Flask application package
│       ├── 📄 __init__.py          # App factory (create_app)
│       ├── 📄 routes.py            # All REST API endpoints
│       ├── 📁 services/            # Business logic layer
│       │   ├── 📄 parser_service.py      # Code parsing orchestrator
│       │   ├── 📄 ai_service.py          # AI bug detection & naming
│       │   ├── 📄 graph_service.py       # Dependency graph generation
│       │   ├── 📄 clustering_service.py  # ML-based service grouping
│       │   └── 📄 codegen_service.py     # Microservice code generation
│       └── 📁 utils/               # Shared utilities
│           ├── 📄 api_manager.py         # Tri-level AI API fallback manager
│           ├── 📄 language_detector.py   # Auto language detection
│           └── 📁 parsers/               # Language-specific parsers
│               ├── 📄 __init__.py        # Parser registry (get_parser)
│               ├── 📄 base_parser.py     # Abstract base parser class
│               ├── 📄 python_parser.py   # Python AST parser
│               ├── 📄 javascript_parser.py # JS/TS parser (Esprima)
│               ├── 📄 java_parser.py     # Java regex parser
│               ├── 📄 go_parser.py       # Go regex parser
│               └── 📄 csharp_parser.py   # C# regex parser
│
├── 📁 frontend/                    # Next.js Frontend (TypeScript)
│   ├── 📄 Dockerfile               # Node.js container config
│   ├── 📄 package.json             # Node.js dependencies & scripts
│   ├── 📄 tsconfig.json            # TypeScript configuration
│   ├── 📄 next.config.ts           # Next.js configuration
│   ├── 📄 postcss.config.mjs       # PostCSS for Tailwind
│   ├── 📄 eslint.config.mjs        # ESLint configuration
│   ├── 📁 public/                  # Static assets
│   └── 📁 src/
│       ├── 📁 app/                 # Next.js App Router
│       │   ├── 📄 layout.tsx       # Root layout (Geist fonts, metadata)
│       │   ├── 📄 page.tsx         # Main page (sidebar + 6-step wizard)
│       │   ├── 📄 globals.css      # Global styles (Tailwind base)
│       │   └── 📄 favicon.ico      # App icon
│       └── 📁 components/          # React UI Modules
│           ├── 📄 InputModule.tsx        # Phase 1: Code input & parsing
│           ├── 📄 BugModule.tsx          # Phase 2: AI bug detection
│           ├── 📄 NamingModule.tsx       # Phase 3: Smart function naming
│           ├── 📄 GraphModule.tsx        # Phase 4: Dependency graph
│           ├── 📄 GroupingModule.tsx      # Phase 5: Service grouping
│           └── 📄 GenerationModule.tsx   # Phase 6: Code generation & download
│
├── 📁 output/                      # Generated microservice outputs
├── 📁 examples/                    # Sample input files for testing
└── 📁 Screenshots/                 # UI screenshots
```

---

## 6. Backend Deep Dive

### App Factory Pattern (`app/__init__.py`)

The backend uses Flask's **App Factory pattern** for clean initialization:

```python
from flask import Flask
from flask_cors import CORS
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app)  # Enable cross-origin requests from Next.js
    from app.routes import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    return app
```

### Configuration (`config.py`)

Centralized configuration management:

| Config Key | Value | Source |
|---|---|---|
| `GEMINI_API_KEY` | User's key | `.env` file |
| `GROQ_API_KEY` | User's key | `.env` file |
| `HF_API_KEY` | User's key | `.env` file |
| `GEMINI_MODEL` | `gemini-1.5-flash` | Hardcoded default |
| `GROQ_MODEL` | `llama-3.3-70b-versatile` | Hardcoded default |
| `HF_MODEL` | `bigcode/starcoder` | Hardcoded default |
| `UPLOAD_FOLDER` | `backend/uploads/` | Auto-created |

### Services Layer

The backend follows a **Service-Oriented Architecture** internally. Each service is a static class:

| Service | File | Responsibility |
|---|---|---|
| `ParserService` | `parser_service.py` | Orchestrates language detection + parsing |
| `AIService` | `ai_service.py` | Bug analysis, name suggestions, service naming |
| `GraphService` | `graph_service.py` | Builds dependency graph, generates visualization |
| `ClusteringService` | `clustering_service.py` | K-Means clustering for service grouping |
| `CodegenService` | `codegen_service.py` | Generates Flask/Express microservice code |
| `CodeGenerator` | `codegen_service.py` | Template engine for Python/Node.js code |

### API Manager (`api_manager.py`)

The `APIManager` is a **singleton** that implements a **tri-level AI fallback strategy**:

```
Gemini (Primary) → Groq (Secondary) → HuggingFace (Tertiary)
```

- Each provider is called with a 30-second timeout
- If one fails, the next provider is attempted automatically
- The successful provider name is returned alongside the response
- Configuration is read from Flask's `current_app` or environment variables

### Parser System

The parser system uses a **Strategy Pattern** with a base parser class and language-specific implementations:

| Parser | Language(s) | Technique |
|---|---|---|
| `python_parser.py` | Python | Built-in `ast` module (AST parsing) |
| `javascript_parser.py` | JavaScript, TypeScript | `esprima` library (AST parsing) |
| `java_parser.py` | Java | Regex-based pattern matching |
| `go_parser.py` | Go | Regex-based pattern matching |
| `csharp_parser.py` | C# | Regex-based pattern matching |

Each parser extracts:
- Function/method **name**
- **Parameters** list
- **Body** (complete function code)
- **Line number** in original file
- **Calls** (other functions referenced in the body)

---

## 7. Frontend Deep Dive

### Page Architecture (`page.tsx`)

The frontend is a **Single Page Application** using a step-wizard pattern:

- **Sidebar**: Shows all 6 phases with progress indicators (⚪ pending → 🔵 active → ✅ completed)
- **Main Content Area**: Renders the active module component
- **State**: Centralized `projectData` object passed down to all modules via props

```typescript
const [projectData, setProjectData] = useState({
  code: "",        // Raw source code
  language: "",    // Detected language
  filename: "",    // Original file name
  functions: [],   // Parsed function list
  services: {},    // Grouped service mapping
  renames: {},     // Applied function renames
});
```

### Module Components

Each phase has its own dedicated React component:

| Component | Phase | Key Features |
|---|---|---|
| `InputModule.tsx` | 1 | File upload, code paste, calls `/api/parse` |
| `BugModule.tsx` | 2 | AI analysis, issue list, apply fixes, calls `/api/analyze-bugs` |
| `NamingModule.tsx` | 3 | Name suggestions, selective apply, calls `/api/suggest-names` |
| `GraphModule.tsx` | 4 | Dependency visualization, metrics, calls `/api/dependency-graph` |
| `GroupingModule.tsx` | 5 | Service clusters, rename services, calls `/api/group-services` |
| `GenerationModule.tsx` | 6 | Code export, ZIP download, calls `/api/generate-code` |

### UI Design System

- **Font**: Geist Sans + Geist Mono (Google Fonts via Next.js)
- **Styling**: Tailwind CSS v4 with PostCSS
- **Animations**: Framer Motion for smooth transitions
- **Icons**: Lucide React icon library
- **Charts**: Recharts for any data visualizations
- **Theme**: Clean white/gray with blue accents

---

## 8. Phase-by-Phase Workflow

### Phase 1: Input & Analysis

```
User uploads .py/.js/.ts/.java/.go/.cs file OR pastes code
        │
        ▼
Frontend reads file content in browser (FileReader API)
        │
        ▼
POST /api/parse { code, fileName }
        │
        ▼
LanguageDetector → detects language by extension + code patterns
        │
        ▼
get_parser(language) → returns appropriate parser
        │
        ▼
Parser extracts functions → { name, params, body, calls }
        │
        ▼
Returns { language, functions[], count }
```

**What Happens Technically:**
1. The frontend's `InputModule` uses the browser's `FileReader` API to read the uploaded file as text.
2. The raw code and filename are sent to the backend's `/api/parse` endpoint.
3. `LanguageDetector.detect_language()` checks the file extension first, then falls back to code pattern analysis.
4. The appropriate language parser (e.g., `PythonParser`) uses AST parsing or regex to extract all function definitions.
5. Each function is returned as a structured object with name, parameters, body, and inter-function calls.

---

### Phase 2: AI Bug Detection

```
Frontend sends { code, language } to POST /api/analyze-bugs
        │
        ▼
AIService crafts a structured prompt with:
  - Language context
  - Bug categories to check
  - JSON output format requirements
        │
        ▼
APIManager.generate_content(prompt)
  → Tries Gemini → Groq → HuggingFace (fallback chain)
        │
        ▼
AI Response: { issues[], fixed_code, summary }
        │
        ▼
AIService._extract_json() parses response
  (handles markdown code blocks, JSON extraction)
        │
        ▼
User reviews issues → can "Apply Fixes" to update code
```

**What Happens Technically:**
1. A carefully crafted prompt is sent to the AI, containing the full code and specific instructions for JSON-formatted output.
2. The prompt engineering includes escape rules for newlines and quotes to ensure valid JSON responses.
3. The `_extract_json()` method has multiple fallback strategies: strip markdown → direct parse → regex brace extraction.
4. The AI identifies: logic errors, null pointer issues, type mismatches, security vulnerabilities, performance bottlenecks, and code smells.
5. The user can selectively apply the AI's suggested fixes.

---

### Phase 3: Smart Function Naming

```
Frontend sends { code, language, functions[] } to POST /api/suggest-names
        │
        ▼
AIService crafts naming prompt with:
  - Current function names
  - Code context (first 2000 chars)
  - Language-specific naming conventions
  - Uniqueness requirement
        │
        ▼
AI analyzes code semantics and suggests new names
        │
        ▼
Returns { suggestions: [{ current, suggested, reason }] }
        │
        ▼
User selectively applies renames → stored in projectData.renames
```

**What Happens Technically:**
1. The AI receives function names and code context to understand what each function actually does.
2. It applies language-specific naming conventions: `snake_case` for Python, `camelCase` for JS/Java/C#.
3. Names are based on semantic understanding of the code logic (e.g., `func1` → `calculate_monthly_revenue`).
4. Each suggestion includes a reason explaining why the new name is better.
5. Applied renames are stored and carried forward to code generation.

---

### Phase 4: Dependency Graph

```
Frontend sends { functions[] } to POST /api/dependency-graph
        │
        ▼
GraphService builds directed graph using NetworkX:
  - Nodes = function names
  - Edges = function calls (A calls B → edge A→B)
        │
        ▼
Layout algorithm:
  - <10 nodes → spring_layout (k=2, 50 iterations)
  - ≥10 nodes → kamada_kawai_layout (fallback: spring)
        │
        ▼
Matplotlib renders graph → Base64 PNG image
        │
        ▼
Returns { image (base64), metrics { total, connections, isolated } }
```

**What Happens Technically:**
1. A `DiGraph` (directed graph) is constructed where each function is a node.
2. Edges represent function calls found during parsing (Phase 1 identifies `calls` for each function).
3. Only edges between known functions are added (filters out stdlib/external calls).
4. **Metrics calculated**: total functions, number of connections, isolated functions (degree 0).
5. Isolated functions are flagged as potential dead code.
6. The graph is rendered as a PNG using Matplotlib with dark-themed nodes (#234C6A), exported as Base64.
7. The frontend displays the Base64 image directly in an `<img>` tag.

---

### Phase 5: Service Grouping (ML-Powered)

```
Frontend sends { functions[] } to POST /api/group-services
        │
        ▼
ClusteringService:
  1. Extract function names
  2. TF-IDF Vectorization (tokenize names → numerical vectors)
  3. K-Means Clustering
     - n_clusters = max(2, min(5, n_functions // 3))
     - random_state=42 for reproducibility
  4. AI names each cluster via AIService
        │
        ▼
Returns { services: { "UserService": ["login", "register"], ... }, count, provider }
```

**What Happens Technically:**

#### Step 1: Feature Extraction (TF-IDF)
- Function names are treated as "documents"
- `TfidfVectorizer` with token pattern `[a-zA-Z_][a-zA-Z0-9_]*` splits names like `calculate_user_tax` into tokens: `["calculate", "user", "tax"]`
- Each function gets a numerical feature vector based on term frequency and inverse document frequency
- If vectorization fails, falls back to identity matrix (each function is unique)

#### Step 2: K-Means Clustering
- **K (number of clusters)** is automatically determined: `max(2, min(5, n_functions // 3))`
  - Minimum 2 services, maximum 5 services
  - Roughly 1 service per 3 functions
- `KMeans(n_clusters, random_state=42, n_init=10)` runs 10 initializations for stability
- Functions with similar names/purposes are grouped together

#### Step 3: AI Service Naming
- The cluster map (e.g., `{ 0: ["login_user", "register_user"], 1: ["process_payment"] }`) is sent to the AI
- AI generates business-meaningful service names (e.g., `AuthenticationService`, `PaymentService`)
- Naming rules enforced: CamelCase, ends with "Service", no special characters

---

### Phase 6: Code Generation

```
Frontend sends { services, language, functions, renames, filename }
  to POST /api/generate-code
        │
        ▼
CodegenService.generate_code_package():
  For each service:
    If Python → CodeGenerator.generate_python_flask()
      - Creates Flask app with routes for each function
      - Generates requirements.txt, Dockerfile
    If JavaScript → CodeGenerator.generate_nodejs_express()
      - Creates Express.js app with routes
      - Generates package.json, Dockerfile
    │
    ▼
  Generates shared docker-compose.yml
  Generates README.md with instructions
  Packages everything into ZIP (in-memory BytesIO)
        │
        ▼
Returns ZIP file as binary download
```

**Generated Microservice Structure (per service):**

```
microservices_python/
├── docker-compose.yml      # Orchestrates all services
├── README.md               # Deployment instructions
├── AuthService/
│   ├── app.py              # Flask app with API routes
│   ├── requirements.txt    # Flask dependency
│   └── Dockerfile          # Python 3.11-slim container
├── PaymentService/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
└── ...
```

**Code Generation Patterns:**
- Each function becomes a `POST` endpoint at `/<function_name>`
- Functions with applied renames use the new names
- Error handling with try-catch blocks
- CORS enabled for inter-service communication
- Health check endpoint (`/health`) on each service
- Port assignment: 5001, 5002, 5003, ... (incrementing per service)

---

## 9. AI & Machine Learning Pipeline

### AI Provider Fallback Strategy

```
┌──────────────────────┐
│   APIManager         │
│   (Singleton)        │
├──────────────────────┤
│                      │
│  1. Try Gemini ──────┼──► Success? → Return (response, "Gemini")
│     │                │
│     ▼ (fails)        │
│  2. Try Groq ────────┼──► Success? → Return (response, "Groq")
│     │                │
│     ▼ (fails)        │
│  3. Try HuggingFace ─┼──► Success? → Return (response, "HuggingFace")
│     │                │
│     ▼ (fails)        │
│  Return (None, error)│
│                      │
└──────────────────────┘

Each call has: 30-second timeout, temperature: 0.7, max_tokens: 2048
```

### Machine Learning Algorithms Used

| Algorithm | Library | Purpose | Phase |
|---|---|---|---|
| **TF-IDF Vectorization** | scikit-learn | Convert function names to numerical features | Phase 5 |
| **K-Means Clustering** | scikit-learn | Group similar functions into services | Phase 5 |
| **Directed Graph Analysis** | NetworkX | Model and analyze function dependencies | Phase 4 |
| **Spring/Kamada-Kawai Layout** | NetworkX | Optimize graph visualization layout | Phase 4 |

### Prompt Engineering Techniques

The AI prompts are carefully structured to ensure:

1. **Structured Output**: JSON format is enforced with explicit formatting rules
2. **Escape Rules**: Newlines must be `\\n`, quotes must be `\\"`
3. **No Markdown**: Responses must be raw JSON (no code blocks)
4. **Context Limiting**: Code context is truncated to 2000 chars for naming to avoid token limits
5. **Uniqueness Constraints**: Function name suggestions must all be unique
6. **Language Awareness**: Prompts specify the source language for appropriate analysis
7. **JSON Extraction Fallback**: `_extract_json()` handles markdown-wrapped, raw, and brace-only responses

---

## 10. API Reference

All endpoints are prefixed with `/api` and served by the Flask backend at `http://localhost:5000`.

### `GET /api/health`

Health check endpoint.

**Response:**
```json
{ "status": "ok", "message": "MicroSculpt AI Backend Running" }
```

---

### `POST /api/parse`

Parse source code and extract function definitions.

**Request Body:**
```json
{
  "code": "def hello(): print('hi')\ndef world(): hello()",
  "fileName": "main.py"
}
```

**Response:**
```json
{
  "language": "python",
  "functions": [
    { "name": "hello", "params": [], "body": "def hello(): print('hi')", "calls": [] },
    { "name": "world", "params": [], "body": "def world(): hello()", "calls": ["hello"] }
  ],
  "count": 2
}
```

---

### `POST /api/analyze-bugs`

AI-powered bug detection and fixing.

**Request Body:**
```json
{
  "code": "def divide(a, b): return a/b",
  "language": "python"
}
```

**Response:**
```json
{
  "issues": ["Division by zero not handled", "No type checking"],
  "fixed_code": "def divide(a, b):\n    if b == 0:\n        raise ValueError('Cannot divide by zero')\n    return a / b",
  "summary": "Added zero-division guard",
  "provider": "Gemini"
}
```

---

### `POST /api/suggest-names`

AI-powered function name suggestions.

**Request Body:**
```json
{
  "code": "def f1(x): return x * 1.08",
  "language": "python",
  "functions": ["f1"]
}
```

**Response:**
```json
{
  "suggestions": [
    { "current": "f1", "suggested": "calculate_tax_inclusive_price", "reason": "Function multiplies by 1.08, indicating tax calculation" }
  ],
  "provider": "Gemini"
}
```

---

### `POST /api/dependency-graph`

Generate function dependency graph visualization.

**Request Body:**
```json
{
  "functions": [
    { "name": "main", "calls": ["process", "output"] },
    { "name": "process", "calls": ["validate"] },
    { "name": "validate", "calls": [] },
    { "name": "output", "calls": [] }
  ]
}
```

**Response:**
```json
{
  "image": "iVBORw0KGgoAAAANS...",  // Base64-encoded PNG
  "metrics": {
    "total_functions": 4,
    "connections": 3,
    "isolated": 0
  }
}
```

---

### `POST /api/group-services`

ML-powered service grouping.

**Request Body:**
```json
{
  "functions": [
    { "name": "login_user" },
    { "name": "register_user" },
    { "name": "process_payment" },
    { "name": "validate_card" }
  ]
}
```

**Response:**
```json
{
  "services": {
    "AuthenticationService": ["login_user", "register_user"],
    "PaymentService": ["process_payment", "validate_card"]
  },
  "count": 2,
  "provider": "Gemini"
}
```

---

### `POST /api/generate-code`

Generate and download microservice code package.

**Request Body:**
```json
{
  "services": { "AuthService": ["login", "register"], "PayService": ["pay"] },
  "language": "python",
  "functions": [{ "name": "login", "body": "def login(): pass" }],
  "renames": { "login": "authenticate_user" },
  "filename": "myapp"
}
```

**Response:** Binary ZIP file download (`microservices_python.zip`)

---

## 11. Deployment & Infrastructure

### Docker Compose Configuration

```yaml
version: '3.8'

services:
  backend:
    build: ./backend                    # Uses backend/Dockerfile
    ports:
      - "5000:5000"                     # Flask API
    volumes:
      - ./backend:/app                  # Live reload in development
    environment:
      - FLASK_ENV=development
    env_file:
      - .env                            # API keys

  frontend:
    build: ./frontend                   # Uses frontend/Dockerfile
    ports:
      - "3000:3000"                     # Next.js
    volumes:
      - ./frontend:/app
      - /app/node_modules               # Preserve node_modules in container
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:5000/api
    depends_on:
      - backend                         # Start backend first
```

### Running the Application

#### Option 1: Docker (Recommended)
```bash
# Build and start both services
docker-compose up --build

# Access:
# Frontend → http://localhost:3000
# Backend  → http://localhost:5000/api/health
```

#### Option 2: Manual Setup

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
python run.py                  # Starts Flask on port 5000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev                    # Starts Next.js on port 3000
```

### Docker Images

| Service | Base Image | Exposed Port |
|---|---|---|
| Backend | `python:3.11-slim` | 5000 |
| Frontend | Node.js (Next.js default) | 3000 |

---

## 12. Data Flow & State Management

### End-to-End Data Flow

```
User                 Frontend (React)              Backend (Flask)              AI APIs
 │                       │                              │                         │
 ├── Upload file ──────► │                              │                         │
 │                       ├── POST /api/parse ─────────► │                         │
 │                       │   { code, fileName }         ├── detect language       │
 │                       │                              ├── parse functions       │
 │                       │ ◄── { language, functions } ─┤                         │
 │                       │                              │                         │
 │ ◄── Show functions ──┤                              │                         │
 │                       │                              │                         │
 ├── "Analyze Bugs" ───► │                              │                         │
 │                       ├── POST /api/analyze-bugs ──► │                         │
 │                       │                              ├── prompt ─────────────► │
 │                       │                              │ ◄── AI response ───────┤
 │                       │ ◄── { issues, fixed_code } ─┤                         │
 │                       │                              │                         │
 │ ◄── Show issues ─────┤                              │                         │
 │── "Apply Fixes" ────►│── updates local state        │                         │
 │                       │                              │                         │
 │── "Suggest Names" ──►│                              │                         │
 │                       ├── POST /api/suggest-names ─► │                         │
 │                       │                              ├── prompt ─────────────► │
 │                       │ ◄── { suggestions } ────────┤ ◄── AI response ───────┤
 │                       │                              │                         │
 │ ◄── Show suggestions ┤                              │                         │
 │── "Apply Renames" ──►│── updates projectData.renames│                         │
 │                       │                              │                         │
 │── "Show Graph" ─────►│                              │                         │
 │                       ├── POST /api/dependency-graph►│                         │
 │                       │                              ├── build NetworkX graph  │
 │                       │                              ├── render Matplotlib img │
 │                       │ ◄── { image (base64) } ─────┤                         │
 │                       │                              │                         │
 │ ◄── Display graph ───┤                              │                         │
 │                       │                              │                         │
 │── "Group Services" ─►│                              │                         │
 │                       ├── POST /api/group-services ─►│                         │
 │                       │                              ├── TF-IDF vectorize     │
 │                       │                              ├── K-Means cluster      │
 │                       │                              ├── AI name services ───► │
 │                       │ ◄── { services } ───────────┤ ◄── service names ─────┤
 │                       │                              │                         │
 │ ◄── Show services ───┤                              │                         │
 │                       │                              │                         │
 │── "Generate Code" ──►│                              │                         │
 │                       ├── POST /api/generate-code ──►│                         │
 │                       │                              ├── generate Flask/       │
 │                       │                              │   Express code          │
 │                       │                              ├── create Dockerfiles   │
 │                       │                              ├── ZIP everything       │
 │                       │ ◄── ZIP file (binary) ──────┤                         │
 │                       │                              │                         │
 │ ◄── Download ZIP ────┤                              │                         │
```

### State Object (`projectData`)

The state is managed in the main `page.tsx` and passed as props to all modules:

| Field | Type | Set By | Used By |
|---|---|---|---|
| `code` | `string` | Phase 1 (InputModule) | Phases 2, 3, 6 |
| `language` | `string` | Phase 1 (InputModule) | Phases 2, 3, 6 |
| `filename` | `string` | Phase 1 (InputModule) | Phase 6 |
| `functions` | `array` | Phase 1 (InputModule) | Phases 4, 5, 6 |
| `services` | `object` | Phase 5 (GroupingModule) | Phase 6 |
| `renames` | `object` | Phase 3 (NamingModule) | Phase 6 |

---

## 13. Supported Languages

| Language | File Extensions | Parser Type | Parser File |
|---|---|---|---|
| **Python** | `.py` | AST (built-in `ast` module) | `python_parser.py` |
| **JavaScript** | `.js`, `.jsx` | AST (`esprima` library) | `javascript_parser.py` |
| **TypeScript** | `.ts`, `.tsx` | AST (`esprima` library) | `javascript_parser.py` |
| **Java** | `.java` | Regex pattern matching | `java_parser.py` |
| **Go** | `.go` | Regex pattern matching | `go_parser.py` |
| **C#** | `.cs` | Regex pattern matching | `csharp_parser.py` |

### Code Generation Target Frameworks

| Source Language | Generated Framework | Generated Files |
|---|---|---|
| Python | **Flask** | `app.py`, `requirements.txt`, `Dockerfile` |
| JavaScript/TypeScript | **Express.js** | `index.js`, `package.json`, `Dockerfile` |
| Java/Go/C# | **Flask** (default) | `app.py`, `requirements.txt`, `Dockerfile` |

---

## 14. Security & Configuration

### API Key Management

```
.env.example (committed to Git — contains only placeholders)
     │
     ▼
.env (NOT committed — contains actual keys)
     │
     ▼
config.py reads via python-dotenv → Flask app config
     │
     ▼
APIManager reads from current_app.config or os.environ
```

### Required API Keys

| Key | Required | Free Tier | Get It At |
|---|---|---|---|
| `GEMINI_API_KEY` | ✅ Yes (primary) | Yes | [Google AI Studio](https://makersuite.google.com/app/apikey) |
| `GROQ_API_KEY` | ⚠️ Recommended | Yes | [Groq Console](https://console.groq.com/keys) |
| `HF_API_KEY` | 💡 Optional | Yes | [HuggingFace](https://huggingface.co/settings/tokens) |

### Security Best Practices

- `.env` and `config.py` are in `.gitignore` — never committed
- Only `.env.example` is tracked (contains placeholders only)
- API keys are injected via environment variables in Docker
- CORS is enabled to allow frontend-backend communication
- No user authentication (designed for local/development use)

---

## 15. Migration History

The project underwent a **major architectural migration** from a monolithic Streamlit application to a decoupled full-stack architecture:

| Aspect | Before (v1.0) | After (v2.0) |
|---|---|---|
| **Frontend** | Streamlit (Python) | Next.js 16 + React 19 (TypeScript) |
| **Backend** | Streamlit built-in | Flask REST API (Python) |
| **State** | `st.session_state` (server-side) | React `useState` (client-side) |
| **File Upload** | Streamlit file uploader | Browser FileReader → API POST |
| **Visualization** | Matplotlib rendered directly | Base64 PNG via API |
| **Deployment** | `streamlit run app.py` | Docker Compose (2 containers) |
| **Entry Point** | Single `app.py` | `run.py` (backend) + `npm run dev` (frontend) |
| **UI Framework** | Streamlit widgets | Tailwind CSS + Framer Motion |
| **Port** | 8501 (Streamlit) | 3000 (frontend) + 5000 (backend) |

### Why the Migration?

1. **Better UI/UX**: Next.js + Tailwind enables modern, polished interfaces that Streamlit cannot achieve.
2. **Scalability**: Decoupled architecture allows independent scaling of frontend and backend.
3. **Developer Experience**: TypeScript + React provides better tooling, type safety, and component reuse.
4. **Deployment Flexibility**: Docker containerization enables cloud-native deployment.
5. **Performance**: Client-side rendering reduces server load.

---

## 16. Future Enhancements

| Feature | Description | Status |
|---|---|---|
| Database Schema Generation | Auto-design databases for each microservice | 🔮 Planned |
| API Gateway Configuration | Generate API gateway routing rules | 🔮 Planned |
| Automated Test Generation | Create unit and integration tests | 🔮 Planned |
| Monitoring & Observability | Built-in logging and metrics setup | 🔮 Planned |
| CI/CD Pipeline Generation | GitHub Actions / GitLab CI configs | 🔮 Planned |
| Performance Optimization | AI-powered performance tuning | 🔮 Planned |
| Advanced Security Scanning | Deeper vulnerability detection | 🔮 Planned |
| Cloud Deployment | Direct deploy to AWS/Azure/GCP | 🔮 Planned |
| Real-time Collaboration | Multi-user editing and review | 🔮 Planned |
| Plugin System | Custom parser/generator extensions | 🔮 Planned |

---

## Summary

MicroSculpt AI 2.0 is a **full-stack, AI-powered monolith-to-microservices refactoring platform** built with:

- **Next.js 16 + React 19** (frontend) — modern, responsive UI with Tailwind CSS
- **Flask + Python 3.11** (backend) — REST API with 5 service classes
- **Google Gemini / Groq / HuggingFace** (AI) — tri-level fallback for reliability
- **scikit-learn** (ML) — TF-IDF + K-Means for intelligent service grouping
- **NetworkX + Matplotlib** (visualization) — dependency graph analysis
- **Docker Compose** (deployment) — containerized 2-service architecture

The platform takes monolithic code through **6 automated phases**: Parse → Detect Bugs → Rename Functions → Map Dependencies → Group Services → Generate Code — producing a **ready-to-deploy ZIP** with Docker support.

---

*Built with ❤️ using Next.js, Flask, and Google Gemini AI*
