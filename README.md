# 📱 SocialConnect: A Simple Flask Social Media Application

## 🚀 Project Overview

SocialConnect is a minimalist social media platform built using **Flask** and **Flask-SQLAlchemy**. Users can register, log in, create text-based posts with optional image uploads, view a dashboard feed, like posts, and comment on them. The project was developed as a [**CDAC DBDA Project**] and demonstrates core web development concepts, including secure authentication, ORM database management, and modular application structure using Blueprints.

| Feature | Status | Details |
| :--- | :--- | :--- |
| **Authentication** | ✅ Implemented | Registration, Login, Logout (using `werkzeug.security` for hashing). |
| **Posting** | ✅ Implemented | Users can create posts with text content. |
| **Media** | ✅ Implemented | Optional image uploads handled by Flask's `request.files`. |
| **Database** | ✅ Implemented | Persistent data storage using **SQLite** and **Flask-SQLAlchemy** ORM. |
| **Interactions** | ✅ Implemented | Like and Comment functionality (counts are displayed dynamically). |

***

## ⚙️ Technical Stack

* **Backend Framework:** Python (3.12+) & Flask
* **Database:** SQLite (local development)
* **ORM:** Flask-SQLAlchemy
* **Authentication:** `werkzeug.security` (for password hashing)
* **Templating:** Jinja2
* **Frontend:** HTML5, CSS3, JavaScript (for simple interactions)

***

## 💻 Getting Started

### Prerequisites

You must have **Python 3.10 or higher** installed on your system.

### Installation Steps

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/rujalinagbhidkar/Social-Connect.git](https://github.com/rujalinagbhidkar/Social-Connect.git)
    cd Social-Connect
    ```

2.  **Create and Activate a Virtual Environment:**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Application:**
    The application will automatically initialize the database and create all necessary tables upon starting.

    ```bash
    python app.py
    ```

5.  **Access the App:**
    Open your web browser and navigate to:
    ```
    [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
    ```

***

## 🔑 Implementation Highlights

### 1. Flask-SQLAlchemy Models
The application uses **User, Post, Like, and Comment** models. A key detail is that the `Post` model's table name is explicitly set to **`post`** (singular) to ensure compatibility with generated queries and foreign key constraints in SQLite.

### 2. Secure Authentication
The `auth` blueprint handles user authentication using:
* **`generate_password_hash`**: To securely hash and store passwords in the database.
* **`check_password_hash`**: To verify the user's login attempt against the stored hash.

### 3. File Handling
The `posts.py` blueprint handles file uploads using the `enctype="multipart/form-data"` in the HTML form. Uploaded images are secured using `werkzeug.utils.secure_filename` before being saved to the `static/uploads` folder.

### 4. Relationships and ORM Access
Post data is efficiently retrieved in `dashboard.html` by leveraging SQLAlchemy relationships, such as accessing the author's username via **`{{ post.author.username }}`** instead of performing manual joins.

***

## 📋 Requirements File (`requirements.txt`)

The core dependencies required for the project are:

```txt
Flask
Flask-SQLAlchemy
werkzeug
(Note: A full pip freeze command would include specific version numbers for a production environment.)

🤝 Contribution
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
