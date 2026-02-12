# ============================================
# FILE: parsers/java_parser.py
# PURPOSE: Java parser using regex
# ============================================

import re
from .base_parser import BaseParser

class JavaParser(BaseParser):
    def parse(self, code):
        """Parse Java code and extract methods"""
        functions = []
        
        # Regex for method: public/private/protected [static] Type name(Args) {
        method_regex = r'(public|protected|private|static|\s) +[\w\<\>\[\]]+\s+([a-zA-Z0-9_]+)\s*\(([^)]*)\)\s*(\{|throws)'
        
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            # Skip comments
            if line.strip().startswith('//') or line.strip().startswith('*'):
                continue
                
            match = re.search(method_regex, line)
            if match:
                # Filter out keywords like 'if', 'for', 'while' if regex picked them up
                name = match.group(2)
                if name in ['if', 'for', 'while', 'switch', 'catch']:
                    continue
                    
                functions.append({
                    'name': name,
                    'line': i + 1,
                    'args': [a.strip() for a in match.group(3).split(',') if a.strip()],
                    'type': 'method'
                })
        
        return functions

    def get_dependencies(self, code):
        """Extract imports"""
        imports = []
        import_regex = r'import\s+([\w\.]+);'
        
        for match in re.finditer(import_regex, code):
            imports.append(match.group(1))
            
        return list(set(imports))
