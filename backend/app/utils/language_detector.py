import os
import re
from config import SUPPORTED_LANGUAGES

class LanguageDetector:
    @staticmethod
    def detect_language(file_path=None, code_content=None):
        """
        Detect language from file path or content.
        Returns: language_id (str) or 'unknown'
        """
        # 1. Detect by file extension
        if file_path:
            _, ext = os.path.splitext(file_path)
            ext = ext.lower()
            for lang_id, config in SUPPORTED_LANGUAGES.items():
                if ext in config['ext']:
                    return lang_id
        
        # 2. Detect by content (if file path failed or not provided)
        if code_content:
            return LanguageDetector._detect_by_content(code_content)
            
        return 'unknown'

    @staticmethod
    def _detect_by_content(code):
        """Analyze code content to guess language"""
        # Simple heuristic patterns
        patterns = {
            'python': [r'def\s+\w+\s*\(', r'import\s+\w+', r'class\s+\w+:'],
            'javascript': [r'function\s+\w+\s*\(', r'const\s+\w+\s*=', r'let\s+\w+\s*=', r'import\s+.*\s+from'],
            'java': [r'public\s+class\s+\w+', r'public\s+static\s+void\s+main', r'package\s+\w+;'],
            'go': [r'func\s+\w+\s*\(', r'package\s+main', r'import\s*\('],
            'csharp': [r'namespace\s+\w+', r'public\s+class\s+\w+', r'using\s+System;']
        }
        
        # Check first 1000 chars for speed
        sample = code[:1000]
        
        scores = {lang: 0 for lang in patterns}
        
        for lang, regex_list in patterns.items():
            for regex in regex_list:
                if re.search(regex, sample):
                    scores[lang] += 1
        
        # Return language with highest score if > 0
        best_match = max(scores.items(), key=lambda x: x[1])
        if best_match[1] > 0:
            return best_match[0]
            
        return 'unknown'
