# Use official Python image
FROM python:3.12

# Set working directory inside container
WORKDIR /app

# Copy all project files to container
COPY . .

# Install required Python packages
RUN pip install --no-cache-dir flask bcrypt flask-limiter

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
