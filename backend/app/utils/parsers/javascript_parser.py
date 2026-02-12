# ============================================
# FILE: parsers/javascript_parser.py
# PURPOSE: JavaScript/TypeScript parser using regex/heuristics
# NOTE: For production, a real parser like esprima-python is better, 
# but for now we use regex to avoid heavy dependencies validation issues.
# ============================================

import re
from .base_parser import BaseParser

class JavascriptParser(BaseParser):
    def parse(self, code):
        """Parse JS/TS code and extract functions"""
        functions = []
        
        # Regex for function declarations: function name(args) { ... }
        # Matches: function myFunc(a, b)
        func_regex = r'function\s+([a-zA-Z0-9_]+)\s*\(([^)]*)\)'
        
        # Regex for arrow functions/expressions: const name = (args) => { ... }
        # Matches: const myFunc = (a, b) =>
        arrow_regex = r'(const|let|var)\s+([a-zA-Z0-9_]+)\s*=\s*(\([^)]*\)|[a-zA-Z0-9_]+)\s*=>'
        
        # Regex for method definitions: name(args) { ... } inside classes (simplified)
        method_regex = r'([a-zA-Z0-9_]+)\s*\(([^)]*)\)\s*{'
        
        lines = code.split('\n')
        
        lines = code.split('\n')
        
        # Helper to extract body by counting braces starting from a line
        def extract_body(start_index, line_content):
            # Find the first opening brace `{` in the start line
            # If not found, look ahead. This is a simplified approach.
            open_brace = line_content.find('{')
            if open_brace == -1:
                return "    // Body extraction failed (complex syntax)"
            
            brace_count = 0
            body_lines = []
            param_started = False
            
            # Simple line-by-line scanner starting from this line
            for i in range(start_index, len(lines)):
                line = lines[i]
                current_line_text = line
                
                # If it's the first line, strip anything before the opening brace if extracting just body
                # But we want the whole function usually. 
                # Let's simple capture everything from start line to end line.
                
                for char in line:
                    if char == '{':
                        brace_count += 1
                        param_started = True
                    elif char == '}':
                        brace_count -= 1
                
                body_lines.append(line)
                
                if param_started and brace_count == 0:
                    return "\n".join(body_lines)
            
            return "\n".join(body_lines) # Return what we found

        for i, line in enumerate(lines):
            # Check standard functions
            match = re.search(func_regex, line)
            if match:
                functions.append({
                    'name': match.group(1),
                    'line': i + 1,
                    'args': [a.strip() for a in match.group(2).split(',') if a.strip()],
                    'type': 'function',
                    'body': extract_body(i, line)
                })
                continue
                
            # Check arrow functions
            match = re.search(arrow_regex, line)
            if match:
                args_raw = match.group(3).replace('(', '').replace(')', '')
                functions.append({
                    'name': match.group(2),
                    'line': i + 1,
                    'args': [a.strip() for a in args_raw.split(',') if a.strip()],
                    'type': 'arrow',
                    'body': extract_body(i, line)
                })
        
        # Determine internal calls (naive approach)
        func_names = [f['name'] for f in functions]
        for func in functions:
            func['calls'] = []
            # Look for calls in the code (simple string matching)
            for other_func in func_names:
                if other_func != func['name'] and other_func + '(' in func['body']:
                    func['calls'].append(other_func) 
            
        return functions

    def get_dependencies(self, code):
        """Extract imports"""
        imports = []
        
        # import X from 'Y'
        import_regex = r'import\s+.*\s+from\s+[\'"]([^\'"]+)[\'"]'
        # const X = require('Y')
        require_regex = r'require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)'
        
        for match in re.finditer(import_regex, code):
            imports.append(match.group(1))
            
        for match in re.finditer(require_regex, code):
            imports.append(match.group(1))
            
        return list(set(imports))
