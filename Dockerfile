FROM python:3.11-slim

# Install system dependencies
# ffmpeg is required for yt-dlp audio post-processing
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install pipenv
RUN pip install pipenv

# Copy Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock ./

# Install python dependencies system-wide
RUN pipenv install --system --deploy

# Copy source code
COPY . .

# Expose port
EXPOSE 8000

# Run commands
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
