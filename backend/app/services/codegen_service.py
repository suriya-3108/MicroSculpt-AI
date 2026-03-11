import zipfile
import io
import re
from datetime import datetime

class CodeGenerator:
    @staticmethod
    def _extract_imports(code_body):
        """Extract import statements from original code body"""
        imports = set()
        if not code_body:
            return imports
        for line in code_body.split('\n'):
            stripped = line.strip()
            if stripped.startswith('import ') or stripped.startswith('from '):
                imports.add(stripped)
        return imports

    @staticmethod
    def _extract_file_imports(source_code):
        """Extract top-level import statements from the original source file"""
        imports = set()
        if not source_code:
            return imports
        for line in source_code.split('\n'):
            stripped = line.strip()
            # Only grab top-level imports (not indented ones inside functions)
            if (line.startswith('import ') or line.startswith('from ')) and not line.startswith(' '):
                imports.add(stripped)
        return imports

    @staticmethod
    def _collect_service_imports(functions, all_funcs, source_code=''):
        """Collect all imports needed by the functions in this service from the full source"""
        # Extract from the top-level source code (much more reliable than scanning bodies)
        imports = set()
        if source_code:
            imports = CodeGenerator._extract_file_imports(source_code)
        # Remove flask/requests imports since we add those ourselves
        imports = {imp for imp in imports
                   if not imp.startswith('from flask')
                   and 'flask_cors' not in imp
                   and imp != 'import requests'}
        return sorted(imports)

    @staticmethod
    def generate_python_flask(service_name, functions, all_funcs, renames_map, all_services=None, source_code=''):
        # Collect imports from the original source file
        extra_imports = CodeGenerator._collect_service_imports(functions, all_funcs, source_code)
        import_block = '\n'.join(extra_imports)
        if import_block:
            import_block = '\n' + import_block + '\n'

        # Build cross-service lookup: function_name -> (service_folder, port)
        cross_service_map = {}
        if all_services:
            port = 5001
            for svc_name, svc_funcs in all_services.items():
                s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', svc_name)
                svc_host = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
                if not svc_host.endswith('_service'):
                    svc_host += '_service'
                for fn in svc_funcs:
                    if fn not in functions:  # Only external functions
                        cross_service_map[fn] = (svc_host, port)
                port += 1

        # Build parameter names map for ALL functions to use as JSON keys
        param_names_map = {}
        for f in all_funcs:
            f_name = f['name']
            f_body = f.get('body', '')
            if f_body:
                # Extract original params from def line
                match = re.search(r'def\s+\w+\((.*?)\)', f_body)
                if match:
                    p_str = match.group(1).strip()
                    # Filter out 'self' and split by comma
                    p_list = [p.strip().split('=')[0].strip() for p in p_str.split(',') if p.strip() and p.strip() != 'self']
                    param_names_map[f_name] = p_list

        code = f"""from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
{import_block}
app = Flask(__name__)
CORS(app)

class {service_name}:
    def health_check(self):
        return {{"status": "healthy", "service": "{service_name}"}}


"""
        # Create lookup map for function bodies
        func_map = {f['name']: f.get('body', '# Body not found') for f in all_funcs}
        
        # Create mapping of old names to new names (if functions were renamed)
        old_to_new_names = renames_map or {}
        
        for func_name in functions:
            # Retrieve original code
            original_body = func_map.get(func_name, "")
            
            # Extract parameters from original function signature
            params = "self"
            if original_body:
                lines = original_body.split('\n')
                if lines and lines[0].strip().startswith("def "):
                    match = re.search(r'def\s+\w+\((.*?)\)', lines[0])
                    if match:
                        original_params = match.group(1).strip()
                        if original_params:
                            params = f"self, {original_params}"
            
            # Indent logic (4 spaces) and replace old function names
            indented_body = ""
            if original_body:
                lines = original_body.split('\n')
                # Remove def line if present (we created our own)
                if lines[0].strip().startswith("def "):
                    lines = lines[1:]
                
                # Re-indent and replace old function names with new ones
                service_functions = set(functions)
                
                for line in lines:
                    # Replace old function names with new renamed versions
                    modified_line = line
                    for old_name, new_name in old_to_new_names.items():
                        # Match function calls: old_name( but not in strings
                        pattern = r'\b' + re.escape(old_name) + r'\('
                        replacement = new_name + '('
                        modified_line = re.sub(pattern, replacement, modified_line)
                    
                    # Add self. prefix for same-service method calls
                    for service_func in service_functions:
                         # Match: service_func( but NOT self.service_func( or module.service_func(
                        pattern = r'(?<!self\.)(?<!\.)(?<!def\s)\b' + re.escape(service_func) + r'\('
                        replacement = f'self.{service_func}('
                        modified_line = re.sub(pattern, replacement, modified_line)
                    
                    # Replace cross-service calls with HTTP requests
                    if cross_service_map:
                        for ext_func, (svc_host, svc_port) in cross_service_map.items():
                            # Match: ext_func(args) capturing the args group
                            pattern = r'(?<!self\.)(?<!\.)(?<!def\s)\b' + re.escape(ext_func) + r'\(([^)]*)\)'
                            # Use a callback so we can properly use the captured args group
                            def make_http_replacer(host, port, fname):
                                def replacer(m):
                                    args_str = m.group(1).strip()
                                    if args_str:
                                        # Split args by comma, ignoring commas inside parentheses/brackets
                                        # (Simple regex splitting for balanced parens)
                                        arg_parts = []
                                        depth = 0
                                        current = ""
                                        for char in args_str:
                                            if char == ',' and depth == 0:
                                                arg_parts.append(current.strip())
                                                current = ""
                                            else:
                                                if char in '([{': depth += 1
                                                if char in ')]}': depth -= 1
                                                current += char
                                        if current:
                                            arg_parts.append(current.strip())
                                        
                                        # Get original parameter names for the target function
                                        target_params = param_names_map.get(fname, [])
                                        
                                        pairs = []
                                        for i, val in enumerate(arg_parts):
                                            # Use param name if we have it, else fallback to argN
                                            if i < len(target_params):
                                                key = target_params[i]
                                            else:
                                                key = f"arg{i+1}"
                                            pairs.append(f'"{key}": {val}')
                                        
                                        json_payload = '{' + ', '.join(pairs) + '}'
                                    else:
                                        json_payload = '{}'
                                    return f'requests.post("http://{host}:{port}/{fname}", json={json_payload}).json().get("result")'
                                return replacer
                            modified_line = re.sub(pattern, make_http_replacer(svc_host, svc_port, ext_func), modified_line)
                    
                    indented_body += "        " + modified_line + "\n"
            else:
                indented_body = f"        # TODO: Implement business logic for {func_name}\n        return \"{func_name} executed\""


            code += f"""    def {func_name}({params}):
{indented_body or '        pass'}

"""
        code += f"""
service = {service_name}()

@app.route('/health', methods=['GET'])
def health():
    return jsonify(service.health_check())

"""
        for func in functions:
            code += f"""@app.route('/{func}', methods=['POST'])
def api_{func}():
    data = request.json
    # Pass data as kwargs or however the original function expects it
    # Simplified mapping:
    try:
        if isinstance(data, dict):
             result = service.{func}(**data)
        else:
             result = service.{func}(data)
        return jsonify({{"result": result}})
    except TypeError as te:
        return jsonify({{"error": f"Invalid arguments: {{str(te)}}"}}), 400
    except Exception as e:
        return jsonify({{"error": str(e)}}), 500

"""
        code += """
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
"""
        return code

    @staticmethod
    def generate_nodejs_express(service_name, functions):
        code = f"""const express = require('express');
const cors = require('cors');
const app = express();
const PORT = 5000;

app.use(cors());
app.use(express.json());

class {service_name} {{
    healthCheck() {{
        return {{ status: 'healthy', service: '{service_name}' }};
    }}
"""
        for func in functions:
            code += f"""
    {func}(data) {{
        // TODO: Implement logic for {func}
        return `{func} executed`;
    }}
"""
        code += f"""}}

const service = new {service_name}();

app.get('/health', (req, res) => {{
    res.json(service.healthCheck());
}});
"""
        for func in functions:
            code += f"""
app.post('/{func}', (req, res) => {{
    try {{
        const result = service.{func}(req.body);
        res.json({{ result }});
    }} catch (e) {{
        res.status(500).json({{ error: e.message }});
    }}
}});
"""
        code += """
app.listen(PORT, () => {
    console.log(`Service running on port ${PORT}`);
});
"""
        return code

