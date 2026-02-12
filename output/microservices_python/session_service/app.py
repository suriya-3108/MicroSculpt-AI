from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class SessionService:
    def health_check(self):
        return {"status": "healthy", "service": "SessionService"}


    def create_user_session(self, user_id):
            """Create a new session for authenticated user"""
            import random
            session_token = f"session_{user_id}_{random.randint(1000, 9999)}"
            return session_token



service = SessionService()

@app.route('/health', methods=['GET'])
def health():
    return jsonify(service.health_check())

@app.route('/create_user_session', methods=['POST'])
def api_create_user_session():
    data = request.json
    # Pass data as kwargs or however the original function expects it
    # Simplified mapping:
    try:
        if isinstance(data, dict):
             result = service.create_user_session(**data)
        else:
             result = service.create_user_session(data)
        return jsonify({"result": result})
    except TypeError:
        # Fallback if args don't match
        return jsonify({"result": service.create_user_session()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
