from flask import Blueprint, jsonify, request
import os
import json

bp = Blueprint('api', __name__)

@bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'message': 'MicroSculpt AI Backend Running'})

# Placeholder headers for routes - implementation will be added in subsequent steps
from app.services.parser_service import ParserService

# /api/parse
@bp.route('/parse', methods=['POST'])
def parse_code():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
        
    code_content = data.get('code')
    file_name = data.get('fileName')
    
    if not code_content:
        return jsonify({'error': 'No code content provided'}), 400
        
    result = ParserService.parse_code(file_name, code_content)
    return jsonify(result)

# /api/analyze-bugs
# /api/suggest-names
from app.services.ai_service import AIService

@bp.route('/analyze-bugs', methods=['POST'])
def analyze_bugs():
    data = request.json
    code = data.get('code')
    language = data.get('language')
    
    if not code or not language:
        return jsonify({'error': 'Missing code or language'}), 400
        
    result = AIService.analyze_bugs(code, language)
    return jsonify(result)

@bp.route('/suggest-names', methods=['POST'])
def suggest_names():
    data = request.json
    code = data.get('code')
    language = data.get('language')
    func_names = data.get('functions', []) # List of function names
    
    if not code or not language:
        return jsonify({'error': 'Missing code or language'}), 400
        
    result = AIService.suggest_names(code, func_names, language)
    return jsonify(result)

# /api/dependency-graph
from app.services.graph_service import GraphService

@bp.route('/dependency-graph', methods=['POST'])
def dependency_graph():
    data = request.json
    functions = data.get('functions', [])
    
    if not functions:
        return jsonify({'error': 'No functions data provided'}), 400
        
    result = GraphService.generate_graph(functions)
    return jsonify(result)

# /api/group-services
from app.services.clustering_service import ClusteringService

@bp.route('/group-services', methods=['POST'])
def group_services():
    data = request.json
    functions = data.get('functions', [])
    
    if not functions:
        return jsonify({'error': 'No functions data provided'}), 400
        
    result = ClusteringService.group_services(functions)
    return jsonify(result)

# /api/generate-code
from app.services.codegen_service import CodegenService
from flask import send_file

@bp.route('/generate-code', methods=['POST'])
def generate_code():
    data = request.json
    services = data.get('services', {})
    language = data.get('language', 'python')
    functions_data = data.get('functions', []) # With bodies
    renames = data.get('renames', {})
    filename = data.get('filename', 'project')
    source_code = data.get('source_code', '')  # Original source for import extraction
    
    if not services:
        return jsonify({'error': 'No services data provided'}), 400
        
    zip_buffer = CodegenService.generate_code_package(services, language, functions_data, renames, filename, source_code)
    
    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name=f'microservices_{language}.zip'
    )
