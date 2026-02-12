import json
import re
from app.utils.api_manager import api_client

class AIService:
    @staticmethod
    def _extract_json(text):
        """Extract JSON from text using regex and various fallbacks"""
        try:
            # 1. Strip Markdown
            json_str = text.strip()
            if '```' in json_str:
                # Try to match json block first
                match = re.search(r'```(?:json)?\s*(\{[\s\S]*?\})\s*```', json_str)
                if match:
                    json_str = match.group(1)
                else:
                    # Just find the brace content
                    match = re.search(r'\{[\s\S]*\}', json_str)
                    if match:
                        json_str = match.group(0)
            
            # 2. Try simple parse
            return json.loads(json_str)
        except json.JSONDecodeError:
             # Fallback: Just find the brace content if not already done
             match = re.search(r'\{[\s\S]*\}', text)
             if match:
                 try:
                     return json.loads(match.group(0))
                 except:
                     pass
             raise Exception("Failed to parse AI response as JSON")

    @staticmethod
    def analyze_bugs(code, language):
        prompt = f'''
        Analyze this {language} code for bugs, syntax errors, and logical issues.
        Return ONLY a valid JSON object.
        
        CRITICAL rules for JSON:
        1. Use double quotes for all keys and strings.
        2. Escape all newlines in the 'fixed_code' string with \\n (literal backslash n).
        3. Escape double quotes inside strings with \\".
        4. No trailing commas.
        5. No markdown formatting (just the raw JSON string).
        
        Expected Structure:
        {{
            "issues": ["issue1", "issue2"],
            "fixed_code": "import os\\nwith open('file') as f:\\n    print(f.read())",
            "summary": "Added proper file handling"
        }}
        
        CODE:
        {code}
        '''
        
        response, provider = api_client.generate_content(prompt)
        
        if not response:
             return {"error": "AI Analysis failed", "details": provider}
             
        try:
            data = AIService._extract_json(response)
            data['provider'] = provider
            return data
        except Exception as e:
            return {
                "error": f"Failed to parse AI response: {str(e)}",
                "raw_response": response,
                "provider": provider
            }

    @staticmethod
    def suggest_names(code, func_names, language):
        prompt = f'''
        Analyze the following {language} function names and suggest better, more descriptive names.
        
        CRITICAL: Each suggested name MUST be unique. Do not suggest the same name for different functions.
        
        Current Functions: {func_names}
        
        Code Context (first 2000 chars):
        {code[:2000]}
        
        Return ONLY a valid JSON object.
        CRITICAL rules for JSON:
        1. Use double quotes for all keys and strings.
        2. Escape all newlines in strings with \\n.
        3. No markdown formatting.
        
        Structure:
        {{
            "suggestions": [
                {{"current": "old_name", "suggested": "new_name", "reason": "why this is better"}}
            ]
        }}
        
        If all names are good, return: {{"suggestions": []}}
        '''
        
        response, provider = api_client.generate_content(prompt)
        
        if not response:
             return {"suggestions": [], "error": "AI Analysis failed", "provider": provider}
             
        try:
            data = AIService._extract_json(response)
            return {
                "suggestions": data.get('suggestions', []),
                "provider": provider
            }
        except Exception as e:
             return {
                "suggestions": [], 
                "error": f"Failed to parse AI response: {str(e)}",
                "provider": provider
            }

    @staticmethod
    def suggest_service_names(clusters_map):
        # Prepare cluster data for AI
        cluster_desc = ""
        for cid, fnames in clusters_map.items():
            cluster_desc += f"Cluster {cid}: {', '.join(fnames)}\\n"
        
        prompt = f'''
        I have grouped function names into clusters. Suggest a CamelCase specific microservice name for each cluster.
        Examples: UserService, PaymentService, InventoryService.
        
        Clusters:
        {cluster_desc}
        
        Return ONLY a JSON object mapping Cluster ID to Name:
        {{ "0": "NameService", "1": "AnotherService" }}
        '''
        
        response, provider = api_client.generate_content(prompt)
        
        if not response:
             return {}, provider
             
        try:
            # Reuse extraction logic
            data = AIService._extract_json(response)
            # Normalize keys to int strings if possible, but returning dict is fine
            return data, provider
        except Exception:
            return {}, provider