class CodegenService:
    @staticmethod
    def generate_code_package(services, language, functions_data, renames_map, source_filename, source_code=''):
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            
            # Generate code for each service
            for svc_name, funcs in services.items():
                # Remove duplicate functions (preserves order)
                funcs = list(dict.fromkeys(funcs))
                
                # Convert CamelCase to snake_case for folder
                s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', svc_name)
                clean_name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
                
                # Ensure it ends with _service but not _service_service
                if not clean_name.endswith("_service"):
                    folder = f"{clean_name}_service"
                else:
                    folder = clean_name
                
                # Language specific generation
                if language == 'python':
                    # Main App — pass source_code for top-level import extraction
                    code = CodeGenerator.generate_python_flask(svc_name, funcs, functions_data, renames_map, all_services=services, source_code=source_code)
                    zipf.writestr(f"{folder}/app.py", code)
                    
                    # Dockerfile
                    docker = "FROM python:3.9-slim\nWORKDIR /app\nCOPY . .\nRUN pip install flask flask-cors requests\nCMD [\"python\", \"app.py\"]"
                    zipf.writestr(f"{folder}/Dockerfile", docker)
                    
                    # Requirements
                    zipf.writestr(f"{folder}/requirements.txt", "flask\nflask-cors\nrequests")
                    
                elif language in ['javascript', 'typescript']:
                    # Main App
                    code = CodeGenerator.generate_nodejs_express(svc_name, funcs)
                    zipf.writestr(f"{folder}/index.js", code)
                    
                    # Dockerfile
                    docker = "FROM node:18-alpine\nWORKDIR /app\nCOPY . .\nRUN npm install express cors\nCMD [\"node\", \"index.js\"]"
                    zipf.writestr(f"{folder}/Dockerfile", docker)
                    
                    # Package.json
                    pkg = f'{{"name": "{clean_name}", "dependencies": {{"express": "^4.18.2", "cors": "^2.8.5"}}}}'
                    zipf.writestr(f"{folder}/package.json", pkg)
                    
            # Docker Compose
            compose = "version: '3.8'\nservices:\n"
            port = 5001
            for svc_name in services:
                # Use same snake_case conversion as folder creation
                s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', svc_name)
                clean_name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
                
                if not clean_name.endswith("_service"):
                    folder_name = f"{clean_name}_service"
                else:
                    folder_name = clean_name
                
                compose += f"  {clean_name}:\n    build: ./{folder_name}\n    ports:\n      - \"{port}:5000\"\n"
                port += 1
            
            zipf.writestr("docker-compose.yml", compose)
            
            # Readme
            readme = f"""# Generated Microservices
            
Project: {source_filename}
Language: {language}
Generated: {datetime.now()}

## How to Run
1. Ensure Docker is installed.
2. Run `docker-compose up --build`
3. Access services starting at port 5001.
"""
            zipf.writestr("README.md", readme)

        zip_buffer.seek(0)
        return zip_buffer
