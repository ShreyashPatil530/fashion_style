# 1. Use official Python 3.11 slim image as base
FROM python:3.11-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy requirements file
COPY requirements.txt .

# 4. Upgrade pip and install dependencies from requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 5. Install PyTorch CPU and TorchVision CPU
RUN pip install torch==2.8.0 torchvision==0.23.0 -f https://download.pytorch.org/whl/cpu/torch_stable.html

# 6. Copy the rest of the application
COPY . .

# 7. Expose port (Railway uses environment variable PORT)
EXPOSE ${PORT:-8000}

# 8. Command to run the app using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main:app"]
