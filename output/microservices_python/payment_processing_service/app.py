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

class PaymentProcessingService:
    def health_check(self):
        return {"status": "healthy", "service": "PaymentProcessingService"}


    def process_payment_transaction(self, sender_id, receiver_id, amount):
            """Process a payment between two users"""
            if amount <= 0:
                return {"error": "Invalid amount"}
            
            if not requests.post("http://account_management_service:5002/authenticate_user_credentials", json={"user_id": sender_id, "pin": None}).json().get("result"):
                return {"error": "Invalid sender"}
            
            sender = requests.post("http://account_management_service:5002/retrieve_user_data", json={"user_id": sender_id}).json().get("result")
            receiver = requests.post("http://account_management_service:5002/retrieve_user_data", json={"user_id": receiver_id}).json().get("result")
            
            if not sender or not receiver:
                return {"error": "User not found"}
            
            if sender["balance"] < amount:
                return {"error": "Insufficient funds"}
            
            txn_id = requests.post("http://account_management_service:5002/generate_unique_transaction_identifier", json={}).json().get("result")
            
            debit_result = requests.post("http://account_management_service:5002/modify_user_account_balance", json={"user_id": sender_id, "amount": amount, "operation": "debit"}).json().get("result")
            if not debit_result.get("success"):
                return debit_result
            
            credit_result = requests.post("http://account_management_service:5002/modify_user_account_balance", json={"user_id": receiver_id, "amount": amount, "operation": "credit"}).json().get("result")
            
            requests.post("http://account_management_service:5002/log_transaction_data", json={"txn_id": txn_id, "sender_id": sender_id, "receiver_id": receiver_id, "amount": amount, "status": "completed"}).json().get("result")
            requests.post("http://user_data_service:5005/send_user_notification", json={"user_id": sender_id, "message": f"Payment of ${amount} sent to {receiver['name']}"}).json().get("result")
            requests.post("http://user_data_service:5005/send_user_notification", json={"user_id": receiver_id, "message": f"Payment of ${amount} received from {sender['name']}"}).json().get("result")
            requests.post("http://account_management_service:5002/record_user_activity", json={"user_id": sender_id, "action": f"payment_sent:{txn_id}"}).json().get("result")
            
            return {"success": True, "transaction_id": txn_id, "amount": amount}



service = PaymentProcessingService()

@app.route('/health', methods=['GET'])
def health():
    return jsonify(service.health_check())

@app.route('/process_payment_transaction', methods=['POST'])
def api_process_payment_transaction():
    data = request.json
    # Pass data as kwargs or however the original function expects it
    # Simplified mapping:
    try:
        if isinstance(data, dict):
             result = service.process_payment_transaction(**data)
        else:
             result = service.process_payment_transaction(data)
        return jsonify({"result": result})
    except TypeError as te:
        return jsonify({"error": f"Invalid arguments: {str(te)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
