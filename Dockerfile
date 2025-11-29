FROM python:3.11-slim

# Avoid interactive prompts during package install
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies (poppler + tesseract)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       poppler-utils \
       tesseract-ocr \
       libtesseract-dev \
       ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /usr/src/app

# Copy requirements and install
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY app /usr/src/app/app

# Expose port
EXPOSE 8000

# Default environment variables (can be overridden in the host/platform)
ENV POPPLER_BIN=/usr/bin
ENV TESSERACT_CMD=/usr/bin/tesseract

# Run the FastAPI app with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
