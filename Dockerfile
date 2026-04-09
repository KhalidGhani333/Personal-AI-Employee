# Personal AI Employee - Dockerfile
# Multi-stage build for optimized image size

FROM python:3.13-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    wget \
    gnupg \
    ca-certificates \
    build-essential \
    gcc \
    python3-dev \
    libxml2-dev \
    libxslt1-dev \
    xvfb \
    xauth \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    libatspi2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js (for MCP servers)
RUN curl -fsSL https://deb.nodesource.com/setup_24.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install chromium
RUN playwright install-deps chromium

# Copy application code
COPY scripts/ ./scripts/
COPY mcp-servers/ ./mcp-servers/
COPY AI_Employee_Vault/ ./AI_Employee_Vault/
COPY .claude/ ./.claude/
COPY *.py ./
COPY *.sh ./

# Install MCP server dependencies
WORKDIR /app/mcp-servers/business_mcp
RUN if [ -f package.json ]; then npm install --production; fi

WORKDIR /app/mcp-servers/accounting_mcp
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

WORKDIR /app/mcp-servers/social_mcp
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Back to app directory
WORKDIR /app

# Create necessary directories
RUN mkdir -p \
    /app/AI_Employee_Vault/Needs_Action \
    /app/AI_Employee_Vault/Needs_Approval \
    /app/AI_Employee_Vault/Done \
    /app/AI_Employee_Vault/Approved \
    /app/AI_Employee_Vault/Plans \
    /app/AI_Employee_Vault/Accounting \
    /app/AI_Employee_Vault/Briefings \
    /app/AI_Employee_Vault/Logs \
    /app/AI_Employee_Vault/Archive \
    /app/Logs \
    /app/secrets

# Set permissions
RUN chmod +x /app/scripts/*.py || true
RUN chmod +x /app/*.sh || true

# Health check script
COPY health-check.sh /app/health-check.sh
RUN chmod +x /app/health-check.sh

# Create non-root user for security
RUN useradd -m -u 1000 aiemployee && \
    chown -R aiemployee:aiemployee /app

# Switch to non-root user
USER aiemployee

# Default command (can be overridden in docker-compose)
CMD ["python", "/app/scripts/orchestrator.py"]
