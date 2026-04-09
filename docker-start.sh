#!/bin/bash
# Docker Quick Start Script for Personal AI Employee
# This script helps you get started with Docker deployment

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "=================================================="
echo "  Personal AI Employee - Docker Quick Start"
echo "=================================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed${NC}"
    echo "Please install Docker from: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed${NC}"
    echo "Please install Docker Compose from: https://docs.docker.com/compose/install/"
    exit 1
fi

echo -e "${GREEN}✅ Docker installed${NC}"
echo -e "${GREEN}✅ Docker Compose installed${NC}"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found${NC}"
    echo "Creating .env from template..."

    if [ -f .env.example ]; then
        cp .env.example .env
        echo -e "${GREEN}✅ .env file created${NC}"
        echo -e "${YELLOW}⚠️  Please edit .env file with your credentials before continuing${NC}"
        echo ""
        read -p "Press Enter after editing .env file..."
    else
        echo -e "${RED}❌ .env.example not found${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ .env file exists${NC}"
fi

# Create secrets directory
if [ ! -d secrets ]; then
    echo "Creating secrets directory..."
    mkdir -p secrets
    mkdir -p secrets/git_ssh
    echo -e "${GREEN}✅ Secrets directory created${NC}"
    echo -e "${YELLOW}⚠️  Please add your credentials to secrets/ directory${NC}"
else
    echo -e "${GREEN}✅ Secrets directory exists${NC}"
fi

# Create necessary vault directories
echo ""
echo "Creating vault directories..."
mkdir -p AI_Employee_Vault/{Needs_Action,Needs_Approval,Done,Approved,Plans,Accounting,Briefings,Logs,Archive}
echo -e "${GREEN}✅ Vault directories created${NC}"

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo -e "${RED}❌ Docker daemon is not running${NC}"
    echo "Please start Docker and try again"
    exit 1
fi

echo ""
echo "=================================================="
echo "  Starting Docker Services"
echo "=================================================="
echo ""

# Pull images
echo "Pulling Docker images..."
docker-compose pull

# Build custom images
echo ""
echo "Building custom images..."
docker-compose build

# Start services
echo ""
echo "Starting services..."
docker-compose up -d

# Wait for services to start
echo ""
echo "Waiting for services to initialize..."
sleep 10

# Check service status
echo ""
echo "=================================================="
echo "  Service Status"
echo "=================================================="
docker-compose ps

echo ""
echo "=================================================="
echo "  Setup Complete!"
echo "=================================================="
echo ""
echo -e "${GREEN}✅ All services started successfully${NC}"
echo ""
echo "Access points:"
echo "  - Odoo Accounting: http://localhost:8069"
echo "  - Vault Location: ./AI_Employee_Vault/"
echo ""
echo "Useful commands:"
echo "  - View logs: docker-compose logs -f"
echo "  - Stop services: docker-compose down"
echo "  - Restart: docker-compose restart"
echo "  - CEO Briefing: docker-compose exec ceo_briefing python /app/scripts/ceo_briefing.py weekly"
echo ""
echo "For detailed documentation, see: DOCKER_SETUP.md"
echo ""
