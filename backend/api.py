
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import pandas as pd
import pickle
import re
import os
import json
import numpy as np
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "../frontend")

app = Flask(
    __name__,
    static_folder=FRONTEND_DIR,
    template_folder=FRONTEND_DIR
)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)
limiter.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    is_verified = db.Column(db.Boolean, default=False)

    otp = db.Column(db.String(6))
    otp_expiry = db.Column(db.DateTime)

    search_history = db.Column(db.Text, default="[]")


with app.app_context():
    db.create_all()
    print("✅ Database ready")

DATA_PATH = "C:/Users/hp/AIBookDiscoveryProject/data/books/preprocessed/clean_books.csv"
MODEL_PATH = "C:/Users/hp/AIBookDiscoveryProject/backend/model/similarity_matrix.pkl"

df = pd.read_csv(DATA_PATH)
with open(MODEL_PATH, "rb") as f:
    similarity_matrix = pickle.load(f)

df['title_norm'] = df['title_clean'].apply(lambda x: re.sub(r'[^a-z0-9 ]', '', str(x).lower()).strip())

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(user_email, otp):
    try:
        sender_email = "dewanshikarnawat05@gmail.com"      
        app_password = "ijdsqjurpvndhitd"        

        receiver_email = user_email  

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "AI Book Discovery - Verify Your Email"

        body = f"""
        Hello,

        Your OTP for AI Book Discovery is: {otp}

        This OTP will expire in 5 minutes.

        If you did not request this, please ignore this email.

        Thanks,
        AI Book Discovery Team
        """
        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.send_message(message)

        print(f"📧 OTP {otp} sent to {receiver_email}")
    except Exception as e:
        print("❌ Email sending failed:", e)


def universal_fuzzy_search(query):
    query_norm = re.sub(r'[^a-z0-9 ]', '', str(query).lower()).strip()
    shortcuts = {
        "hp": "harry potter",
        "davi": "da vinci", 
        "da": "da vinci",
        "1984": "1984",
        "lotr": "lord",
        "twilight": "twilight"
    }
    for short, target in shortcuts.items():
        if short in query_norm:
            matches = df[df['title_norm'].str.contains(target, na=False)]
            if not matches.empty:
                return matches.index[0]
    for word in query_norm.split():
        if len(word) >= 2:
            matches = df[df['title_norm'].str.contains(word, na=False)]
            if not matches.empty:
                return matches.index[0]
    return df['average_rating'].idxmax()

from email.mime.multipart import MIMEMultipart  # TOP pe add

@app.route("/register", methods=["POST"])
def register_user():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {"error": "Email and password required"}, 400

    if not is_valid_email(email):
        return {"error": "Invalid email"}, 400

    existing_user = User.query.filter_by(email=email).first()

    
    if existing_user and not existing_user.is_verified:
        otp = generate_otp()
        existing_user.otp = otp
        existing_user.otp_expiry = datetime.utcnow() + timedelta(minutes=5)
        db.session.commit()

        send_otp_email(email, otp)  
        print("🔁 OTP resent")
        return {"message": "OTP resent. Please verify."}, 200


    if existing_user and existing_user.is_verified:
        return {"error": "Email already registered. Please login."}, 400

    
    otp = generate_otp()
    user = User(
        email=email,
        password_hash=bcrypt.generate_password_hash(password).decode("utf-8"),
        otp=otp,
        otp_expiry=datetime.utcnow() + timedelta(minutes=5),
        is_verified=False
    )

    db.session.add(user)
    db.session.commit()

    send_otp_email(email, otp)  
    print("✅ New user registered")

    return {"message": "OTP sent to email"}, 201


@app.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.json
    email = data.get("email")
    otp = data.get("otp")

    if not email or not otp:
        return {"error": "Email and OTP required"}, 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return {"error": "User not found"}, 404


    if user.is_verified:
        return {"message": "Email already verified"}, 200


    if user.otp != otp:
        return {"error": "Invalid OTP"}, 400

    if not user.otp_expiry or datetime.utcnow() > user.otp_expiry:
        return {"error": "OTP expired. Please register again."}, 400


    user.is_verified = True
    user.otp = None
    user.otp_expiry = None
    db.session.commit()

    return {"message": "Email verified successfully"}, 200

