from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

from datetime import datetime, timedelta
from decimal import Decimal
import hashlib
import json
import os
import random

app = Flask(__name__)
CORS(app)

class AccountCreationService:
    def health_check(self):
        return {"status": "healthy", "service": "AccountCreationService"}


    def create_new_user_account(self, name, email, initial_balance=0.0):
            """Create a new user account"""
            user_id = requests.post("http://user_data_service:5005/create_unique_user_identifier", json={"name": name}).json().get("result")
            user = {
                "id": user_id,
                "name": name,
                "email": email,
                "balance": initial_balance,
                "created_at": datetime.now().isoformat(),
                "status": "active"
            }
            requests.post("http://user_data_service:5005/store_user_data", json={"user": user}).json().get("result")
            requests.post("http://user_data_service:5005/send_new_user_welcome_notification", json={"email": email, "name": name}).json().get("result")
            requests.post("http://account_management_service:5002/record_user_activity", json={"user_id": user_id, "action": "account_created"}).json().get("result")
            return user



service = AccountCreationService()

@app.route('/health', methods=['GET'])
def health():
    return jsonify(service.health_check())

@app.route('/create_new_user_account', methods=['POST'])
def api_create_new_user_account():
    data = request.json
    # Pass data as kwargs or however the original function expects it
    # Simplified mapping:
    try:
        if isinstance(data, dict):
             result = service.create_new_user_account(**data)
        else:
             result = service.create_new_user_account(data)
        return jsonify({"result": result})
    except TypeError as te:
        return jsonify({"error": f"Invalid arguments: {str(te)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
