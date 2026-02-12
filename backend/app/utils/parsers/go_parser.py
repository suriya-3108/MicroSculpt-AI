# ============================================
# FILE: parsers/go_parser.py
# PURPOSE: Go parser using regex
# ============================================

import re
from .base_parser import BaseParser

class GoParser(BaseParser):
    def parse(self, code):
        """Parse Go code and extract functions"""
        functions = []
        
        # Regex for func: func Name(Args) Type {
        func_regex = r'func\s+([a-zA-Z0-9_]+)\s*\(([^)]*)\)'
        
        # Regex for method: func (r Receiver) Name(Args) Type {
        method_regex = r'func\s+\([^)]+\)\s+([a-zA-Z0-9_]+)\s*\(([^)]*)\)'
        
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            # Standard functions
            match = re.search(func_regex, line)
            if match:
                functions.append({
                    'name': match.group(1),
                    'line': i + 1,
                    'args': [a.strip() for a in match.group(2).split(',') if a.strip()],
                    'type': 'function'
                })
                continue
                
            # Methods
            match = re.search(method_regex, line)
            if match:
                functions.append({
                    'name': match.group(1),
                    'line': i + 1,
                    'args': [a.strip() for a in match.group(2).split(',') if a.strip()],
                    'type': 'method'
                })
                
        return functions

    def get_dependencies(self, code):
        """Extract imports"""
        imports = []
        
        # Single line import
        import_regex = r'import\s+"([^"]+)"'
        for match in re.finditer(import_regex, code):
            imports.append(match.group(1))
            
        # Multi-line imports (simplified detection)
        if 'import (' in code:
            import_block_regex = r'import\s*\(([^)]+)\)'
            block_match = re.search(import_block_regex, code, re.DOTALL)
            if block_match:
                block_content = block_match.group(1)
                for line in block_content.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('//'):
                        # Extract "package/path"
                        m = re.search(r'"([^"]+)"', line)
                        if m:
                            imports.append(m.group(1))
            
        return list(set(imports))
