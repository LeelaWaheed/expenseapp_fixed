"""
This module handles the main application setup and routes, including functions like "create_app".
"""
from werkzeug.security import generate_password_hash
from app import create_app
from app.models import db, User


app = create_app()

with app.app_context():
    # Ensure the database tables exist
    db.create_all()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
