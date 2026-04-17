# Kubernetes Setup Guide for Marketing Planning Assistant

## Overview
This guide will help you set up Kubernetes locally using Docker Desktop's built-in Kubernetes cluster.

## Prerequisites
- Docker Desktop installed and running
- kubectl installed (already installed on your system)
- At least 4GB RAM available for Kubernetes

---

## Step 1: Enable Kubernetes in Docker Desktop

1. **Open Docker Desktop**
   - Click on the Docker icon in system tray
   - Click on "Settings" (gear icon)

2. **Enable Kubernetes**
   - Go to "Kubernetes" in the left sidebar
   - Check "Enable Kubernetes"
   - Click "Apply & Restart"
   - Wait for Kubernetes to start (5-10 minutes)

3. **Verify Kubernetes is Running**
   ```powershell
   kubectl cluster-info
   kubectl get nodes
   ```

   You should see:
   ```
   Kubernetes control plane is running at https://kubernetes.docker.internal:6443
   NAME             STATUS   ROLES           AGE   VERSION
   docker-desktop   Ready    control-plane   1m    v1.xx.x
   ```

---

## Step 2: Create Kubernetes Secret with Your API Key

Your OpenRouter API key needs to be stored as a Kubernetes Secret:

```powershell
# Navigate to the k8s directory
cd c:\Planner Agent\marketing_agent\k8s

# Create the secret with your actual API key
kubectl create secret generic marketing-agent-secrets `
  --from-literal=openrouter-api-key=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 `
  --namespace=marketing-agent
```

**Note:** If the namespace doesn't exist yet, it will be created automatically when you apply the manifests.

---

## Step 3: Build Docker Image for Kubernetes

Kubernetes needs the Docker image to be available locally:

```powershell
# Navigate to marketing_agent directory
cd c:\Planner Agent\marketing_agent

# Build the Docker image
docker build -t marketing-agent:k8s .

# Verify the image was built
docker images | findstr marketing-agent
```

---

## Step 4: Update Deployment Image

The deployment.yaml currently points to a remote registry. Update it to use the local image:

**File:** `k8s/deployment.yaml` (Line 45)

Change:
```yaml
image: ghcr.io/marketing-agent:latest
```

To:
```yaml
image: marketing-agent:k8s
imagePullPolicy: IfNotPresent
```

---

## Step 5: Deploy to Kubernetes

### Option A: Deploy Everything at Once

```powershell
cd c:\Planner Agent\marketing_agent\k8s

# Apply all configurations
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

### Option B: Deploy Step by Step (Recommended)

```powershell
cd c:\Planner Agent\marketing_agent\k8s

# 1. Create namespace and service account
kubectl apply -f deployment.yaml

# 2. Create services and ingress
kubectl apply -f service.yaml

# 3. Verify everything is running
kubectl get all -n marketing-agent
```

---

## Step 6: Verify Deployment

### Check Pods
```powershell
kubectl get pods -n marketing-agent
```

Expected output:
```
NAME                                   READY   STATUS    RESTARTS   AGE
marketing-agent-api-xxxxxxxxx-xxxxx    1/1     Running   0          2m
marketing-agent-api-xxxxxxxxx-xxxxx    1/1     Running   0          2m
redis-xxxxxxxxx-xxxxx                  1/1     Running   0          2m
```

### Check Services
```powershell
kubectl get services -n marketing-agent
```

Expected output:
```
NAME                    TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
marketing-agent-service LoadBalancer   10.96.x.x       localhost     80:30000/TCP   2m
redis-service           ClusterIP      10.96.x.x       <none>        6379/TCP       2m
```

### Check Deployment Status
```powershell
kubectl get deployments -n marketing-agent
```

---

## Step 7: Access the Application

### Via Port Forwarding (Recommended for Local Testing)

```powershell
# Forward port 8080 to the service
kubectl port-forward service/marketing-agent-service 8080:80 -n marketing-agent
```

Then access:
- **Application**: http://localhost:8080
- **Health Check**: http://localhost:8080/health

### Via LoadBalancer (Docker Desktop)

Docker Desktop exposes LoadBalancer services on localhost:

- **Application**: http://localhost
- **Health Check**: http://localhost/health

---

## Step 8: Monitor and Troubleshoot

### View Pod Logs
```powershell
# API logs
kubectl logs -f deployment/marketing-agent-api -n marketing-agent

# Redis logs
kubectl logs -f deployment/redis -n marketing-agent
```

### Check Pod Status
```powershell
kubectl describe pod -l app=marketing-agent -n marketing-agent
```

### Check Events
```powershell
kubectl get events -n marketing-agent --sort-by='.lastTimestamp'
```

### Execute Commands in Pod
```powershell
# Enter API pod shell
kubectl exec -it deployment/marketing-agent-api -n marketing-agent -- /bin/sh

# Test API from inside the cluster
kubectl exec deployment/marketing-agent-api -n marketing-agent -- curl http://localhost:8000/health
```

---

## Step 9: Test the Application

```powershell
# Health check
curl http://localhost:8080/health