@app.route("/login", methods=["POST"])
# @limiter.limit("10 per minute")
def login_user():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return {"error": "Invalid credentials"}, 401

    if not user.is_verified:
        return {"error": "Please verify your email first"}, 403


    return {"message": "Login successful", "user": {"email": user.email}}

@app.route("/search", methods=["POST"])
# @limiter.limit("30 per hour")
def search():
    data = request.json
    email = data.get("email")
    query = data.get("query")

    user = User.query.filter_by(email=email).first()
    if not user:
        return {"error": "User not found"}, 404

    history = json.loads(user.search_history)
    
    # spam prevention: same query repeated within last 5 searches
    if query.lower() in [h.lower() for h in history[-5:]]:
        return {"error": "You are submitting the same query too frequently"}, 429

    history.append(query)
    user.search_history = json.dumps(history[-20:])  # keep last 20
    db.session.commit()

    return {"message": "Search saved"}

@app.route("/recommend", methods=["GET"])
# @limiter.limit("50 per hour")
def recommend():
    book = request.args.get("book", "").strip()
    if not book:
        return {"error": "Please provide a book title"}, 400

    idx = universal_fuzzy_search(book)
    matched_title = df.iloc[idx]['title']

    scores = list(enumerate(similarity_matrix[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:6]

    result = []
    for i, score in scores:
        result.append({
            "title": df.iloc[i]['title'],
            "author": df.iloc[i]['authors'],
            "rating": float(df.iloc[i]['average_rating']),
            "similarity_score": float(score)
        })
    return jsonify(result)

@app.route("/autocomplete", methods=["GET"])
# @limiter.limit("50 per hour")
def autocomplete():
    query = request.args.get("q", "").strip().lower()
    if len(query) < 2:
        return jsonify([])

    shortcuts = {
        "hp": "Harry Potter and the Sorcerer's Stone",
        "davi": "The Da Vinci Code",
        "da": "The Da Vinci Code",
        "1984": "1984",
        "lotr": "The Lord of the Rings"
    }

    suggestions = []
    for short, title in shortcuts.items():
        if short.startswith(query):
            suggestions.append({"title": title, "authors": "Popular Book", "is_shortcut": True})

    matches = df[df['title_norm'].str.contains(query, na=False, case=False)].head(4)
    for _, row in matches.iterrows():
        suggestions.append({"title": row['title'], "authors": row['authors'], "is_shortcut": False})

    return jsonify(suggestions[:5])

@app.route("/popular", methods=["GET"])
# @limiter.limit("50 per hour")
def popular_books():
    if 'recommend_count' not in df.columns:
        df['recommend_count'] = np.random.randint(10, 200, size=len(df))

    most_recommended = df.sort_values(by=['ratings_count', 'average_rating'], ascending=False).head(5)
    top_rated = df[(df['average_rating'] >= 4.5) & (df['ratings_count'] >= 1000)].sort_values(by='average_rating', ascending=False).head(5)

    def format_books(subset):
        return [{"title": r['title'], "author": r['authors'], "rating": float(r['average_rating'])} for _, r in subset.iterrows()]

    return jsonify({"most_recommended": format_books(most_recommended), "top_rated": format_books(top_rated)})


@app.route("/")
@app.route("/index.html")
def serve_index(): return send_from_directory(FRONTEND_DIR, "index.html")
@app.route("/login.html")
def serve_login(): return send_from_directory(FRONTEND_DIR, "login.html")
@app.route("/register.html")
def serve_register(): return send_from_directory(FRONTEND_DIR, "register.html")
@app.route("/app.html")
def serve_app(): return send_from_directory(FRONTEND_DIR, "app.html")
@app.route("/verifyOTP.html")
def serve_verify_otp():
    return send_from_directory(FRONTEND_DIR, "verifyOTP.html")


if __name__ == "__main__":
    print("🚀 API ready with spam prevention & rate limiting")
    app.run(debug=True, host='0.0.0.0', port=5000)