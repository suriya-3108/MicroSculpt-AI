from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class ProductService:
    def health_check(self):
        return {"status": "healthy", "service": "ProductService"}


    def save_product_stock(self, product_id, stock):
            """Save updated stock level"""
            return True



service = ProductService()

@app.route('/health', methods=['GET'])
def health():
    return jsonify(service.health_check())

@app.route('/save_product_stock', methods=['POST'])
def api_save_product_stock():
    data = request.json
    # Pass data as kwargs or however the original function expects it
    # Simplified mapping:
    try:
        if isinstance(data, dict):
             result = service.save_product_stock(**data)
        else:
             result = service.save_product_stock(data)
        return jsonify({"result": result})
    except TypeError:
        # Fallback if args don't match
        return jsonify({"result": service.save_product_stock()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
