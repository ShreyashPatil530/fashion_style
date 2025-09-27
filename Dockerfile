# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app
COPY . .

# Expose port for Railway
ENV PORT 8000

# Run the app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main:app"]

# Install PyTorch CPU version
RUN pip install torch==2.8.0+cpu torchvision==0.23.0+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html
