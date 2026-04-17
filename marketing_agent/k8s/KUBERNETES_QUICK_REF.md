# Kubernetes Quick Reference - Marketing Planning Assistant

## 🚀 Quick Start

### 1. Enable Kubernetes in Docker Desktop
- Open Docker Desktop → Settings → Kubernetes → Enable Kubernetes → Apply & Restart
- Wait 5-10 minutes

### 2. Deploy Everything (One Command)
```powershell
cd c:\Planner Agent\marketing_agent\k8s
.\setup-k8s.bat
```

### 3. Access Application
```powershell
kubectl port-forward service/marketing-agent-service 8080:80 -n marketing-agent
```
Open: http://localhost:8080

---

## 📋 Essential Commands

### Check Status
```powershell
# View all resources
kubectl get all -n marketing-agent

# View pods
kubectl get pods -n marketing-agent

# View services
kubectl get services -n marketing-agent

# View deployments
kubectl get deployments -n marketing-agent
```

### View Logs
```powershell
# API logs (follow mode)
kubectl logs -f deployment/marketing-agent-api -n marketing-agent

# Redis logs
kubectl logs -f deployment/redis -n marketing-agent

# Last 100 lines
kubectl logs deployment/marketing-agent-api -n marketing-agent --tail=100
```

### Debug Issues
```powershell
# Describe pod (shows events and status)
kubectl describe pod <pod-name> -n marketing-agent

# Check events
kubectl get events -n marketing-agent --sort-by='.lastTimestamp'

# Enter pod shell
kubectl exec -it <pod-name> -n marketing-agent -- /bin/sh
```

### Scale Application
```powershell
# Manual scaling
kubectl scale deployment marketing-agent-api --replicas=5 -n marketing-agent

# Check HPA status
kubectl get hpa -n marketing-agent
```

### Update Deployment
```powershell
# Restart all pods
kubectl rollout restart deployment/marketing-agent-api -n marketing-agent

# Check rollout status
kubectl rollout status deployment/marketing-agent-api -n marketing-agent

# View rollout history
kubectl rollout history deployment/marketing-agent-api -n marketing-agent
```

### Port Forwarding
```powershell
# Forward to service
kubectl port-forward service/marketing-agent-service 8080:80 -n marketing-agent

# Forward to specific pod
kubectl port-forward <pod-name> 8080:8000 -n marketing-agent
```

---

## 🔧 Common Tasks

### Rebuild and Redeploy
```powershell
# 1. Build new image
cd c:\Planner Agent\marketing_agent
docker build -t marketing-agent:k8s .

# 2. Restart deployment (uses new image)
kubectl rollout restart deployment/marketing-agent-api -n marketing-agent

# 3. Watch pods restart
kubectl get pods -n marketing-agent -w
```

### Update API Key
```powershell
# Delete old secret
kubectl delete secret marketing-agent-secrets -n marketing-agent

# Create new secret
kubectl create secret generic marketing-agent-secrets ^
  --from-literal=openrouter-api-key=YOUR-NEW-KEY ^
  --namespace=marketing-agent

# Restart pods to pick up new secret
kubectl rollout restart deployment/marketing-agent-api -n marketing-agent
```

### Test API
```powershell
# Health check
curl http://localhost:8080/health

# Generate plan
curl -X POST http://localhost:8080/plan ^
  -H "Content-Type: application/json" ^
  -d "{\"goal\":\"Increase brand awareness\",\"use_ai\":true,\"duration_days\":14}"
```

---

## 🗑️ Cleanup

### Remove Everything
```powershell
cd c:\Planner Agent\marketing_agent\k8s
.\cleanup-k8s.bat
```

**Or manually:**
```powershell
# Delete namespace
kubectl delete namespace marketing-agent

# Remove Docker image
docker rmi marketing-agent:k8s
```

---

## 📊 Architecture

```
Namespace: marketing-agent
├── Deployment: marketing-agent-api (2-10 replicas)
│   ├── Image: marketing-agent:k8s
│   ├── Port: 8000
│   ├── Resources: 256Mi-512Mi RAM, 250m-1000m CPU
│   └── Secret: marketing-agent-secrets
│
├── Deployment: redis (1 replica)
│   ├── Image: redis:7-alpine
│   ├── Port: 6379
│   └── PVC: 1GB storage
│
├── Service: marketing-agent-service (LoadBalancer)
│   └── Port: 80 → 8000
│
├── Service: redis-service (ClusterIP)
│   └── Port: 6379
│
└── HPA: marketing-agent-hpa
    ├── Min: 2 replicas
    ├── Max: 10 replicas
    └── Triggers: CPU 70%, Memory 80%
```

---

## ⚠️ Troubleshooting

### Pods in Pending State
```powershell
# Check why
kubectl describe pod <pod-name> -n marketing-agent

# Common fix: Check Docker Desktop has enough resources
# Settings → Resources → Increase CPU/Memory
```

### ImagePullBackOff Error
```powershell
# Verify image exists
docker images | findstr marketing-agent

# Rebuild if missing
docker build -t marketing-agent:k8s .
```

### CrashLoopBackOff Error
```powershell
# Check logs
kubectl logs <pod-name> -n marketing-agent

# Check if secret exists
kubectl get secret marketing-agent-secrets -n marketing-agent
```

### Service Not Accessible
```powershell
# Check service
kubectl get service marketing-agent-service -n marketing-agent

# Port forward manually
kubectl port-forward service/marketing-agent-service 8080:80 -n marketing-agent
```

---

## 📚 File Structure

```
k8s/
├── deployment.yaml        # API deployment + HPA
├── service.yaml           # Services + Redis + Namespace + Secrets
├── setup-k8s.bat          # Automated setup script
├── cleanup-k8s.bat        # Cleanup script
└── KUBERNETES_QUICK_REF.md # This file
```

---

## 🎯 Production Checklist

Before deploying to production (AWS EKS, GCP GKE, Azure AKS):

- [ ] Push image to container registry (GitHub Container Registry, Docker Hub, etc.)
- [ ] Update deployment.yaml image to registry URL
- [ ] Change `imagePullPolicy` to `Always`
- [ ] Configure proper Ingress with SSL/TLS
- [ ] Use managed Redis (AWS ElastiCache, GCP Memorystore, Azure Cache)
- [ ] Set up monitoring (Prometheus + Grafana)
- [ ] Configure log aggregation (ELK Stack, CloudWatch, etc.)
- [ ] Set up backup strategy for Redis
- [ ] Configure network policies
- [ ] Set up CI/CD pipeline
- [ ] Configure resource quotas and limits
- [ ] Enable pod disruption budgets
- [ ] Set up alerts and notifications

---

## 💡 Tips

1. **Always check logs first** when something goes wrong
2. **Use `kubectl describe`** to get detailed pod information
3. **Watch pods** with `-w` flag to see real-time changes
4. **Use namespaces** to isolate different environments
5. **Keep secrets secure** - never commit them to Git
6. **Test locally** with Docker Compose before deploying to K8s
7. **Monitor resource usage** with `kubectl top pods`

---

## 🔗 Useful Links

- Kubernetes Docs: https://kubernetes.io/docs/
- kubectl Cheat Sheet: https://kubernetes.io/docs/reference/kubectl/cheatsheet/
- Docker Desktop K8s: https://docs.docker.com/desktop/kubernetes/
- Helm (Package Manager): https://helm.sh/

---

**Need Help?** Check the full guide: `KUBERNETES_SETUP.md`
