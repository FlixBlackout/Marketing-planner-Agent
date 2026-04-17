# =============================================================================
# AWS Free Tier Deployment Guide - Marketing Planning Assistant
# =============================================================================

## 🎯 Deployment Strategy: AWS Free Tier Optimized

This guide shows you how to deploy your Marketing Planning Assistant to AWS using **only free tier resources**.

### Free Tier Components:
- ✅ **AWS App Runner** - Free for first 100GB-hours/month (sufficient for small apps)
- ✅ **Amazon ECR** - Free 1GB storage (enough for your Docker image)
- ✅ **AWS Free Tier** - 750 hours/month of compute (App Runner)
- ✅ **Upstash Redis** - Free tier (10K commands/day) - Alternative to self-hosted Redis

**Total Cost: ~$0/month** (within free tier limits)

---

## 📋 Prerequisites

1. AWS Account (with free tier eligibility)
2. AWS CLI installed and configured
3. Docker installed
4. Your OpenRouter API key

---

## 🚀 Option 1: AWS App Runner (RECOMMENDED - Easiest)

**Why App Runner?**
- Fully managed container service
- Automatic HTTPS
- Auto-scaling included
- Free tier: 100 GB-hours/month
- No Kubernetes complexity

### Step 1: Build and Push Docker Image to ECR

```powershell
# 1. Login to AWS ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

# 2. Create ECR repository
aws ecr create-repository --repository-name marketing-agent --region us-east-1

# 3. Build Docker image
cd marketing_agent
docker build -t marketing-agent:latest .

# 4. Tag and push to ECR
docker tag marketing-agent:latest <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/marketing-agent:latest
docker push <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/marketing-agent:latest
```

### Step 2: Deploy to App Runner via AWS Console

1. Go to **AWS App Runner** console
2. Click **Create an App Runner service**
3. Choose **Container registry** → **Amazon ECR**
4. Select your image: `marketing-agent:latest`
5. Configure service:
   - **Service name**: `marketing-agent`
   - **Port**: `8000`
   - **Environment variables**:
     - `OPENROUTER_API_KEY`: `your-api-key-here`
     - `REDIS_URL`: `redis://default:@localhost:6379/0` (or Upstash URL)
   - **Instance type**: `1 vCPU, 2 GB memory` (cheapest option)
6. Click **Create & Deploy**

### Step 3: Access Your Application

App Runner provides a public URL: `https://xxxxx.us-east-1.awsapprunner.com`

---

## 🔧 Option 2: AWS ECS Fargate (Serverless Containers)

**Why ECS Fargate?**
- Serverless (no EC2 management)
- Pay only for what you use
- Free tier: 750 hours/month (first 12 months)

### Step 1: Create ECS Cluster

```powershell
# Create cluster
aws ecs create-cluster --cluster-name marketing-agent-cluster --region us-east-1
```

### Step 2: Create Task Definition

Use the `aws/ecs-task-definition.json` file provided in this repository.

```powershell
aws ecs register-task-definition --cli-input-json file://aws/ecs-task-definition.json --region us-east-1
```

### Step 3: Deploy Service

```powershell
aws ecs create-service ^
  --cluster marketing-agent-cluster ^
  --service-name marketing-agent-service ^
  --task-definition marketing-agent ^
  --desired-count 1 ^
  --launch-type FARGATE ^
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxxxx],securityGroups=[sg-xxxxx],assignPublicIp=ENABLED}" ^
  --region us-east-1
```

---

## 📦 Option 3: Amazon EC2 (Free Tier - t2.micro)

**Why EC2?**
- 750 hours/month free (t2.micro instance)
- Full control
- Good for learning AWS

### Step 1: Launch EC2 Instance

```powershell
# Launch t2.micro instance (free tier eligible)
aws ec2 run-instances ^
  --image-id ami-0c55b159cbfafe1f0 ^
  --count 1 ^
  --instance-type t2.micro ^
  --key-name YourKeyPair ^
  --security-group-ids sg-xxxxx ^
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=marketing-agent}]' ^
  --region us-east-1
```

### Step 2: Install Docker and Deploy

SSH into your instance and run:

```bash
# Install Docker
sudo yum update -y
sudo yum install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user

# Pull and run
docker run -d -p 80:8000 \
  -e OPENROUTER_API_KEY=your-key \
  your-account.dkr.ecr.us-east-1.amazonaws.com/marketing-agent:latest
```

---

## 💾 Redis Options (Free Tier)

### Option 1: Disable Redis (Simplest)
If you don't need caching/sessions, remove Redis dependency.

### Option 2: Upstash Redis (FREE)
- Sign up: https://upstash.com
- Create free Redis database
- Get connection URL: `redis://default:password@endpoint:port`
- Set environment variable: `REDIS_URL=your-upstash-url`

### Option 3: Self-hosted on EC2
Deploy Redis on the same EC2 instance (uses more resources).

---

## 🔒 Security Best Practices

1. **Store secrets in AWS Secrets Manager** (free for first 10,000 API calls/month)
2. **Use IAM roles** instead of hardcoded credentials
3. **Enable HTTPS** (App Router does this automatically)
4. **Restrict security groups** to necessary ports only
5. **Enable CloudWatch logging** (free tier: 5GB ingestion/month)

---

## 📊 Cost Estimation (Monthly)

| Service | Usage | Cost |
|---------|-------|------|
| **App Runner** | 100 GB-hours | $0 (free tier) |
| **ECR Storage** | 1 GB | $0 (free tier) |
| **Upstash Redis** | 10K commands/day | $0 (free tier) |
| **CloudWatch Logs** | 5 GB | $0 (free tier) |
| **TOTAL** | | **~$0/month** |

---

## 🔄 CI/CD with GitHub Actions

See `.github/workflows/aws-deploy.yml` for automated deployment pipeline.

---

## 🗑️ Cleanup (Avoid Unexpected Charges)

```powershell
# Delete App Runner service
aws apprunner delete-service --service-arn arn:aws:apprunner:us-east-1:ACCOUNT:service/marketing-agent/xxxxx

# Delete ECR repository
aws ecr delete-repository --repository-name marketing-agent --force --region us-east-1

# Delete ECS cluster (if used)
aws ecs delete-service --cluster marketing-agent-cluster --service marketing-agent-service --force
aws ecs delete-cluster --cluster marketing-agent-cluster
```

---

## 📚 Quick Commands Reference

```powershell
# Check App Runner service status
aws apprunner describe-service --service-arn YOUR_ARN

# View logs
aws apprunner list-operations --service-arn YOUR_ARN

# Update service
aws apprunner update-service --service-arn YOUR_ARN

# Restart deployment
aws apprunner start-deployment --service-arn YOUR_ARN
```

---

## ⚠️ Important Notes

1. **Free tier is only for 12 months** after AWS account creation
2. **Monitor your usage** in AWS Cost Explorer
3. **Set billing alerts** to avoid surprise charges
4. **App Runner is the easiest** option for beginners
5. **EC2 requires more management** but gives you full control

---

## 🆘 Troubleshooting

### Container won't start
```powershell
# Check logs in App Runner console
# Or via CLI:
aws apprunner list-operations --service-arn YOUR_ARN
```

### Can't connect to Redis
```powershell
# Verify REDIS_URL environment variable
# Check security group allows outbound traffic
```

### High costs
```powershell
# Check AWS Cost Explorer
# Ensure you're within free tier limits
# Delete unused resources
```

---

**Ready to deploy?** Start with **Option 1: App Runner** for the easiest experience!
