# Example Social Media Platform Code for Testing MicroSculpt AI

def register_new_user(username, email, password):
    """Register a new user account"""
    if not username or not email or not password:
        return {"error": "Missing required fields"}
    
    # Hash password
    import hashlib
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    
    user_id = create_user_record(username, email, hashed_pw)
    send_welcome_email(email, username)
    
    return {"success": True, "user_id": user_id}

def create_user_record(username, email, password_hash):
    """Create user record in database"""
    import random
    user_id = f"USR{random.randint(100000, 999999)}"
    # Simulated database insert
    return user_id

def authenticate_user(username, password):
    """Verify user credentials"""
    import hashlib
    stored_hash = get_password_hash(username)
    input_hash = hashlib.sha256(password.encode()).hexdigest()
    
    if stored_hash == input_hash:
        return {"authenticated": True, "user_id": get_user_id(username)}
    return {"authenticated": False}

def get_password_hash(username):
    """Retrieve stored password hash"""
    # Simulated database lookup
    return "abc123hash"

def get_user_id(username):
    """Get user ID from username"""
    import hashlib
    return int(hashlib.sha256(username.encode()).hexdigest(), 16) % 1000000

def create_post(user_id, content, media_urls=None):
    """Create a new social media post"""
    if not content or len(content) > 5000:
        return {"error": "Invalid content length"}
    
    import random
    post_id = f"POST{random.randint(1000000, 9999999)}"
    
    # Store post
    save_post_to_db(post_id, user_id, content, media_urls)
    
    # Update user's feed
    update_user_timeline(user_id, post_id)
    
    # Notify followers
    notify_followers(user_id, post_id)
    
    return {"success": True, "post_id": post_id}

def save_post_to_db(post_id, user_id, content, media_urls):
    """Save post to database"""
    from datetime import datetime
    timestamp = datetime.now().isoformat()
    # Simulated save
    return True

def update_user_timeline(user_id, post_id):
    """Add post to user's timeline"""
    timeline = get_user_timeline(user_id)
    timeline.insert(0, post_id)
    return True

def get_user_timeline(user_id):
    """Retrieve user's timeline"""
    # Simulated retrieval
    return []

def notify_followers(user_id, post_id):
    """Send notifications to all followers"""
    followers = get_followers(user_id)
    for follower_id in followers:
        send_notification(follower_id, f"New post from {user_id}", post_id)
    return len(followers)

def get_followers(user_id):
    """Get list of user's followers"""
    # Simulated follower list
    return ["USR123", "USR456", "USR789"]

def send_notification(user_id, message, reference_id):
    """Send push notification to user"""
    # Simulated notification service
    return True

def send_welcome_email(email, username):
    """Send welcome email to new user"""
    subject = f"Welcome to SocialApp, {username}!"
    body = f"Thanks for joining! Your account is ready."
    return send_email(email, subject, body)

def send_email(to_address, subject, body):
    """Generic email sending function"""
    # Simulated email service
    return {"sent": True, "message_id": "MSG123"}

def like_post(user_id, post_id):
    """Add a like to a post"""
    # Check if already liked
    if has_user_liked(user_id, post_id):
        return {"error": "Already liked"}
    
    add_like_record(user_id, post_id)
    increment_like_count(post_id)
    
    # Notify post author
    post_author = get_post_author(post_id)
    send_notification(post_author, f"{user_id} liked your post", post_id)
    
    return {"success": True}

def has_user_liked(user_id, post_id):
    """Check if user already liked a post"""
    # Simulated check
    return False

def add_like_record(user_id, post_id):
    """Record the like in database"""
    from datetime import datetime
    timestamp = datetime.now().isoformat()
    return True

def increment_like_count(post_id):
    """Increment the like counter for a post"""
    current_count = get_like_count(post_id)
    new_count = current_count + 1
    update_like_count(post_id, new_count)
    return new_count

def get_like_count(post_id):
    """Get current like count"""
    # Simulated retrieval
    return 42

def update_like_count(post_id, count):
    """Update like count in database"""
    return True

def get_post_author(post_id):
    """Get the user ID of post author"""
    # Simulated lookup
    return "USR999"

def generate_feed(user_id, page=1, limit=20):
    """Generate personalized feed for user"""
    # Get posts from followed users
    following = get_following(user_id)
    
    all_posts = []
    for followed_id in following:
        user_posts = get_user_posts(followed_id)
        all_posts.extend(user_posts)
    
    # Sort by engagement score
    ranked_posts = rank_posts_by_engagement(all_posts)
    
    # Paginate
    start = (page - 1) * limit
    end = start + limit
    
    return ranked_posts[start:end]

def get_following(user_id):
    """Get list of users that this user follows"""
    # Simulated following list
    return ["USR111", "USR222", "USR333"]

def get_user_posts(user_id):
    """Get all posts by a user"""
    # Simulated post retrieval
    return ["POST1", "POST2", "POST3"]

def rank_posts_by_engagement(posts):
    """Rank posts by engagement metrics"""
    # Simulated ML ranking
    import random
    shuffled = posts.copy()
    random.shuffle(shuffled)
    return shuffled

def calculate_engagement_score(post_id):
    """Calculate engagement score for a post"""
    likes = get_like_count(post_id)
    comments = get_comment_count(post_id)
    shares = get_share_count(post_id)
    
    # Weighted scoring
    score = (likes * 1) + (comments * 3) + (shares * 5)
    return score

def get_comment_count(post_id):
    """Get number of comments on a post"""
    return 10

def get_share_count(post_id):
    """Get number of shares for a post"""
    return 5
