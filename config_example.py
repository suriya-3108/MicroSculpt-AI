# ============================================
# FILE: config_example.py
# PURPOSE: Example configuration file (Safe for Git)
# ============================================
# INSTRUCTIONS:
# 1. Copy this file to config.py
# 2. Replace the placeholder values with your actual API keys
# 3. Never commit config.py to Git (it's in .gitignore)

import os

# API KEYS (Prioritized Fallback)
# ---------------------------------------------
# 1. Google Gemini (Primary)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "your_gemini_api_key_here")

# 2. Groq (Secondary)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "your_groq_api_key_here")

# 3. Hugging Face (Tertiary)
HF_API_KEY = os.environ.get("HF_API_KEY", "your_huggingface_api_key_here")

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
