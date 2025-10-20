from flask import Flask, render_template
# Import the SQLAlchemy db object from the new database.py
from database import db, init_app
from auth import auth
from posts import posts
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# --- NEW: Flask-SQLAlchemy Configuration ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///social_media.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# -------------------------------------------

# Initialize the db object with the app
init_app(app)

# Create upload folder
os.makedirs('static/uploads', exist_ok=True)

# Register blueprints
app.register_blueprint(auth)
app.register_blueprint(posts)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Initialize the database and create tables within the app context
    with app.app_context():
        # This replaces your old raw init_db() call
        db.create_all() 
        print("✅ Database tables created via Flask-SQLAlchemy!")
        
    app.run(debug=True, port=5000)