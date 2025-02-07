# Use the official Python image as the base image.
FROM python:3.9-slim

# Set the working directory in the container.
WORKDIR /app

# Copy the dependencies file to the working directory.
COPY requirements.txt .

# Upgrade pip and install dependencies.
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code.
COPY . .

# Expose port 5000 to allow external access.
EXPOSE 5000

# Define the default command to run the Flask app.
CMD ["python", "app.py"]
