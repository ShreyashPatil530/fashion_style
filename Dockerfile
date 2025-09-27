# Use a smaller Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy only requirements first (caching layer)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project
COPY . .

# Expose port for Railway
EXPOSE 8000

# Run the app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main:app"]
