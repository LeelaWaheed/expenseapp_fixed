# Use a lightweight Python image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy everything first
COPY . /app

# Explicitly copy app.py to ensure it's inside /app/
COPY app.py /app/app.py

# Ensure instance directory exists
RUN mkdir -p /app/instance
COPY instance/expenses.db /app/instance/expenses.db

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir bandit

# Run Flask application
CMD ["python", "app/app.py"]