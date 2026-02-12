# ============================================
# FILE: parsers/python_parser.py
# PURPOSE: Enhanced Python code parser
# ============================================

import ast
from .base_parser import BaseParser

class PythonParser(BaseParser):
    def parse(self, code):
        """Parse Python code and extract functions"""
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return {'error': f"Syntax error: {e}"}
            
        functions = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Extract called functions
                calls = []
                for child in ast.walk(node):
                    if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                        calls.append(child.func.id)
                
                func_info = {
                    'name': node.name,
                    'line': node.lineno,
                    'args': [arg.arg for arg in node.args.args],
                    'has_return': any(isinstance(n, ast.Return) for n in ast.walk(node)),
                    'calls': calls,
                    'body': ast.get_source_segment(code, node) or ""
                }
                functions.append(func_info)
                
        return functions

    def get_dependencies(self, code):
        """Extract imports"""
        try:
            tree = ast.parse(code)
        except:
            return []
            
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    imports.append(name.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
                    
        return list(set(imports))
