from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, func
from datetime import datetime

# Initialize SQLAlchemy object - it's not connected to the app yet
db = SQLAlchemy()

# Function to initialize the app with the database object
def init_app(app):
    db.init_app(app)

# ----------------------------------------------------------------------
# ORM Models (This replaces your raw SQL CREATE TABLE statements)
# ----------------------------------------------------------------------

class User(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    posts = relationship("Post", back_populates="author")
    likes = relationship("Like", back_populates="user")
    comments = relationship("Comment", back_populates="user")

class Post(db.Model):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    image_path: Mapped[str] = mapped_column(String, nullable=True)
    likes_count: Mapped[int] = mapped_column(Integer, default=0) # We'll maintain this count manually or via query
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    author = relationship("User", back_populates="posts")
    likes = relationship("Like", back_populates="post", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")

    @property
    def like_count(self):
        # Calculate like count using a query
        return db.session.scalar(
            db.select(func.count(Like.id)).where(Like.post_id == self.id)
        )
        
    @property
    def comment_count(self):
        # Calculate comment count using a query
        return db.session.scalar(
            db.select(func.count(Comment.id)).where(Comment.post_id == self.id)
        )

class Like(db.Model):
    __tablename__ = 'likes'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('post.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'post_id', name='_user_post_uc'),
    )

    # Relationships
    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")

class Comment(db.Model):
    __tablename__ = 'comments'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('post.id'), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

# ----------------------------------------------------------------------
# ORM Helper Functions (Replacing your raw sqlite3 functions)
# ----------------------------------------------------------------------

# NOTE: The helper functions in your previous database.py are now simplified or
# replaced by direct SQLAlchemy calls, which are generally done in the route files (auth.py, posts.py).
# We'll provide the new ORM versions here for clarity.

# AUTH Helpers (for use in auth.py)
def create_user(username, email, password):
    # This is a basic example; you should add password hashing (e.g., with werkzeug.security)
    try:
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return new_user.id
    except:
        db.session.rollback()
        return None

def get_user_by_username(username):
    return db.session.execute(db.select(User).filter_by(username=username)).scalar_one_or_none()

def get_user_by_id(user_id):
    return db.session.get(User, user_id)

# POSTS Helpers (for use in posts.py)
def create_post(user_id, content, image_path=None):
    new_post = Post(user_id=user_id, content=content, image_path=image_path)
    db.session.add(new_post)
    db.session.commit()
    return new_post.id

def get_all_posts():
    # Includes joining with User to get the username
    return db.session.execute(
        db.select(Post)
        .order_by(Post.created_at.desc())
    ).scalars().all()

def get_posts_by_user(user_id):
    return db.session.execute(
        db.select(Post).filter_by(user_id=user_id)
        .order_by(Post.created_at.desc())
    ).scalars().all()

def toggle_like(user_id, post_id):
    like = db.session.execute(
        db.select(Like).filter_by(user_id=user_id, post_id=post_id)
    ).scalar_one_or_none()

    if like:
        db.session.delete(like)
        action = 'unliked'
    else:
        new_like = Like(user_id=user_id, post_id=post_id)
        db.session.add(new_like)
        action = 'liked'
    
    db.session.commit()
    return action

def add_comment(user_id, post_id, content):
    new_comment = Comment(user_id=user_id, post_id=post_id, content=content)
    db.session.add(new_comment)
    db.session.commit()
    # No return value needed based on your original function
    
def get_comments(post_id):
    return db.session.execute(
        db.select(Comment).filter_by(post_id=post_id)
        .order_by(Comment.created_at.asc())
    ).scalars().all()
