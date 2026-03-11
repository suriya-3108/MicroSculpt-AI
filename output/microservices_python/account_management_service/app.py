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

class AccountManagementService:
    def health_check(self):
        return {"status": "healthy", "service": "AccountManagementService"}


    def authenticate_user_credentials(self, user_id, pin):
            """Validate user identity and PIN"""
            if not user_id or not pin:
                return False
            user = self.retrieve_user_data(user_id)
            if not user:
                return False
            return requests.post("http://user_data_service:5005/verify_pin_against_user_data", json={"user": user, "pin": pin}).json().get("result")


    def retrieve_user_data(self, user_id):
            """Fetch user from database"""
            return {"id": user_id, "name": "John Doe", "status": "active", "balance": 1000.00}


    def encrypt_user_pin(self, pin):
            """Hash a PIN using SHA-256"""
            return hashlib.sha256(str(pin).encode()).hexdigest()


    def retrieve_user_account_balance(self, user_id):
            """Get current account balance"""
            user = self.retrieve_user_data(user_id)
            if not user:
                return {"error": "User not found"}
            return {"balance": user["balance"], "user_id": user_id}


    def modify_user_account_balance(self, user_id, amount, operation):
            """Update user balance for debit or credit"""
            user = self.retrieve_user_data(user_id)
            if not user:
                return {"error": "User not found"}
            if operation == "debit":
                if user["balance"] < amount:
                    return {"error": "Insufficient funds"}
                user["balance"] -= amount
            elif operation == "credit":
                user["balance"] += amount
            requests.post("http://user_data_service:5005/store_user_data", json={"user": user}).json().get("result")
            self.record_user_activity(user_id, f"balance_{operation}:{amount}")
            return {"success": True, "new_balance": user["balance"]}


    def deactivate_user_account(self, user_id, reason):
            """Freeze a user account"""
            user = self.retrieve_user_data(user_id)
            if not user:
                return {"error": "User not found"}
            user["status"] = "frozen"
            user["freeze_reason"] = reason
            requests.post("http://user_data_service:5005/store_user_data", json={"user": user}).json().get("result")
            requests.post("http://user_data_service:5005/send_user_notification", json={"user_id": user_id, "message": f"Your account has been frozen: {reason}"}).json().get("result")
            self.record_user_activity(user_id, f"account_frozen:{reason}")
            return {"success": True}


    def generate_unique_transaction_identifier(self):
            """Generate a unique transaction ID"""
            return f"TXN-{random.randint(100000, 999999)}-{datetime.now().strftime('%Y%m%d')}"


    def log_transaction_data(self, txn_id, sender_id, receiver_id, amount, status):
            """Store transaction record"""
            transaction = {
                "id": txn_id,
                "sender_id": sender_id,
                "receiver_id": receiver_id,
                "amount": amount,
                "status": status,
                "timestamp": datetime.now().isoformat()
            }
            requests.post("http://user_data_service:5005/store_transaction_data", json={"transaction": transaction}).json().get("result")
            return transaction


    def retrieve_user_transaction_history(self, user_id, limit=10):
            """Get recent transactions for a user"""
            transactions = requests.post("http://transaction_data_service:5004/fetch_transaction_data", json={"user_id": user_id}).json().get("result")
            sorted_txns = sorted(transactions, key=lambda t: t["timestamp"], reverse=True)
            return sorted_txns[:limit]


    def identify_potential_fraudulent_activity(self, user_id, amount, receiver_id):
            """Run fraud checks on a transaction"""
            risk_score = self.calculate_transaction_risk_score(user_id, amount)
            if risk_score > 80:
                self.mark_transaction_as_suspicious(user_id, amount, "high_risk")
                requests.post("http://user_data_service:5005/send_user_notification", json={"user_id": user_id, "message": "Suspicious activity detected on your account"}).json().get("result")
                self.record_user_activity(user_id, f"fraud_flag:score={risk_score}")
                return {"flagged": True, "risk_score": risk_score}
            return {"flagged": False, "risk_score": risk_score}


    def calculate_transaction_risk_score(self, user_id, amount):
            """Calculate a fraud risk score"""
            history = self.retrieve_user_transaction_history(user_id)
            avg_amount = sum(t["amount"] for t in history) / len(history) if history else 0
            score = 0
            if amount > avg_amount * 3:
                score += 40
            if len(history) < 3:
                score += 30
            return min(score, 100)


    def mark_transaction_as_suspicious(self, user_id, amount, reason):
            """Flag a transaction for review"""
            entry = {
                "user_id": user_id,
                "amount": amount,
                "reason": reason,
                "flagged_at": datetime.now().isoformat()
            }
            requests.post("http://user_data_service:5005/store_transaction_flag", json={"entry": entry}).json().get("result")
            return True


    def send_general_notification_email(self, to_address, message):
            """Send email to an address"""
            return True


    def record_user_activity(self, user_id, action):
            """Log a user action for audit trail"""
            entry = {
                "user_id": user_id,
                "action": action,
                "timestamp": datetime.now().isoformat(),
                "ip": "0.0.0.0"
            }
            requests.post("http://user_data_service:5005/store_system_log_entry", json={"entry": entry}).json().get("result")
            return True


    def retrieve_system_audit_log(self, user_id):
            """Retrieve full audit trail for a user"""
            logs = self.fetch_system_log_data(user_id)
            return sorted(logs, key=lambda l: l["timestamp"], reverse=True)


    def fetch_system_log_data(self, user_id):
            """Load logs from database"""
            return []



