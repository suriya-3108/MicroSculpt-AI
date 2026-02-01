# ============================================
# FILE: config.py
# PURPOSE: Configuration management for MicroSculpt AI
# ============================================

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API KEYS (Loaded from .env file)
# ---------------------------------------------
# 1. Google Gemini (Primary)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# 2. Groq (Secondary)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# 3. Hugging Face (Tertiary)
HF_API_KEY = os.environ.get("HF_API_KEY")

# Validate that at least one API key is configured
if not GEMINI_API_KEY and not GROQ_API_KEY:
    raise ValueError(
        "No API keys found! Please set up your .env file with at least GEMINI_API_KEY or GROQ_API_KEY. "
        "Copy .env.example to .env and add your keys."
    )

# LANGUAGE SETTINGS
# ---------------------------------------------
SUPPORTED_LANGUAGES = {
    'python': {'ext': ['.py'], 'name': 'Python'},
    'javascript': {'ext': ['.js', '.jsx'], 'name': 'JavaScript'},
    'typescript': {'ext': ['.ts', '.tsx'], 'name': 'TypeScript'},
    'java': {'ext': ['.java'], 'name': 'Java'},
    'go': {'ext': ['.go'], 'name': 'Go'},
    'csharp': {'ext': ['.cs'], 'name': 'C#'}
}

# UI CONFIGURATION
# ---------------------------------------------
APP_NAME = "MicroSculpt AI"
APP_VERSION = "2.0.0"
THEME_COLOR = "#1E3A8A"
SECONDARY_COLOR = "#0EA5E9"

# API MODELS
# ---------------------------------------------
GEMINI_MODEL = "gemini-1.5-flash"
GROQ_MODEL = "llama-3.3-70b-versatile"
HF_MODEL = "bigcode/starcoder"
