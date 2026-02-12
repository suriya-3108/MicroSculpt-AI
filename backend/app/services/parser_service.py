from app.utils.language_detector import LanguageDetector
from app.utils.parsers import get_parser

class ParserService:
    @staticmethod
    def parse_code(file_name, code_content):
        # 1. Detect Language
        language = LanguageDetector.detect_language(file_name, code_content)
        
        if language == 'unknown':
            return {
                'language': 'unknown',
                'functions': [],
                'error': 'Could not detect language'
            }
            
        # 2. Get Parser
        parser = get_parser(language)
        if not parser:
            return {
                'language': language,
                'functions': [],
                'error': f'Parser not available for {language}'
            }
            
        # 3. Parse
        try:
            functions = parser.parse(code_content)
            return {
                'language': language,
                'functions': functions,
                'count': len(functions)
            }
        except Exception as e:
            return {
                'language': language,
                'functions': [],
                'error': str(e)
            }
