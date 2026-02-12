import os
import requests
from flask import current_app
# Use safe imports that work both in Flask context and standalone if config is in path
try:
    from config import GEMINI_API_KEY, GROQ_API_KEY, HF_API_KEY, GEMINI_MODEL, GROQ_MODEL, HF_MODEL
except ImportError:
    # Fallback or rely on current_app
    pass

class APIManager:
    def __init__(self):
        self.primary_available = True
        self.secondary_available = True
        self.tertiary_available = True

    def _get_config(self, key, default=None):
        if current_app:
            return current_app.config.get(key, default)
        return os.environ.get(key, default)

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
        key = self._get_config('GEMINI_API_KEY')
        model = self._get_config('GEMINI_MODEL', "gemini-1.5-flash")
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
        
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
        key = self._get_config('GROQ_API_KEY')
        model = self._get_config('GROQ_MODEL', "llama-3.3-70b-versatile")
        
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        data = {
            "messages": [{"role": "user", "content": prompt}],
            "model": model,
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
        key = self._get_config('HF_API_KEY')
        model = self._get_config('HF_MODEL', "bigcode/starcoder")
        
        url = f"https://router.huggingface.co/models/{model}"
        headers = {"Authorization": f"Bearer {key}"}
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