service = AccountManagementService()

@app.route('/health', methods=['GET'])
def health():
    return jsonify(service.health_check())

@app.route('/authenticate_user_credentials', methods=['POST'])
def api_authenticate_user_credentials():
    data = request.json
    # Pass data as kwargs or however the original function expects it
    # Simplified mapping:
    try:
        if isinstance(data, dict):
             result = service.authenticate_user_credentials(**data)
        else:
             result = service.authenticate_user_credentials(data)
        return jsonify({"result": result})
    except TypeError as te:
        return jsonify({"error": f"Invalid arguments: {str(te)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/retrieve_user_data', methods=['POST'])
def api_retrieve_user_data():
    data = request.json
    # Pass data as kwargs or however the original function expects it
    # Simplified mapping:
    try:
        if isinstance(data, dict):
             result = service.retrieve_user_data(**data)
        else:
             result = service.retrieve_user_data(data)
        return jsonify({"result": result})
    except TypeError as te:
        return jsonify({"error": f"Invalid arguments: {str(te)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/encrypt_user_pin', methods=['POST'])
def api_encrypt_user_pin():
    data = request.json
    # Pass data as kwargs or however the original function expects it
    # Simplified mapping:
    try:
        if isinstance(data, dict):
             result = service.encrypt_user_pin(**data)
        else:
             result = service.encrypt_user_pin(data)
        return jsonify({"result": result})
    except TypeError as te:
        return jsonify({"error": f"Invalid arguments: {str(te)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/retrieve_user_account_balance', methods=['POST'])
def api_retrieve_user_account_balance():
    data = request.json
    # Pass data as kwargs or however the original function expects it
    # Simplified mapping:
    try:
        if isinstance(data, dict):
             result = service.retrieve_user_account_balance(**data)
        else:
             result = service.retrieve_user_account_balance(data)
        return jsonify({"result": result})
    except TypeError as te:
        return jsonify({"error": f"Invalid arguments: {str(te)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/modify_user_account_balance', methods=['POST'])
def api_modify_user_account_balance():
    data = request.json
    # Pass data as kwargs or however the original function expects it
    # Simplified mapping:
    try:
        if isinstance(data, dict):
             result = service.modify_user_account_balance(**data)
        else:
             result = service.modify_user_account_balance(data)
        return jsonify({"result": result})
    except TypeError as te:
        return jsonify({"error": f"Invalid arguments: {str(te)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/deactivate_user_account', methods=['POST'])
def api_deactivate_user_account():
    data = request.json
    # Pass data as kwargs or however the original function expects it
    # Simplified mapping:
    try:
        if isinstance(data, dict):
             result = service.deactivate_user_account(**data)
        else:
             result = service.deactivate_user_account(data)
        return jsonify({"result": result})
    except TypeError as te:
        return jsonify({"error": f"Invalid arguments: {str(te)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate_unique_transaction_identifier', methods=['POST'])
def api_generate_unique_transaction_identifier():
    data = request.json
    # Pass data as kwargs or however the original function expects it
    # Simplified mapping:
    try:
        if isinstance(data, dict):
             result = service.generate_unique_transaction_identifier(**data)
        else:
             result = service.generate_unique_transaction_identifier(data)
        return jsonify({"result": result})
    except TypeError as te:
        return jsonify({"error": f"Invalid arguments: {str(te)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/log_transaction_data', methods=['POST'])
def api_log_transaction_data():
    data = request.json
    # Pass data as kwargs or however the original function expects it
    # Simplified mapping:
    try:
        if isinstance(data, dict):
             result = service.log_transaction_data(**data)
        else:
             result = service.log_transaction_data(data)
        return jsonify({"result": result})
    except TypeError as te:
        return jsonify({"error": f"Invalid arguments: {str(te)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/retrieve_user_transaction_history', methods=['POST'])
def api_retrieve_user_transaction_history():
    data = request.json
    # Pass data as kwargs or however the original function expects it
    # Simplified mapping:
    try:
        if isinstance(data, dict):
             result = service.retrieve_user_transaction_history(**data)
        else:
             result = service.retrieve_user_transaction_history(data)
        return jsonify({"result": result})
    except TypeError as te:
        return jsonify({"error": f"Invalid arguments: {str(te)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/identify_potential_fraudulent_activity', methods=['POST'])
def api_identify_potential_fraudulent_activity():
    data = request.json
    # Pass data as kwargs or however the original function expects it
    # Simplified mapping:
    try:
        if isinstance(data, dict):
             result = service.identify_potential_fraudulent_activity(**data)
        else:
             result = service.identify_potential_fraudulent_activity(data)
        return jsonify({"result": result})
    except TypeError as te:
        return jsonify({"error": f"Invalid arguments: {str(te)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/calculate_transaction_risk_score', methods=['POST'])
def api_calculate_transaction_risk_score():
    data = request.json
    # Pass data as kwargs or however the original function expects it
    # Simplified mapping:
    try:
        if isinstance(data, dict):
             result = service.calculate_transaction_risk_score(**data)
        else:
             result = service.calculate_transaction_risk_score(data)
        return jsonify({"result": result})
    except TypeError as te:
        return jsonify({"error": f"Invalid arguments: {str(te)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/mark_transaction_as_suspicious', methods=['POST'])
def api_mark_transaction_as_suspicious():
    data = request.json
    # Pass data as kwargs or however the original function expects it
    # Simplified mapping:
    try:
        if isinstance(data, dict):
             result = service.mark_transaction_as_suspicious(**data)
        else:
             result = service.mark_transaction_as_suspicious(data)
        return jsonify({"result": result})
    except TypeError as te:
        return jsonify({"error": f"Invalid arguments: {str(te)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/send_general_notification_email', methods=['POST'])
def api_send_general_notification_email():
    data = request.json
    # Pass data as kwargs or however the original function expects it
    # Simplified mapping:
    try:
        if isinstance(data, dict):
             result = service.send_general_notification_email(**data)
        else:
             result = service.send_general_notification_email(data)
        return jsonify({"result": result})
    except TypeError as te:
        return jsonify({"error": f"Invalid arguments: {str(te)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/record_user_activity', methods=['POST'])
def api_record_user_activity():
    data = request.json
    # Pass data as kwargs or however the original function expects it
    # Simplified mapping:
    try:
        if isinstance(data, dict):
             result = service.record_user_activity(**data)
        else:
             result = service.record_user_activity(data)
        return jsonify({"result": result})
    except TypeError as te:
        return jsonify({"error": f"Invalid arguments: {str(te)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/retrieve_system_audit_log', methods=['POST'])
def api_retrieve_system_audit_log():
    data = request.json
    # Pass data as kwargs or however the original function expects it
    # Simplified mapping:
    try:
        if isinstance(data, dict):
             result = service.retrieve_system_audit_log(**data)
        else:
             result = service.retrieve_system_audit_log(data)
        return jsonify({"result": result})
    except TypeError as te:
        return jsonify({"error": f"Invalid arguments: {str(te)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/fetch_system_log_data', methods=['POST'])
def api_fetch_system_log_data():
    data = request.json
    # Pass data as kwargs or however the original function expects it
    # Simplified mapping:
    try:
        if isinstance(data, dict):
             result = service.fetch_system_log_data(**data)
        else:
             result = service.fetch_system_log_data(data)
        return jsonify({"result": result})
    except TypeError as te:
        return jsonify({"error": f"Invalid arguments: {str(te)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
