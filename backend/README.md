# B-Social V2 Backend API

A robust REST API built to power the B-Social, social media platform. This service handles user authentication, profile management, and creating post, commenting, and also handle reactions to post and comments. B-Social is created to help me understand how the web works and ahow to apply different solutions in solving different types of problems involving the web.

## 🚀 Features
*   **Secure Authentication:** JWT-based user login and registration.
*   **Profile Management:** Custom user profiles with secure image uploads and unique user name.
*   **Creating Post:** Endpoints to manage creating and editing of posts.
* **Commenting:** User can comment to any post and edit them if any mistake was made.
* **Reacting to Posts and Comments:** User can react to different posts and comments.
*   **Concurrency:** Multithreaded execution for background tasks and some file processing.

## 🛠 Tech Stack
*   **Language:** Python 3.11
*   **Framework:** Flask
*   **Database:** SQLAlchemy (ORM)
*   **Authentication:** Flask-JWT-Extended
*   **API Documentation:** Swagger / OpenAPI

## 📋 Prerequisites
Ensure you have the following installed on your local machine:
*   [Python 3.10+](https://www.python.org/downloads/)
*   [Git](https://git-scm.com/)
*   A relational database (SQLite for dev, PostgreSQL recommended for prod)

## ⚙️ Installation and Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/meribehenry/b-social-v2-api.git](https://github.com/meribehenry/b-social-v2-api.git)
   cd b-social-v2-api
2. **Create and activate a virtual environment:**
    python venv -m venv
    venv/scripts/activate # On Windows
    venv/bin/activate # On Mac
3. **Install dependencies:**
    pip install -r requirements.txt
4. **Environment variables:**
Create a .env file in the root directory and add your configuration (like the the one in the .env.examples)
5. **Initialize the database:**
    flask db init #First step
    flask db migrate #Second step, read the migration file before going to the last step
     flask db upgrade #Last step and it should create a instances/your_db_name.db
6. **Run the application:**
    python run.py

## 📖 API Documentation
The API is fully documented using Swagger OpenAPI.
Once the server is running locally, you can view the interactive documentation and test endpoints by navigating to:
http://localhost:5000/api/docs or http://127.0.0.1:5000/api/docs

### Sample Endpoints:
• POST /api/v1/auth/login - Authenticate a user and return a JWT.
• GET /api/v1/users/<id>/profile - Retrieve a user's profile.
• POST /api/v1/posts – This creates a posts
• PATCH /api/v1/posts/<id> – Edits a post
• DELETE /api/v1/posts/<id> – Deletes a post

## 🤝 Contributing
Pull requests are not welcome for now, this project have not been completed and it won't work for others to contribute to it. But if you really have a good vision on it you can reach out to me.