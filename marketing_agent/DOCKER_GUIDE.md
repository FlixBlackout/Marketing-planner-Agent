# Docker & Kubernetes Setup Guide

## Overview

This guide explains how to containerize and deploy the Marketing Planning Assistant using Docker and Kubernetes with industry best practices.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Production Environment                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────────┐          │
│  │ Internet │───▶│  Nginx   │───▶│ Marketing    │          │
│  │          │    │ (Proxy)  │    │ Agent API    │          │
│  └──────────┘    └──────────┘    └──────┬───────┘          │
│                                        │                    │
│                                        ▼                    │
│                                 ┌──────────┐               │
│                                 │  Redis   │               │
│                                 │ (Cache)  │               │
│                                 └──────────┘               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Prerequisites

- Docker >= 20.10
- Docker Compose >= 2.0
- kubectl >= 1.24
- Kubernetes cluster (minikube, EKS, GKE, or AKS)
- Git

## Quick Start

### 1. Local Development with Docker Compose

```bash
# Clone the repository
git clone <repository-url>
cd marketing_agent

# Copy environment file
cp .env.example .env
# Edit .env with your API keys

# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f api

# Access the application
# API: http://localhost:8000
# Health: http://localhost:8000/health
```

### 2. Development Mode with Hot Reload

```bash
# Start in development mode
docker-compose --profile dev up

# Access development server
# http://localhost:8001
```

### 3. Building Docker Image

```bash
# Build production image
docker build -t marketing-agent:latest .

# Build with specific tag
docker build -t marketing-agent:v1.0.0 --target production .

# Run container
docker run -d \
  --name marketing-agent \
  -p 8000:8000 \
  --env-file .env \
  marketing-agent:latest
```

## Docker Best Practices Implemented

### Multi-Stage Build

The Dockerfile uses a multi-stage build to optimize image size:

- **Stage 1 (builder)**: Compiles dependencies in a full Python environment
- **Stage 2 (production)**: Creates minimal runtime image (~150MB vs ~900MB)

### Security Features

✅ **Non-root user**: Application runs as unprivileged user `appuser`
✅ **Minimal base image**: Uses `python:3.10-slim` instead of full image
✅ **No unnecessary packages**: Only runtime dependencies included
✅ **Read-only filesystem**: Root filesystem is read-only
✅ **Dropped capabilities**: All Linux capabilities dropped
✅ **Health checks**: Built-in health monitoring

### Optimization

✅ **Layer caching**: Dependencies installed before code copy
✅ **.dockerignore**: Excludes unnecessary files from build context
✅ **Alpine images**: Redis and Nginx use Alpine variants
✅ **Resource limits**: CPU and memory limits defined

## Docker Compose Configuration

### Services

| Service | Description | Port |
|---------|-------------|------|
| api | Marketing Planning Assistant | 8000 |
| redis | Cache and session storage | 6379 |
| nginx | Reverse proxy and load balancer | 80, 443 |
| dev | Development server (optional) | 8001 |

### Useful Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild and restart
docker-compose up -d --build

# Scale API instances
docker-compose up -d --scale api=3

# View running containers
docker-compose ps

# Execute command in container
docker-compose exec api bash

# View resource usage
docker stats
```

## Kubernetes Deployment

### 1. Setup Namespace and Secrets

```bash
# Create namespace
kubectl apply -f k8s/deployment.yaml

# Create secrets (replace with your actual values)
kubectl create secret generic marketing-agent-secrets \
  --from-literal=openrouter-api-key=your-api-key \
  --namespace=marketing-agent
```

### 2. Deploy Application

```bash
# Apply all Kubernetes manifests
kubectl apply -f k8s/

# Verify deployment
kubectl get pods -n marketing-agent
kubectl get services -n marketing-agent
kubectl get ingress -n marketing-agent

# View logs
kubectl logs -f deployment/marketing-agent-api -n marketing-agent
```

### 3. Autoscaling

The deployment includes Horizontal Pod Autoscaler (HPA):

- **Min replicas**: 2
- **Max replicas**: 10
- **CPU threshold**: 70%
- **Memory threshold**: 80%

```bash
# Check HPA status
kubectl get hpa -n marketing-agent

# View autoscaling events
kubectl describe hpa marketing-agent-hpa -n marketing-agent
```

### 4. Rolling Updates

```bash
# Update image
kubectl set image deployment/marketing-agent-api \
  api=marketing-agent:v2.0.0 -n marketing-agent

