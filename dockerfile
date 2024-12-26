# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app
#my name pandurangasai 
# Copy the requirements.txt file to the container
COPY requirements.txt /app/

# Install dependencies using pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY src /app/src

# Expose the port the app runs on
EXPOSE 8000

# Define environment variable to disable buffering
ENV PYTHONUNBUFFERED=1

# Run the FastAPI app using Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

