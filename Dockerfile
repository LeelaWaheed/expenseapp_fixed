# Use a lightweight Python image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Define environment variables early for cleaner execution
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Optimize dependency installation caching
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the full application after dependencies are installed
COPY . /app

# Explicitly copy app.py to ensure it's inside /app/
COPY app.py /app/app.py

# Ensure instance directory exists for SQLite setup
RUN mkdir -p /app/instance
COPY instance/expenses.db /app/instance/expenses.db

# Install security tools (e.g., Bandit for security scans)
RUN pip install --no-cache-dir bandit

# Expose Flask port
EXPOSE 5000

# Run Flask application
CMD ["flask", "run", "--host=0.0.0.0"]