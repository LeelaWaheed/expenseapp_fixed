import sys
import os

# Add the parent directory (project root) to the system path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from app import create_app, db
from app.models import User, Expense, Budget
from werkzeug.security import generate_password_hash
import pytest


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SECRET_KEY"] = "test"
    return app

@pytest.fixture
def client(app):
    with app.app_context():
        db.create_all()
        user = User(username="testuser", password=generate_password_hash("abc123"))
        db.session.add(user)
        db.session.commit()

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["user_id"] = 1
            yield client

# ✅ Wrap isolate_db inside app.app_context
@pytest.fixture(autouse=True)
def isolate_db(app):
    with app.app_context():
        db.drop_all()
        db.create_all()


def test_user_registration(client):
    # Use a fresh session for this test
    app = create_app()
    with app.test_client() as new_client:
        response = new_client.post("/api/register", json={
            "username": "newuser",
            "password": "pass123"
        })
        assert response.status_code == 201
        assert b"User registered successfully" in response.data

def test_set_budget(client):
    response = client.post("/api/set-budget", json={
        "amount": 300.0,
        "month": "2025-05"
    })
    assert response.status_code == 200
    assert b"Budget set successfully" in response.data

def test_get_budget(client):
    # Set a budget first
    client.post("/api/set-budget", json={
        "amount": 150.0,
        "month": "2025-06"
    })

    # Now fetch
    response = client.get("/api/budget?month=2025-06")
    assert response.status_code == 200
    data = response.get_json()
    assert data["budget"] == 150.0

def test_delete_expense(client):
    # Add an expense first
    post_resp = client.post("/api/expenses", json={
        "amount": 99.99,
        "category": "Utilities",
        "date": "2025-05-24"
    })
    assert post_resp.status_code == 201

    # Now get the expense ID
    get_resp = client.get("/api/expenses?month=2025-05")
    expense_id = get_resp.get_json()[0]["id"]

    # Delete it
    del_resp = client.delete(f"/api/expenses/{expense_id}")
    assert del_resp.status_code == 200
    assert b"Expense deleted" in del_resp.data
def test_set_budget(client):
    response = client.post("/api/set-budget", json={
        "amount": 250.0,
        "month": "2025-06"
    })
    assert response.status_code == 200
    assert b"Budget set successfully" in response.data

def test_get_budget(client):
    # First set a budget
    client.post("/api/set-budget", json={
        "amount": 400.0,
        "month": "2025-07"
    })

    # Now fetch it
    response = client.get("/api/budget?month=2025-07")
    assert response.status_code == 200
    data = response.get_json()
    assert data["budget"] == 400.0

def test_add_expense(client):
    response = client.post("/api/expenses", json={
        "amount": 45.75,
        "category": "Transport",
        "date": "2025-06-15"
    })
    assert response.status_code == 201
    assert b"Expense added" in response.data

def test_get_expenses(client):
    client.post("/api/expenses", json={
        "amount": 18.50,
        "category": "Food",
        "date": "2025-06-01"
    })

    response = client.get("/api/expenses?month=2025-06")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(e["category"] == "Food" for e in data)

def test_delete_expense(client):
    # Add an expense first
    post_resp = client.post("/api/expenses", json={
        "amount": 60.00,
        "category": "Utilities",
        "date": "2025-06-02"
    })
    assert post_resp.status_code == 201

    # Fetch the ID
    get_resp = client.get("/api/expenses?month=2025-06")
    expense_id = get_resp.get_json()[0]["id"]

    # Delete it
    del_resp = client.delete(f"/api/expenses/{expense_id}")
    assert del_resp.status_code == 200
    assert b"Expense deleted" in del_resp.data
def test_api_register(client):
    # Register a new user with a unique username
    response = client.post("/api/register", json={
        "username": "newuser1",
        "password": "newpass"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert "user_id" in data
    assert data["message"] == "User registered successfully"

def test_api_login_valid(client):
    response = client.post("/api/login", json={
        "username": "testuser",
        "password": "abc123"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Login successful"

def test_api_login_invalid(client):
    response = client.post("/api/login", json={
        "username": "testuser",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    data = response.get_json()
    assert data["error"] == "Invalid username or password"

def test_form_register_post(client):
    response = client.post("/register", data={
        "username": "formuser1",
        "password": "formpass"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Registration successful" in response.data

def test_form_register_post(client):
    response = client.post("/register", data={
        "username": "formuser1",
        "password": "formpass"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"<title>Login</title>" in response.data  # Confirms redirected to login page
    assert b"Username" in response.data              # Confirms login form is present


def test_api_login_missing_fields(client):
    # Missing username
    response = client.post("/api/login", json={
        "password": "abc123"
    })
    assert response.status_code == 401 or response.status_code == 400
    assert b"Invalid" in response.data or b"Missing" in response.data


