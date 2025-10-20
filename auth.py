from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import create_user, get_user_by_username

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validation
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('auth.register'))
        
        # Hash password
        hashed_password = generate_password_hash(password)
        
        # Create user
        user_id = create_user(username, email, hashed_password)
        
        if user_id:
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Username or email already exists!', 'error')
            return redirect(url_for('auth.register'))
    
    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # get_user_by_username returns a SQLAlchemy User object
        user = get_user_by_username(username)
        
        # FIXES HERE: Change user['key'] to user.key
        if user and check_password_hash(user.password, password):
            # FIX 1: Access password using dot notation
            # FIX 2: Access id using dot notation
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('posts.dashboard'))
        else:
            flash('Invalid username or password!', 'error')
            return redirect(url_for('auth.login'))
    
    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))