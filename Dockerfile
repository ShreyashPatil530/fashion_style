# Copy the rest of your application
COPY . .

# Install PyTorch and TorchVision (CPU)
RUN pip install torch==2.8.0 torchvision==0.23.0

# Expose port
EXPOSE 8000

# Start app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main:app"]
