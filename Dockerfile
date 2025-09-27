# Use official Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application
COPY . .

# Expose the default port Railway uses
EXPOSE 8000

# Command to run the Flask app using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main:app"]
