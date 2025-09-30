# Robot Framework + Browser library Dockerfile
FROM python:3.10-slim

# Install dependencies for Playwright/Browser library and npm
RUN apt-get update && \
    apt-get install -y wget curl gnupg2 nodejs npm \
    libgtk-3-0 libx11-xcb1 libnss3 libasound2 libxcomposite1 \
    libxdamage1 libxrandr2 libgbm1 libxshmfence1 libxfixes3 \
    libxext6 libxrender1 libxtst6 libxi6 libgl1 libegl1 && \
    rm -rf /var/lib/apt/lists/*

# Install Robot Framework Browser library and browsers
RUN pip install robotframework-browser robotframework-requests && rfbrowser init

WORKDIR /opt/robotframework/tests
COPY . /opt/robotframework/tests

CMD ["robot", "."]
