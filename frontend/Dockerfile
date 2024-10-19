# Using a lightweight Python runtime as a parent image
FROM python:3.10-slim

# Install any dependencies needed to run your Python code
RUN pip install flask

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Run app.py when the container launches
CMD ["python", "app.py"]
