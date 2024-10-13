# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# Install required C++11 libraries and ca-certificates
RUN apt-get update -qq \
      && apt-get install -y \
      build-essential \
      python3-dev \
      ca-certificates \
      curl \
      && apt-get clean \
      && rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Install additional packages like Streamlit, Pytesseract, and Pymongo
RUN pip install streamlit pytesseract pymongo

# Copy the current directory contents into the container at /app
COPY . /app

# Expose the port that Streamlit uses (default is 8501)
EXPOSE 8501

# Run Streamlit when the container launches
ENTRYPOINT ["streamlit", "run", "login.py", "--server.port=8501", "--server.address=0.0.0.0"]
