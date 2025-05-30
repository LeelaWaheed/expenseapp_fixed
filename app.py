"""
This module handles the main application setup and routes, including functions like "create_app".
"""

from app import create_app
from app.models import db, User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Ensure the database tables exist
    db.create_all()

    # Ensure permanent user exists
    if not User.query.filter_by(username="testuser").first():
        default_user = User(username="testuser", password=generate_password_hash("testpass"))
        db.session.add(default_user)
        db.session.commit()
        print("✅ Permanent user 'testuser' created!")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
