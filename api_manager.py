# ============================================
# FILE: api_manager.py
# PURPOSE: Central API client with intelligent fallback
# ============================================

import os
import requests
from config import GEMINI_API_KEY, GROQ_API_KEY, HF_API_KEY, GEMINI_MODEL, GROQ_MODEL, HF_MODEL

class APIManager:
    def __init__(self):
        self.primary_available = True
        self.secondary_available = True
        self.tertiary_available = True

    def generate_content(self, prompt, temperature=0.7):
        """
        Generate content using available APIs with fallback strategy:
        Gemini -> Groq -> HuggingFace
        """
        response = None
        error_log = []

        # 1. Try Gemini (Primary) - Using REST API
        if self.primary_available:
            try:
                response = self._call_gemini(prompt, temperature)
                if response:
                    return response, "Gemini"
            except Exception as e:
                error_log.append(f"Gemini Error: {str(e)}")
        
        # 2. Try Groq (Secondary)
        if self.secondary_available:
            try:
                response = self._call_groq(prompt, temperature)
                if response:
                    return response, "Groq"
            except Exception as e:
                error_log.append(f"Groq Error: {str(e)}")
        
        # 3. Try HuggingFace (Tertiary)
        if self.tertiary_available:
            try:
                response = self._call_huggingface(prompt, temperature)
                if response:
                    return response, "HuggingFace"
            except Exception as e:
                error_log.append(f"HF Error: {str(e)}")

        return None, f"All APIs failed. Errors: {'; '.join(error_log)}"

    def _call_gemini(self, prompt, temperature):
        """Call Google Gemini API using REST endpoint"""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
        
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": 2048,
            }
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                text = result['candidates'][0]['content']['parts'][0]['text']
                return text
            else:
                raise Exception("No candidates in response")
        else:
            raise Exception(f"Gemini API returned {response.status_code}: {response.text}")

    def _call_groq(self, prompt, temperature):
        """Call Groq API"""
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "messages": [{"role": "user", "content": prompt}],
            "model": GROQ_MODEL,
            "temperature": temperature,
            "max_tokens": 2048
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            raise Exception(f"Groq API returned {response.status_code}: {response.text}")

    def _call_huggingface(self, prompt, temperature):
        """Call Hugging Face Inference API"""
        url = f"https://router.huggingface.co/models/{HF_MODEL}"
        headers = {"Authorization": f"Bearer {HF_API_KEY}"}
        data = {
            "inputs": prompt,
            "parameters": {
                "temperature": temperature,
                "max_new_tokens": 1024,
                "return_full_text": False
            }
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', '')
            elif isinstance(result, dict) and 'generated_text' in result:
                return result['generated_text']
            else:
                return str(result)
        else:
            raise Exception(f"HF API returned {response.status_code}: {response.text}")

# Singleton instance
api_client = APIManager()
