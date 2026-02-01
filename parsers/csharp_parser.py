# ============================================
# FILE: parsers/csharp_parser.py
# PURPOSE: C# parser using regex
# ============================================

import re
from .base_parser import BaseParser

class CSharpParser(BaseParser):
    def parse(self, code):
        """Parse C# code and extract methods"""
        functions = []
        
        # Regex: public/private type Name(Args)
        method_regex = r'(public|protected|private|internal|static|\s) +[\w\<\>\[\]]+\s+([a-zA-Z0-9_]+)\s*\(([^)]*)\)'
        
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if line.startswith('//') or line.startswith('/*'):
                continue
                
            match = re.search(method_regex, line)
            if match:
                name = match.group(2)
                # Filter keywords
                if name in ['if', 'for', 'foreach', 'while', 'switch', 'using', 'catch']:
                    continue
                    
                functions.append({
                    'name': name,
                    'line': i + 1,
                    'args': [a.strip() for a in match.group(3).split(',') if a.strip()],
                    'type': 'method'
                })
        
        return functions

    def get_dependencies(self, code):
        """Extract usings"""
        imports = []
        using_regex = r'using\s+([\w\.]+);'
        
        for match in re.finditer(using_regex, code):
            imports.append(match.group(1))
            
        return list(set(imports))
