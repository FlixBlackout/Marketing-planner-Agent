#!/bin/bash
# =============================================================================
# Quick Start Script for Marketing Planning Assistant
# Team Setup and Deployment
# =============================================================================

set -e

echo "=============================================="
echo "Marketing Planning Assistant - Quick Start"
echo "=============================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo "Checking prerequisites..."

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ Docker is not installed${NC}"
    echo "Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi
echo -e "${GREEN}✓ Docker installed: $(docker --version)${NC}"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}✗ Docker Compose is not installed${NC}"
    echo "Please install Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi
echo -e "${GREEN}✓ Docker Compose installed${NC}"

# Check Git
if ! command -v git &> /dev/null; then
    echo -e "${YELLOW}⚠ Git is not installed (optional but recommended)${NC}"
else
    echo -e "${GREEN}✓ Git installed${NC}"
fi

echo ""

# Check .env file
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠ .env file not found${NC}"
    echo "Creating .env from template..."
    cp .env.example .env
    echo -e "${RED}Please edit .env file with your API keys before continuing!${NC}"
    echo "Press Enter to continue after editing..."
    read
fi

echo ""
echo "=============================================="
echo "Choose deployment mode:"
echo "=============================================="
echo "1. Local Development (Docker Compose)"
echo "2. Production (Kubernetes)"
echo "3. Development with Hot Reload"
echo "4. Build Docker Image Only"
echo "5. Run Tests"
echo ""
read -p "Enter choice (1-5): " choice

case $choice in
    1)
        echo ""
        echo "Starting local development environment..."
        docker-compose up -d
        
        echo ""
        echo -e "${GREEN}✓ Services started!${NC}"
        echo ""
        echo "Access points:"
        echo "  - API: http://localhost:8000"
        echo "  - Health Check: http://localhost:8000/health"
        echo ""
        echo "Useful commands:"
        echo "  - View logs: docker-compose logs -f"
        echo "  - Stop services: docker-compose down"
        echo "  - Restart: docker-compose restart"
        ;;
        
    2)
        echo ""
        echo "Checking Kubernetes access..."
        if ! command -v kubectl &> /dev/null; then
            echo -e "${RED}✗ kubectl is not installed${NC}"
            echo "Install kubectl: https://kubernetes.io/docs/tasks/tools/"
            exit 1
        fi
        
        echo ""
        echo "Deploying to Kubernetes..."
        kubectl apply -f k8s/
        
        echo ""
        echo -e "${GREEN}✓ Kubernetes resources created!${NC}"
        echo ""
        echo "Monitor deployment:"
        echo "  - kubectl get pods -n marketing-agent"
        echo "  - kubectl get services -n marketing-agent"
        echo "  - kubectl logs -f deployment/marketing-agent-api -n marketing-agent"
        ;;
        
    3)
        echo ""
        echo "Starting development mode with hot reload..."
        docker-compose --profile dev up
        
        echo ""
        echo "Development server: http://localhost:8001"
        ;;
        
    4)
        echo ""
        echo "Building Docker image..."
        docker build -t marketing-agent:latest .
        
        echo ""
        echo -e "${GREEN}✓ Image built successfully!${NC}"
        echo ""
        echo "Run container:"
        echo "  docker run -d -p 8000:8000 --env-file .env marketing-agent:latest"
        ;;
        
    5)
        echo ""
        echo "Running tests..."
        docker-compose run --rm api pytest -v
        ;;
        
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo "=============================================="
echo "Setup complete!"
echo "=============================================="
