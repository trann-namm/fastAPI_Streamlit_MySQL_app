# Base Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /src

COPY . .
# Install dependencies

RUN pip install --no-cache-dir -r requirements.txt
# Copy the script
COPY . /src

# Default command 
CMD ["python", "crawling.py"]
