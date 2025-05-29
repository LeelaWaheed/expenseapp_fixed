FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN mkdir -p /app/instance

RUN apt-get update && apt-get install -y \
    bash \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt \
    && pip install pylint bandit

EXPOSE 5000

CMD ["python", "app.py"]
