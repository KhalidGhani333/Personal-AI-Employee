#!/bin/bash
# Docker Stop Script for Personal AI Employee

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "=================================================="
echo "  Personal AI Employee - Docker Stop"
echo "=================================================="
echo ""

# Check if services are running
if ! docker-compose ps | grep -q "Up"; then
    echo -e "${YELLOW}⚠️  No services are currently running${NC}"
    exit 0
fi

echo "Current running services:"
docker-compose ps
echo ""

# Ask for confirmation
read -p "Do you want to stop all services? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled"
    exit 0
fi

# Ask if user wants to remove volumes
echo ""
read -p "Do you want to remove volumes (database data will be deleted)? (y/n) " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo -e "${RED}⚠️  WARNING: This will delete all database data!${NC}"
    read -p "Are you sure? Type 'yes' to confirm: " confirm

    if [ "$confirm" = "yes" ]; then
        echo ""
        echo "Stopping services and removing volumes..."
        docker-compose down -v
        echo -e "${GREEN}✅ Services stopped and volumes removed${NC}"
    else
        echo "Cancelled"
        exit 0
    fi
else
    echo ""
    echo "Stopping services (keeping volumes)..."
    docker-compose down
    echo -e "${GREEN}✅ Services stopped (data preserved)${NC}"
fi

echo ""
echo "=================================================="
echo "  Services Stopped"
echo "=================================================="
echo ""
echo "To start again, run: ./docker-start.sh"
echo "Or: docker-compose up -d"
echo ""
