FROM python:3.11-slim

# Install dependencies needed by Playwright
RUN apt-get update && apt-get install -y \
    wget gnupg curl fonts-liberation \
    libnss3 libatk-bridge2.0-0 libgtk-3-0 libxss1 libasound2 \
    libxcomposite1 libxdamage1 libxrandr2 libxkbcommon0 libgbm1 \
    libpango-1.0-0 libx11-xcb1 libxfixes3 libxext6 libxrender1 libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Install Python packages and Playwright
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install --with-deps

EXPOSE 8080

# ✅ START with Uvicorn directly, NOT `fastapi run`
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]