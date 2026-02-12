# ============================================
# FILE: parsers/__init__.py
# PURPOSE: Parser factory
# ============================================

from .python_parser import PythonParser
from .javascript_parser import JavascriptParser
from .java_parser import JavaParser
from .go_parser import GoParser
from .csharp_parser import CSharpParser

def get_parser(language):
    """Factory to get appropriate parser"""
    if language == 'python':
        return PythonParser()
    elif language in ['javascript', 'typescript']:
        return JavascriptParser()
    elif language == 'java':
        return JavaParser()
    elif language == 'go':
        return GoParser()
    elif language == 'csharp':
        return CSharpParser()
    return None
