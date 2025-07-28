# Use official Python slim image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy your Flask app code
COPY . /app

# Install Flask
RUN pip install --no-cache-dir flask

# Expose port 5000 (default Flask port)
EXPOSE 5000

# Command to run the app
CMD ["python", "app.py"]
