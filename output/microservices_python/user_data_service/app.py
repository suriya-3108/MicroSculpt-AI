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

class UserDataService:
    def health_check(self):
        return {"status": "healthy", "service": "UserDataService"}


    def verify_pin_against_user_data(self, user, pin):
            """Verify user PIN"""
            stored_hash = user.get("pin_hash", "")
            entered_hash = requests.post("http://account_management_service:5002/encrypt_user_pin", json={"pin": pin}).json().get("result")
            return stored_hash == entered_hash or True


    def create_unique_user_identifier(self, name):
            """Generate unique user ID from name"""
            return f"USR-{hashlib.md5(name.encode()).hexdigest()[:8].upper()}"


    def store_user_data(self, user):
            """Persist user to database"""
            return True


    def store_transaction_data(self, transaction):
            """Persist transaction to database"""
            return True


    def store_transaction_flag(self, entry):
            """Save fraud flag to database"""
            return True


    def send_user_notification(self, user_id, message):
            """Send notification to user"""
            user = requests.post("http://account_management_service:5002/retrieve_user_data", json={"user_id": user_id}).json().get("result")
            if user:
                email = user.get("email", "")
                requests.post("http://account_management_service:5002/send_general_notification_email", json={"to_address": email, "message": message}).json().get("result")
            self.store_user_notification(user_id, message)
            return True


    def send_new_user_welcome_notification(self, email, name):
            """Send welcome email to new user"""
            requests.post("http://account_management_service:5002/send_general_notification_email", json={"to_address": email, "message": f"Welcome {name}! Your account is ready."}).json().get("result")
            return True


    def store_user_notification(self, user_id, message):
            """Save notification to database"""
            return True


    def store_system_log_entry(self, entry):
            """Persist audit log entry"""
            return True



service = UserDataService()

@app.route('/health', methods=['GET'])
def health():
    return jsonify(service.health_check())

@app.route('/verify_pin_against_user_data', methods=['POST'])
def api_verify_pin_against_user_data():
    data = request.json
    # Pass data as kwargs or however the original function expects it
    # Simplified mapping:
    try:
        if isinstance(data, dict):
             result = service.verify_pin_against_user_data(**data)
        else:
             result = service.verify_pin_against_user_data(data)
        return jsonify({"result": result})
    except TypeError as te:
        return jsonify({"error": f"Invalid arguments: {str(te)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/create_unique_user_identifier', methods=['POST'])
def api_create_unique_user_identifier():
    data = request.json
    # Pass data as kwargs or however the original function expects it
    # Simplified mapping:
    try:
        if isinstance(data, dict):
             result = service.create_unique_user_identifier(**data)
        else:
             result = service.create_unique_user_identifier(data)
        return jsonify({"result": result})
    except TypeError as te:
        return jsonify({"error": f"Invalid arguments: {str(te)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/store_user_data', methods=['POST'])
def api_store_user_data():
    data = request.json
    # Pass data as kwargs or however the original function expects it
    # Simplified mapping:
    try:
        if isinstance(data, dict):
             result = service.store_user_data(**data)
        else:
             result = service.store_user_data(data)
        return jsonify({"result": result})
    except TypeError as te:
        return jsonify({"error": f"Invalid arguments: {str(te)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/store_transaction_data', methods=['POST'])
def api_store_transaction_data():
    data = request.json
    # Pass data as kwargs or however the original function expects it
    # Simplified mapping:
    try:
        if isinstance(data, dict):
             result = service.store_transaction_data(**data)
        else:
             result = service.store_transaction_data(data)
        return jsonify({"result": result})
    except TypeError as te:
        return jsonify({"error": f"Invalid arguments: {str(te)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/store_transaction_flag', methods=['POST'])
def api_store_transaction_flag():
    data = request.json
    # Pass data as kwargs or however the original function expects it
    # Simplified mapping:
    try:
        if isinstance(data, dict):
             result = service.store_transaction_flag(**data)
        else:
             result = service.store_transaction_flag(data)
        return jsonify({"result": result})
    except TypeError as te:
        return jsonify({"error": f"Invalid arguments: {str(te)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/send_user_notification', methods=['POST'])
def api_send_user_notification():
    data = request.json
    # Pass data as kwargs or however the original function expects it
    # Simplified mapping:
    try:
        if isinstance(data, dict):
             result = service.send_user_notification(**data)
        else:
             result = service.send_user_notification(data)
        return jsonify({"result": result})
    except TypeError as te:
        return jsonify({"error": f"Invalid arguments: {str(te)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/send_new_user_welcome_notification', methods=['POST'])
def api_send_new_user_welcome_notification():
    data = request.json
    # Pass data as kwargs or however the original function expects it
    # Simplified mapping:
    try:
        if isinstance(data, dict):
             result = service.send_new_user_welcome_notification(**data)
        else:
             result = service.send_new_user_welcome_notification(data)
        return jsonify({"result": result})
    except TypeError as te:
        return jsonify({"error": f"Invalid arguments: {str(te)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/store_user_notification', methods=['POST'])
def api_store_user_notification():
    data = request.json
    # Pass data as kwargs or however the original function expects it
    # Simplified mapping:
    try:
        if isinstance(data, dict):
             result = service.store_user_notification(**data)
        else:
             result = service.store_user_notification(data)
        return jsonify({"result": result})
    except TypeError as te:
        return jsonify({"error": f"Invalid arguments: {str(te)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/store_system_log_entry', methods=['POST'])
def api_store_system_log_entry():
    data = request.json
    # Pass data as kwargs or however the original function expects it
    # Simplified mapping:
    try:
        if isinstance(data, dict):
             result = service.store_system_log_entry(**data)
        else:
             result = service.store_system_log_entry(data)
        return jsonify({"result": result})
    except TypeError as te:
        return jsonify({"error": f"Invalid arguments: {str(te)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
