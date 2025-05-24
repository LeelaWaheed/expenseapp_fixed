from flask import Blueprint, render_template, request, redirect, jsonify, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User, Expense, Budget
from datetime import datetime
from sqlalchemy import extract

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return redirect("/login")

@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            flash("Please enter both username and password.", "warning")
            return redirect("/register")
        if User.query.filter_by(username=username).first():
            flash("User already exists. Please log in instead.", "info")
            return redirect("/login")
        user = User(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please log in.", "success")
        return redirect("/login")
    return render_template("register.html")

@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            flash("Please enter both username and password.", "warning")
            return redirect("/login")
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            return redirect("/dashboard")
        flash("Invalid username or password. Please try again.", "danger")
        return redirect("/login")
    return render_template("login.html")

@main.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("dashboard.html")

@main.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@main.route("/api/register", methods=["POST"])
def api_register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "Missing credentials"}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "User already exists. Please log in."}), 409
    user = User(username=username, password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully", "user_id": user.id}), 201

@main.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        session["user_id"] = user.id
        return jsonify({"message": "Login successful", "user_id": user.id}), 200
    return jsonify({"error": "Invalid username or password"}), 401

@main.route("/api/expenses", methods=["POST"])
def add_expense():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    amount = data.get("amount")
    category = data.get("category")
    date = data.get("date")
    if not all([amount, category, date]):
        return jsonify({"error": "Missing fields"}), 400
    expense = Expense(amount=amount, category=category, date=date, user_id=session["user_id"])
    db.session.add(expense)
    db.session.commit()
    return jsonify({"message": "Expense added"}), 201


@main.route("/api/budget", methods=["GET"])
def get_budget():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    month = request.args.get("month")
    if not month:
        return jsonify({"error": "Month required"}), 400

    total_budget = db.session.query(db.func.sum(Budget.amount)).filter_by(
        user_id=session["user_id"], month=month
    ).scalar() or 0

    return jsonify({"budget": total_budget})
@main.route("/api/set-budget", methods=["POST"])
def set_budget():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    amount = data.get("amount")
    month = data.get("month")

    if not amount or not month:
        return jsonify({"error": "Missing data"}), 400

    budget = Budget.query.filter_by(user_id=session["user_id"], month=month, category="General").first()
    if budget:
        budget.amount = amount
    else:
        budget = Budget(user_id=session["user_id"], month=month, category="General", amount=amount)
        db.session.add(budget)

    db.session.commit()
    return jsonify({"message": "Budget set successfully"})
@main.route("/api/budgets", methods=["GET"])
def get_all_budgets():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    budgets = Budget.query.filter_by(user_id=session["user_id"]).order_by(Budget.month.desc()).all()

    return jsonify([
        {"month": b.month, "amount": b.amount}
        for b in budgets
    ])
   
@main.route("/api/expenses/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    expense = Expense.query.filter_by(id=expense_id, user_id=session["user_id"]).first()
    if not expense:
        return jsonify({"error": "Expense not found"}), 404

    db.session.delete(expense)
    db.session.commit()
    return jsonify({"message": "Expense deleted"})

from sqlalchemy import extract

@main.route("/api/expenses", methods=["GET"])
def get_expenses():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    query = Expense.query.filter_by(user_id=session["user_id"])

    month = request.args.get("month")
    if month:
        from sqlalchemy import extract
        year, month_num = map(int, month.split("-"))
        query = query.filter(
            extract("year", Expense.date) == year,
            extract("month", Expense.date) == month_num
        )

    expenses = query.all()
    return jsonify([
    {"amount": e.amount, "category": e.category, "date": str(e.date), "id": e.id}
    for e in expenses
])






