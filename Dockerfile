# Use an official lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy everything into the container
COPY . .
# Optional: If above line doesn't include tests/, use these explicitly
 COPY app/ app/
 COPY tests/ tests/
 COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the app (optional)
CMD ["python", "app.py"]

