# MicroSculpt AI 2.0 - Migration Guide

This document outlines the migration of the MicroSculpt AI application from a monolithic Streamlit app to a modern Full-Stack Architecture using Next.js and Flask.

## 🏗️ Architecture Overview

| Component | Technology | Description |
|-----------|------------|-------------|
| **Frontend** | Next.js 16 (React) | Modern, responsive UI with Tailwind CSS. Handles state and user interactions. |
| **Backend** | Flask (Python) | REST API exposing the original application logic. Handles AI processing and file operations. |
| **Parsing** | Python AST / Regex | Retains original logic for parsing Python, JS, Java, Go, C#. |
| **AI** | Gemini / Groq | Uses `api_manager.py` adapted for the new backend structure. |

## 📂 Project Structure

```
new Microsculpt/
├── backend/                # Flask Backend
│   ├── app/
│   │   ├── services/       # Core business logic (Parser, AI, Graph, etc.)
│   │   ├── utils/          # Shared utilities (API Client, Language Detector)
│   │   ├── routes.py       # API Endpoints
│   │   └── __init__.py     # App Factory
│   ├── original_code_reference/ # Copy of original Streamlit modules
│   ├── Dockerfile          # Backend Container config
│   └── run.py              # Entry point
├── frontend/               # Next.js Frontend
│   ├── src/
│   │   ├── app/            # Pages and Layouts
│   │   ├── components/     # UI Modules (InputModule, BugModule, etc.)
│   │   └── styles/         # Global styles
│   ├── Dockerfile          # Frontend Container config
│   └── next.config.ts      # Next.js Config
├── docker-compose.yml      # Orchestration for both services
└── MIGRATION_MAPPING.md    # Detailed mapping of old files to new files
```

## 🚀 How to Run

### Option 1: Docker (Recommended)
This requires Docker and Docker Compose to be installed.

1. **Build and Start:**
   ```bash
   docker-compose up --build
   ```
2. **Access the App:**
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend API: [http://localhost:5000](http://localhost:5000)

### Option 2: Manual Setup

**Backend:**
1. Navigate to `/backend`
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python run.py
   ```

**Frontend:**
1. Navigate to `/frontend`
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```

## ⚠️ Key Changes & Notes

1. **State Management**: 
   - Original: `st.session_state` (Server-side session).
   - New: React `useState` (Client-side state). Data is passed between steps via props in `page.tsx`.

2. **File Handling**:
   - Original: Direct file upload to Streamlit memory.
   - New: `InputModule` reads file content in browser and sends text to Backend API.

3. **Visualization**:
   - Original: Matplotlib figures rendered directly.
   - New: Backend generates Base64 image strings; Frontend renders `<img>` tags.

4. **Environment Variables**:
   - Ensure a `.env` file exists in `/backend` with your API keys (`GEMINI_API_KEY`, etc.) as defined in `config.py`.

## 🔍 Verification

The system has been verified to:
- [x] Compile Frontend successfully (Next.js Build).
- [x] Initialize Backend structure correctly.
- [x] Contain all original parsing and AI logic.
- [x] Match the original dark/light aesthetic (Black & White strict theme).

For more details on specific code mappings, refer to [MIGRATION_MAPPING.md](./MIGRATION_MAPPING.md).