# Monitor rollout
kubectl rollout status deployment/marketing-agent-api -n marketing-agent

# Rollback if needed
kubectl rollout undo deployment/marketing-agent-api -n marketing-agent
```

## CI/CD Pipeline (GitHub Actions)

The pipeline includes:

1. **Test**: Run pytest and linting
2. **Build**: Create and push Docker image
3. **Security**: Trivy vulnerability scanning
4. **Deploy**: Automatic deployment to Kubernetes

### Setup GitHub Actions

1. Add repository secrets:
   - `OPENROUTER_API_KEY`: Your API key
   - `KUBE_CONFIG`: Base64 encoded Kubernetes config
   - `GITHUB_TOKEN`: Automatically provided

2. Push to main branch to trigger deployment

### Manual Build and Push

```bash
# Login to GitHub Container Registry
echo $GH_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Build and push
docker build -t ghcr.io/your-org/marketing-agent:latest .
docker push ghcr.io/your-org/marketing-agent:latest
```

## Monitoring and Logging

### Health Checks

```bash
# Check API health
curl http://localhost:8000/health

# Check Redis
docker-compose exec redis redis-cli ping
```

### Logging

Logs are configured with rotation:
- Max size: 10MB per file
- Max files: 3
- Driver: json-file

```bash
# View logs
docker-compose logs -f api

# Kubernetes logs
kubectl logs -f deployment/marketing-agent-api -n marketing-agent
```

### Prometheus Metrics

The application exposes metrics for Prometheus scraping:

- Annotations enabled in K8s deployment
- Port: 8000
- Path: /metrics

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| PORT | Application port | No (default: 8000) |
| OPENROUTER_API_KEY | LLM API key | Yes |
| OPENROUTER_BASE_URL | API base URL | No |
| OPENROUTER_MODEL | Model to use | No |
| REDIS_URL | Redis connection string | No |
| LOG_LEVEL | Logging level | No (default: info) |
| APP_ENV | Environment | No (default: production) |

## Troubleshooting

### Common Issues

**Issue**: Container won't start
```bash
# Check logs
docker-compose logs api

# Verify .env file exists
ls -la .env
```

**Issue**: Database connection failed
```bash
# Check Redis is running
docker-compose ps redis

# Test connection
docker-compose exec redis redis-cli ping
```

**Issue**: Image too large
```bash
# Check image layers
docker history marketing-agent:latest

# Ensure .dockerignore is present
cat .dockerignore
```

### Debug Mode

```bash
# Run with debug logging
docker-compose exec api bash
python -c "import logging; logging.basicConfig(level=logging.DEBUG)"

# Inspect container
docker inspect marketing-agent-api
```

## Performance Optimization

### Production Checklist

- [x] Multi-stage Dockerfile
- [x] Non-root user
- [x] Resource limits
- [x] Health checks
- [x] Log rotation
- [x] Gzip compression (Nginx)
- [x] Connection pooling
- [x] Caching (Redis)
- [x] Auto-scaling (K8s HPA)
- [x] Rolling updates
- [x] Security scanning

### Resource Recommendations

| Environment | CPU | Memory | Replicas |
|-------------|-----|--------|----------|
| Development | 0.25-0.5 | 256MB | 1 |
| Staging | 0.5-1.0 | 512MB | 2 |
| Production | 1.0-2.0 | 1GB | 3+ |

## Security Best Practices

1. **Never commit secrets**: Use environment variables or secrets manager
2. **Regular updates**: Keep base images updated
3. **Vulnerability scanning**: Trivy integrated in CI/CD
4. **Network policies**: Implement in Kubernetes
5. **TLS/SSL**: Enabled via Nginx
6. **Rate limiting**: Configured in Nginx
7. **Security headers**: X-Frame-Options, CSP, etc.

## Team Collaboration

### Communication Channels

1. **Daily standups**: Discuss progress and blockers
2. **Code reviews**: All PRs require review
3. **Documentation**: Keep this guide updated
4. **Issue tracking**: Use GitHub Issues

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/your-feature

# Commit changes
git add .
git commit -m "feat: add new feature"

# Push and create PR
git push origin feature/your-feature
```

## Next Steps

1. Set up monitoring with Grafana/Prometheus
2. Implement distributed tracing
3. Add database persistence
4. Configure backup strategies
5. Set up disaster recovery
6. Implement canary deployments

## Support

- **Documentation**: README.md files in each directory
- **Issues**: GitHub Issues
- **Team Chat**: [Your team communication channel]
