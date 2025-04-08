FROM python:3.12-slim

# Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
  && apt-get install -y netcat-openbsd gcc libpq-dev \
  && apt-get clean


# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Copy and give execution permission to start script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Expose the Daphne port
EXPOSE 8000

# Run app
CMD ["/start.sh"]
