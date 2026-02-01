# ============================================
# FILE: module6_code_generation.py
# PURPOSE: Module 6 - Multi-Language Code Gen
# ============================================

import streamlit as st
import os
import zipfile
import io
from datetime import datetime

class CodeGenerator:
    @staticmethod
    def generate_python_flask(service_name, functions):
        code = f"""from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class {service_name}:
    def health_check(self):
        return {{"status": "healthy", "service": "{service_name}"}}


"""
        # Create lookup map for function bodies
        all_funcs = st.session_state.functions_data
        func_map = {f['name']: f.get('body', '# Body not found') for f in all_funcs}
        
        # Create mapping of old names to new names (if functions were renamed)
        old_to_new_names = {}
        if 'function_renames' in st.session_state:
            for old_name, new_name in st.session_state.function_renames.items():
                old_to_new_names[old_name] = new_name
        
        for func_name in functions:
            # Retrieve original code
            original_body = func_map.get(func_name, "")
            
            # Extract parameters from original function signature
            params = "self"
            if original_body:
                lines = original_body.split('\n')
                if lines and lines[0].strip().startswith("def "):
                    # Extract params: def func_name(param1, param2):
                    import re
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
                import re
                for line in lines:
                    # Replace old function names with new renamed versions
                    modified_line = line
                    for old_name, new_name in old_to_new_names.items():
                        # Match function calls: old_name( but not in strings
                        pattern = r'\b' + re.escape(old_name) + r'\('
                        replacement = new_name + '('
                        modified_line = re.sub(pattern, replacement, modified_line)
                    
                    indented_body += "        " + modified_line + "\n"
            else:
                indented_body = f"        # TODO: Implement business logic for {func_name}\n        return \"{func_name} executed\""


            code += f"""    def {func_name}({params}):
{indented_body or '        pass'}

"""
        code += f"""
service = {service_name}()
"""
        # Rest of the File logic
        code += f"""
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
    result = service.{func}(**data) if isinstance(data, dict) else service.{func}(data)
    return jsonify({{"result": result}})

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
    const result = service.{func}(req.body);
    res.json({{ result }});
}});
"""
        code += """
app.listen(PORT, () => {
    console.log(`Service running on port ${PORT}`);
});
"""
        return code

def render_module6():
    st.header("6️⃣ Microservice Generation")
    
    if 'services' not in st.session_state:
        st.warning("Please group services first.")
        return
        
    services = st.session_state.services
    language = st.session_state.current_language
    
    st.success(f"Ready to generate code for **{language.upper()}** project!")
    
    if st.button("🚀 Generate Code Package", type="primary"):
        # Create ZIP in memory
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            
            # Generate code for each service
            for svc_name, funcs in services.items():
                # Remove duplicate functions (preserves order)
                funcs = list(dict.fromkeys(funcs))
                # Convert CamelCase to snake_case
                # e.g. PaymentService -> payment_service
                import re
                s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', svc_name)
                clean_name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
                
                # Ensure it ends with _service but not _service_service
                if not clean_name.endswith("_service"):
                    folder = f"{clean_name}_service"
                else:
                    folder = clean_name
                
                # Language specific generation
                if language == 'python':
                    # Main App
                    code = CodeGenerator.generate_python_flask(svc_name, funcs)
                    zipf.writestr(f"{folder}/app.py", code)
                    
                    # Dockerfile
                    docker = "FROM python:3.9-slim\nWORKDIR /app\nCOPY . .\nRUN pip install flask flask-cors\nCMD [\"python\", \"app.py\"]"
                    zipf.writestr(f"{folder}/Dockerfile", docker)
                    
                    # Requirements
                    zipf.writestr(f"{folder}/requirements.txt", "flask\nflask-cors")
                    
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
                import re
                s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', svc_name)
                clean_name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
                
                # Ensure it ends with _service but not _service_service
                if not clean_name.endswith("_service"):
                    folder_name = f"{clean_name}_service"
                else:
                    folder_name = clean_name
                
                compose += f"  {clean_name}:\n    build: ./{folder_name}\n    ports:\n      - \"{port}:5000\"\n"
                port += 1
            
            zipf.writestr("docker-compose.yml", compose)
            
            # Readme
            readme = f"""# Generated Microservices
            
Project: {st.session_state.filename}
Language: {language}
Generated: {datetime.now()}

## How to Run
1. Ensure Docker is installed.
2. Run `docker-compose up --build`
3. Access services starting at port 5001.
"""
            zipf.writestr("README.md", readme)

        zip_buffer.seek(0)
        
        # Download Button
        st.download_button(
            label="📥 Download Microservices (.zip)",
            data=zip_buffer,
            file_name=f"microservices_{language}_{datetime.now().strftime('%Y%m%d')}.zip",
            mime="application/zip"
        )
        
        st.balloons()
