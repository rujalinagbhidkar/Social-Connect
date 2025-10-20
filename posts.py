from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.utils import secure_filename
import os
# Import ORM-based helper functions
from database import (
    create_post, 
    get_all_posts, 
    get_posts_by_user, 
    get_user_by_id, 
    toggle_like, 
    add_comment, 
    get_comments,
    User, # Import Models if you need to access properties like User.username later
    Post
)

posts = Blueprint('posts', __name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@posts.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login first!', 'error')
        return redirect(url_for('auth.login'))
    
    # ORM Usage: get_all_posts returns a list of Post objects
    all_posts = get_all_posts()
    return render_template('dashboard.html', posts=all_posts)

@posts.route('/create_post', methods=['GET', 'POST'])
def create_post_route():
    # ... (No changes here, it uses the create_post helper function) ...
    if 'user_id' not in session:
        flash('Please login first!', 'error')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        content = request.form['content']
        image_path = None
        
        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Create unique filename
                filename = f"{session['user_id']}_{filename}"
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                image_path = f"uploads/{filename}"
        
        create_post(session['user_id'], content, image_path)
        flash('Post created successfully!', 'success')
        return redirect(url_for('posts.dashboard'))
    
    return render_template('create_post.html')

@posts.route('/profile/<int:user_id>')
def profile(user_id):
    if 'user_id' not in session:
        flash('Please login first!', 'error')
        return redirect(url_for('auth.login'))
    
    # ORM Usage: get_user_by_id returns a User object
    user = get_user_by_id(user_id)
    # ORM Usage: get_posts_by_user returns a list of Post objects
    user_posts = get_posts_by_user(user_id)
    
    return render_template('profile.html', user=user, posts=user_posts)

@posts.route('/like/<int:post_id>', methods=['POST'])
def like_post(post_id):
    # ... (No changes here, it uses the toggle_like helper function) ...
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    action = toggle_like(session['user_id'], post_id)
    return jsonify({'action': action})

@posts.route('/comment/<int:post_id>', methods=['POST'])
def comment_post(post_id):
    # ... (No changes here, it uses the add_comment helper function) ...
    if 'user_id' not in session:
        flash('Please login first!', 'error')
        return redirect(url_for('auth.login'))
    
    content = request.form['content']
    add_comment(session['user_id'], post_id, content)
    flash('Comment added!', 'success')
    return redirect(url_for('posts.dashboard'))