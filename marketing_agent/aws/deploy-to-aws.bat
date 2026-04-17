@echo off
REM =============================================================================
REM AWS App Runner Deployment Script - Marketing Planning Assistant
REM =============================================================================

echo.
echo ========================================================================
echo   AWS App Runner Deployment - Marketing Planning Assistant
echo ========================================================================
echo.

REM Check if AWS CLI is installed
aws --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] AWS CLI is not installed!
    echo Install from: https://aws.amazon.com/cli/
    pause
    exit /b 1
)

REM Check if Docker is running
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)

echo [1/7] Getting AWS Account ID...
for /f "tokens=*" %%i in ('aws sts get-caller-identity --query Account --output text') do set ACCOUNT_ID=%%i
if "%ACCOUNT_ID%"=="" (
    echo [ERROR] Unable to get AWS Account ID. Run 'aws configure' first.
    pause
    exit /b 1
)
echo [OK] Account ID: %ACCOUNT_ID%
echo.

set REGION=us-east-1
set ECR_REPO=%ACCOUNT_ID%.dkr.ecr.%REGION%.amazonaws.com/marketing-agent

echo [2/7] Creating ECR repository (if not exists)...
aws ecr create-repository --repository-name marketing-agent --region %REGION% >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] ECR repository created!
) else (
    echo [OK] ECR repository already exists!
)
echo.

echo [3/7] Logging in to Amazon ECR...
aws ecr get-login-password --region %REGION% | docker login --username AWS --password-stdin %ECR_REPO%
if %errorlevel% neq 0 (
    echo [ERROR] Failed to login to ECR!
    pause
    exit /b 1
)
echo [OK] ECR login successful!
echo.

echo [4/7] Building Docker image...
cd ..
docker build -t marketing-agent:latest .
if %errorlevel% neq 0 (
    echo [ERROR] Failed to build Docker image!
    pause
    exit /b 1
)
echo [OK] Docker image built!
echo.

cd aws

echo [5/7] Tagging image for ECR...
docker tag marketing-agent:latest %ECR_REPO%:latest
if %errorlevel% neq 0 (
    echo [ERROR] Failed to tag image!
    pause
    exit /b 1
)
echo [OK] Image tagged!
echo.

echo [6/7] Pushing image to ECR...
docker push %ECR_REPO%:latest
if %errorlevel% neq 0 (
    echo [ERROR] Failed to push image to ECR!
    pause
    exit /b 1
)
echo [OK] Image pushed to ECR!
echo.

echo [7/7] Deploying to App Runner...
echo.
echo ========================================================================
echo   Next Steps
echo ========================================================================
echo.
echo Your Docker image has been pushed to ECR:
echo   %ECR_REPO%:latest
echo.
echo Now deploy to App Runner:
echo.
echo OPTION 1: Using AWS Console (Easiest)
echo 1. Go to: https://console.aws.amazon.com/apprunner
echo 2. Click "Create a service"
echo 3. Choose "Container registry" -^> "Amazon ECR"
echo 4. Select image: marketing-agent:latest
echo 5. Configure:
echo    - Port: 8000
echo    - Environment variables:
echo      OPENROUTER_API_KEY = your-api-key
echo      REDIS_URL = redis://localhost:6379/0
echo 6. Click "Create ^& Deploy"
echo.
echo OPTION 2: Using CloudFormation
echo Run: aws cloudformation create-stack ^
echo   --stack-name marketing-agent ^
echo   --template-body file://cloudformation-apprunner.yaml ^
echo   --parameters ParameterKey=OpenRouterApiKey,ParameterValue=YOUR_KEY ^
echo   --capabilities CAPABILITY_IAM ^
echo   --region us-east-1
echo.
echo ========================================================================
echo.

pause
