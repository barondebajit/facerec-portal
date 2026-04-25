FROM mcr.microsoft.com/devcontainers/python:3.11-bullseye

# 🔧 Remove broken Yarn repo
RUN rm -f /etc/apt/sources.list.d/yarn.list

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libgl1 \
    curl \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./

# Upgrade pip (optional but good practice)
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]