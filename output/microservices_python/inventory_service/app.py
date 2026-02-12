from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class InventoryService:
    def health_check(self):
        return {"status": "healthy", "service": "InventoryService"}


    def update_inventory(self, product_id, quantity_sold):
            """Update product inventory after sale"""
            current_stock = get_product_stock(product_id)
            new_stock = current_stock - quantity_sold
            save_product_stock(product_id, new_stock)
            return new_stock



service = InventoryService()

@app.route('/health', methods=['GET'])
def health():
    return jsonify(service.health_check())

@app.route('/update_inventory', methods=['POST'])
def api_update_inventory():
    data = request.json
    # Pass data as kwargs or however the original function expects it
    # Simplified mapping:
    try:
        if isinstance(data, dict):
             result = service.update_inventory(**data)
        else:
             result = service.update_inventory(data)
        return jsonify({"result": result})
    except TypeError:
        # Fallback if args don't match
        return jsonify({"result": service.update_inventory()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