# Generate a marketing plan
curl -X POST http://localhost:8080/plan `
  -H "Content-Type: application/json" `
  -d "{\"goal\":\"Increase brand awareness\",\"use_ai\":true,\"duration_days\":14}"
```

---

## Step 10: Scaling

### Manual Scaling
```powershell
# Scale to 5 replicas
kubectl scale deployment marketing-agent-api --replicas=5 -n marketing-agent
```

### Auto-Scaling (HPA)
The Horizontal Pod Autoscaler is already configured in deployment.yaml:
- Min replicas: 2
- Max replicas: 10
- Triggers: CPU > 70%, Memory > 80%

Check HPA status:
```powershell
kubectl get hpa -n marketing-agent
```

---

## Cleanup

### Stop Kubernetes (Keep Docker Desktop)
```powershell
# Delete all resources
kubectl delete namespace marketing-agent
```

### Disable Kubernetes in Docker Desktop
1. Open Docker Desktop Settings
2. Go to Kubernetes
3. Uncheck "Enable Kubernetes"
4. Click "Apply & Restart"

---

## Common Issues

### Issue 1: Pods stuck in Pending
**Solution:** Check resources
```powershell
kubectl describe pod <pod-name> -n marketing-agent
```

### Issue 2: ImagePullBackOff
**Solution:** Ensure image is built
```powershell
docker images | findstr marketing-agent
```

### Issue 3: CrashLoopBackOff
**Solution:** Check logs
```powershell
kubectl logs <pod-name> -n marketing-agent
```

### Issue 4: Secret not found
**Solution:** Recreate secret
```powershell
kubectl delete secret marketing-agent-secrets -n marketing-agent
kubectl create secret generic marketing-agent-secrets `
  --from-literal=openrouter-api-key=YOUR-API-KEY `
  --namespace=marketing-agent
```

---

## Architecture Overview

```
                    Kubernetes Cluster (Docker Desktop)
┌─────────────────────────────────────────────────────┐
│                                                      │
│  ┌────────────────────────────────────────────┐     │
│  │         LoadBalancer Service               │     │
│  │         marketing-agent-service            │     │
│  │         Port: 80 -> 8000                   │     │
│  └──────────────┬─────────────────────────────┘     │
│                 │                                    │
│          ┌──────┴──────┐                            │
│          ▼             ▼                            │
│  ┌────────────┐  ┌────────────┐                    │
│  │  API Pod 1 │  │  API Pod 2 │  ← 2-10 replicas   │
│  │ (Port 8000)│  │ (Port 8000)│                    │
│  └────────────┘  └────────────┘                    │
│                                                      │
│  ┌────────────────────────────────────────────┐     │
│  │         Redis Deployment                   │     │
│  │         redis-service:6379                 │     │
│  │         Persistent Volume: 1GB             │     │
│  └────────────────────────────────────────────┘     │
│                                                      │
│  ┌────────────────────────────────────────────┐     │
│  │    Horizontal Pod Autoscaler (HPA)         │     │
│  │    Min: 2, Max: 10                         │     │
│  │    Trigger: CPU 70%, Memory 80%            │     │
│  └────────────────────────────────────────────┘     │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## Production Deployment

For production deployment to cloud providers (AWS EKS, GCP GKE, Azure AKS):

1. **Push image to container registry:**
   ```powershell
   docker tag marketing-agent:k8s ghcr.io/your-username/marketing-agent:latest
   docker push ghcr.io/your-username/marketing-agent:latest
   ```

2. **Update deployment.yaml:**
   - Change image to `ghcr.io/your-username/marketing-agent:latest`
   - Change `imagePullPolicy` to `Always`

3. **Configure proper Ingress with SSL**

4. **Use managed database instead of Redis pod**

5. **Set up monitoring with Prometheus/Grafana**

---

## Next Steps

1. Enable Kubernetes in Docker Desktop
2. Build the Docker image
3. Create the secret with your API key
4. Deploy using `kubectl apply`
5. Test the application
6. Monitor with `kubectl get all`

---

## Useful Commands Cheat Sheet

```powershell
# Get all resources
kubectl get all -n marketing-agent

# View logs
kubectl logs -f <pod-name> -n marketing-agent

# Execute into pod
kubectl exec -it <pod-name> -n marketing-agent -- /bin/sh

# Port forward
kubectl port-forward service/marketing-agent-service 8080:80 -n marketing-agent

# Scale deployment
kubectl scale deployment marketing-agent-api --replicas=3 -n marketing-agent

# Restart deployment
kubectl rollout restart deployment/marketing-agent-api -n marketing-agent

# Check rollout status
kubectl rollout status deployment/marketing-agent-api -n marketing-agent

# Delete everything
kubectl delete namespace marketing-agent
```

---

## Support

If you encounter issues:
1. Check pod logs: `kubectl logs <pod-name> -n marketing-agent`
2. Describe pod: `kubectl describe pod <pod-name> -n marketing-agent`
3. Check events: `kubectl get events -n marketing-agent`
4. Verify secret exists: `kubectl get secrets -n marketing-agent`
