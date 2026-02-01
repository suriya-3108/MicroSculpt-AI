# Example E-commerce Code for Testing MicroSculpt AI

def validate_user_credentials(username, password):
    """Check if user credentials are valid"""
    if not username or not password:
        return False
    # Simulated validation
    return len(password) >= 8

def create_user_session(user_id):
    """Create a new session for authenticated user"""
    import random
    session_token = f"session_{user_id}_{random.randint(1000, 9999)}"
    return session_token

def user_login(username, password):
    """Handle user login process"""
    if validate_user_credentials(username, password):
        user_id = get_user_id(username)
        session = create_user_session(user_id)
        return {"success": True, "session": session}
    return {"success": False, "error": "Invalid credentials"}

def get_user_id(username):
    """Retrieve user ID from username"""
    # Simulated database lookup
    return hash(username) % 10000

def add_product_to_cart(user_id, product_id, quantity):
    """Add a product to user's shopping cart"""
    if quantity <= 0:
        return {"error": "Invalid quantity"}
    
    cart = get_user_cart(user_id)
    cart[product_id] = quantity
    save_cart(user_id, cart)
    return {"success": True, "cart": cart}

def get_user_cart(user_id):
    """Retrieve user's current cart"""
    # Simulated cart retrieval
    return {}

def save_cart(user_id, cart):
    """Save cart to database"""
    # Simulated save operation
    return True

def calculate_cart_total(user_id):
    """Calculate total price of items in cart"""
    cart = get_user_cart(user_id)
    total = 0
    for product_id, quantity in cart.items():
        price = get_product_price(product_id)
        total += price * quantity
    return total

def get_product_price(product_id):
    """Get price for a product"""
    # Simulated price lookup
    return 29.99

def process_payment(user_id, payment_method):
    """Process payment for user's cart"""
    total = calculate_cart_total(user_id)
    if total <= 0:
        return {"error": "Cart is empty"}
    
    payment_result = charge_payment(payment_method, total)
    if payment_result["success"]:
        order_id = create_order(user_id, total)
        send_confirmation_email(user_id, order_id)
        return {"success": True, "order_id": order_id}
    return {"success": False, "error": "Payment failed"}

def charge_payment(payment_method, amount):
    """Charge the payment method"""
    # Simulated payment processing
    return {"success": True, "transaction_id": "TXN123"}

def create_order(user_id, total):
    """Create a new order record"""
    import random
    order_id = f"ORD{random.randint(10000, 99999)}"
    return order_id

def send_confirmation_email(user_id, order_id):
    """Send order confirmation email to user"""
    email = get_user_email(user_id)
    # Simulated email sending
    return True

def get_user_email(user_id):
    """Get user's email address"""
    return f"user{user_id}@example.com"

def update_inventory(product_id, quantity_sold):
    """Update product inventory after sale"""
    current_stock = get_product_stock(product_id)
    new_stock = current_stock - quantity_sold
    save_product_stock(product_id, new_stock)
    return new_stock

def get_product_stock(product_id):
    """Get current stock level for product"""
    return 100

def save_product_stock(product_id, stock):
    """Save updated stock level"""
    return True
