@echo off
REM =============================================================================
REM Kubernetes Setup Script for Marketing Planning Assistant
REM =============================================================================

echo.
echo ========================================================================
echo   Kubernetes Setup for Marketing Planning Assistant
echo ========================================================================
echo.

REM Check if Docker is running
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)

echo [1/7] Checking Kubernetes status...
kubectl cluster-info >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [WARNING] Kubernetes is not enabled in Docker Desktop!
    echo.
    echo To enable Kubernetes:
    echo 1. Open Docker Desktop
    echo 2. Go to Settings (gear icon)
    echo 3. Click on "Kubernetes" in left sidebar
    echo 4. Check "Enable Kubernetes"
    echo 5. Click "Apply ^& Restart"
    echo 6. Wait 5-10 minutes for Kubernetes to start
    echo.
    echo Then run this script again.
    echo.
    pause
    exit /b 1
)

echo [OK] Kubernetes is running!
echo.

echo [2/7] Building Docker image...
cd ..
docker build -t marketing-agent:k8s .
if %errorlevel% neq 0 (
    echo [ERROR] Failed to build Docker image!
    pause
    exit /b 1
)
echo [OK] Docker image built successfully!
echo.

cd k8s

echo [3/7] Creating namespace...
kubectl create namespace marketing-agent 2>nul
if %errorlevel% neq 0 (
    echo [OK] Namespace already exists
) else (
    echo [OK] Namespace created!
)
echo.

echo [4/7] Creating API key secret...
set /p API_KEY="Enter your OpenRouter API key (or press Enter to use default): "
if "%API_KEY%"=="" (
    set API_KEY=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
)

kubectl delete secret marketing-agent-secrets -n marketing-agent 2>nul
kubectl create secret generic marketing-agent-secrets ^
  --from-literal=openrouter-api-key=%API_KEY% ^
  --namespace=marketing-agent

if %errorlevel% neq 0 (
    echo [ERROR] Failed to create secret!
    pause
    exit /b 1
)
echo [OK] Secret created!
echo.

echo [5/7] Deploying Redis...
kubectl apply -f service.yaml
if %errorlevel% neq 0 (
    echo [ERROR] Failed to deploy Redis!
    pause
    exit /b 1
)
echo [OK] Redis deployed!
echo.

echo [6/7] Deploying API...
kubectl apply -f deployment.yaml
if %errorlevel% neq 0 (
    echo [ERROR] Failed to deploy API!
    pause
    exit /b 1
)
echo [OK] API deployed!
echo.

echo [7/7] Waiting for pods to be ready...
timeout /t 10 /nobreak >nul
echo.

echo ========================================================================
echo   Deployment Status
echo ========================================================================
echo.

kubectl get pods -n marketing-agent
echo.

kubectl get services -n marketing-agent
echo.

kubectl get deployments -n marketing-agent
echo.

echo ========================================================================
echo   Next Steps
echo ========================================================================
echo.
echo 1. Wait 1-2 minutes for all pods to be in "Running" state
echo 2. Check status: kubectl get pods -n marketing-agent
echo 3. Access application: kubectl port-forward service/marketing-agent-service 8080:80 -n marketing-agent
echo 4. Open browser: http://localhost:8080
echo.
echo To view logs:
echo   kubectl logs -f deployment/marketing-agent-api -n marketing-agent
echo.
echo To scale:
echo   kubectl scale deployment marketing-agent-api --replicas=5 -n marketing-agent
echo.
echo ========================================================================
echo.

pause
