# Use official Python image
FROM python:3.12

# Set working directory inside container
WORKDIR /app

# Copy all project files except database.db
COPY . .

# Explicitly copy database.db from host into container
COPY database.db .

# Install required Python packages
RUN pip install --no-cache-dir flask bcrypt flask-limiter psutil

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
