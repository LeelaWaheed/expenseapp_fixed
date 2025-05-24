# Use a minimal Python base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy everything from your project into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask app's default port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
