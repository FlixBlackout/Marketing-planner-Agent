# =============================================================================
# AWS Quick Deploy Script - Marketing Planning Assistant
# Free Tier Optimized (App Runner)
# =============================================================================

Write-Host ""
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "  AWS Quick Deploy - Marketing Planning Assistant" -ForegroundColor Cyan
Write-Host "  Free Tier Optimized (App Runner + ECR)" -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host ""

# Check prerequisites
Write-Host "[1/6] Checking prerequisites..." -ForegroundColor Yellow

$awsCliInstalled = Get-Command aws -ErrorAction SilentlyContinue
if (-not $awsCliInstalled) {
    Write-Host "[ERROR] AWS CLI is not installed!" -ForegroundColor Red
    Write-Host "Install from: https://aws.amazon.com/cli/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

$dockerInstalled = Get-Command docker -ErrorAction SilentlyContinue
if (-not $dockerInstalled) {
    Write-Host "[ERROR] Docker is not installed!" -ForegroundColor Red
    Write-Host "Install from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[OK] Prerequisites checked" -ForegroundColor Green
Write-Host ""

# Get AWS Account ID
Write-Host "[2/6] Getting AWS Account ID..." -ForegroundColor Yellow
$awsAccount = aws sts get-caller-identity --query Account --output text 2>$null
if (-not $awsAccount) {
    Write-Host "[ERROR] AWS CLI not configured! Run 'aws configure' first." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "[OK] Account ID: $awsAccount" -ForegroundColor Green
Write-Host ""

# Configuration
$region = "us-east-1"
$ecrRepo = "$awsAccount.dkr.ecr.$region.amazonaws.com/marketing-agent"

# Create ECR Repository
Write-Host "[3/6] Creating ECR repository..." -ForegroundColor Yellow
aws ecr create-repository --repository-name marketing-agent --region $region *>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] ECR repository created!" -ForegroundColor Green
} else {
    Write-Host "[OK] ECR repository already exists!" -ForegroundColor Green
}
Write-Host ""

# Login to ECR
Write-Host "[4/6] Logging in to Amazon ECR..." -ForegroundColor Yellow
aws ecr get-login-password --region $region | docker login --username AWS --password-stdin $ecrRepo *>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to login to ECR!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "[OK] ECR login successful!" -ForegroundColor Green
Write-Host ""

# Build Docker Image
Write-Host "[5/6] Building Docker image..." -ForegroundColor Yellow
Set-Location ..
docker build -t marketing-agent:latest .
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to build Docker image!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "[OK] Docker image built!" -ForegroundColor Green
Write-Host ""

# Tag and Push
Write-Host "[6/6] Pushing image to ECR..." -ForegroundColor Yellow
docker tag marketing-agent:latest $ecrRepo:latest
docker push $ecrRepo:latest
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to push image to ECR!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "[OK] Image pushed to ECR!" -ForegroundColor Green
Write-Host ""

# Deployment instructions
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "  Image Successfully Pushed to ECR!" -ForegroundColor Green
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "ECR Repository: $ecrRepo" -ForegroundColor Yellow
Write-Host ""
Write-Host "Next Steps (Choose one):" -ForegroundColor Yellow
Write-Host ""
Write-Host "OPTION 1: AWS Console (Easiest - Recommended)" -ForegroundColor Cyan
Write-Host "1. Go to: https://console.aws.amazon.com/apprunner" -ForegroundColor White
Write-Host "2. Click 'Create a service'" -ForegroundColor White
Write-Host "3. Choose 'Container registry' -> 'Amazon ECR'" -ForegroundColor White
Write-Host "4. Select image: marketing-agent:latest" -ForegroundColor White
Write-Host "5. Configure:" -ForegroundColor White
Write-Host "   - Port: 8000" -ForegroundColor White
Write-Host "   - Environment variables:" -ForegroundColor White
Write-Host "     OPENROUTER_API_KEY = your-api-key-here" -ForegroundColor White
Write-Host "     REDIS_URL = redis://localhost:6379/0" -ForegroundColor White
Write-Host "6. Click 'Create & Deploy'" -ForegroundColor White
Write-Host ""
Write-Host "OPTION 2: CloudFormation (Automated)" -ForegroundColor Cyan
Write-Host "Run this command in PowerShell:" -ForegroundColor White
Write-Host ""
Write-Host "aws cloudformation create-stack ``" -ForegroundColor White
Write-Host "  --stack-name marketing-agent ``" -ForegroundColor White
Write-Host "  --template-body file://aws/cloudformation-apprunner.yaml ``" -ForegroundColor White
Write-Host "  --parameters ParameterKey=OpenRouterApiKey,ParameterValue=YOUR_KEY ``" -ForegroundColor White
Write-Host "  --capabilities CAPABILITY_IAM ``" -ForegroundColor White
Write-Host "  --region us-east-1" -ForegroundColor White
Write-Host ""
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Free Tier Benefits:" -ForegroundColor Green
Write-Host "  - App Runner: 100 GB-hours/month FREE" -ForegroundColor Green
Write-Host "  - ECR Storage: 1 GB FREE" -ForegroundColor Green
Write-Host "  - Estimated Cost: ~$0/month" -ForegroundColor Green
Write-Host ""
Write-Host "After deployment, your app will be available at:" -ForegroundColor Yellow
Write-Host "  https://xxxxx.us-east-1.awsapprunner.com" -ForegroundColor White
Write-Host ""

Read-Host "Press Enter to exit"
