# =============================================================================
# AWS Free Tier Cost Optimization Guide
# =============================================================================

## 💰 How to Stay Within AWS Free Tier

This guide ensures your Marketing Planning Assistant runs on AWS for **~$0/month**.

---

## 🎯 Free Tier Limits (First 12 Months)

### Compute Options (Choose ONE):

#### Option 1: AWS App Runner ✅ RECOMMENDED
- **Free Tier**: 100 GB-hours/month
- **Your Usage**: ~720 GB-hours (1 service × 24h × 30 days)
- **Cost if exceeded**: $0.007/GB-hour
- **Tip**: Run 1 service only, stays within free tier

#### Option 2: EC2 t2.micro
- **Free Tier**: 750 hours/month
- **Your Usage**: 720 hours (24/7 for 30 days)
- **Cost if exceeded**: $0.0116/hour
- **Tip**: Only run 1 instance

#### Option 3: ECS Fargate
- **Free Tier**: 750 hours/month
- **Your Usage**: Depends on task count
- **Cost if exceeded**: $0.04048/vCPU-hour + $0.004445/GB-hour
- **Tip**: Use 0.25 vCPU, 0.5GB memory (smallest size)

---

## 📊 Cost Breakdown (Monthly Estimate)

| Resource | Free Tier | Your Usage | Overage Cost |
|----------|-----------|------------|--------------|
| **App Runner** | 100 GB-hours | ~30 GB-hours | $0 |
| **ECR Storage** | 1 GB | ~0.4 GB | $0 |
| **CloudWatch Logs** | 5 GB | ~0.1 GB | $0 |
| **Data Transfer Out** | 100 GB | ~1 GB | $0 |
| **Secrets Manager** | 10K API calls | ~1K calls | $0 |
| **TOTAL** | | | **$0/month** ✅ |

---

## ⚠️ Common Mistakes That Cost Money

### 1. Multiple Services Running
```
❌ BAD: Running 3 App Runner services
✅ GOOD: Run 1 service only
```

### 2. Large Instance Types
```
❌ BAD: 2 vCPU, 4 GB memory
✅ GOOD: 1 vCPU, 2 GB memory (cheapest)
```

### 3. Unused Elastic IPs
```
❌ BAD: Allocating Elastic IP but not using it
✅ GOOD: Use auto-assigned public IP
```

### 4. Not Deleting Old Resources
```
❌ BAD: Keeping unused ECR images
✅ GOOD: Use lifecycle policy (included in our template)
```

### 5. Redis Managed Service
```
❌ BAD: Amazon ElastiCache ($15+/month)
✅ GOOD: Upstash Redis Free Tier OR disable Redis
```

---

## 🛡️ Protect Yourself from Surprise Bills

### Step 1: Set Billing Alerts

```powershell
# Create billing alert for $5
aws cloudwatch put-metric-alarm ^
  --alarm-name "AWS-Billing-Alert-5USD" ^
  --metric-name EstimatedCharges ^
  --namespace AWS/Billing ^
  --statistic Maximum ^
  --period 21600 ^
  --threshold 5 ^
  --comparison-operator GreaterThanThreshold ^
  --evaluation-periods 1 ^
  --alarm-actions "arn:aws:sns:us-east-1:ACCOUNT:billing-alerts" ^
  --region us-east-1
```

### Step 2: Enable AWS Budgets

1. Go to: https://console.aws.amazon.com/billing
2. Click "Create budget"
3. Set budget type: **Cost budget**
4. Set amount: **$5**
5. Set alert threshold: **80%** ($4)
6. Add email notification

### Step 3: Monitor Usage

```powershell
# Check current month's spending
aws ce get-cost-and-usage ^
  --time-period Start=2024-01-01,End=2024-01-31 ^
  --granularity MONTHLY ^
  --metrics "UnblendedCost"
```

---

## 🔧 Resource Cleanup Scripts

### Delete Everything (Start Fresh)

```powershell
# Delete App Runner service
aws apprunner delete-service --service-arn YOUR_SERVICE_ARN --region us-east-1

# Delete ECR repository and all images
aws ecr delete-repository --repository-name marketing-agent --force --region us-east-1

# Delete CloudFormation stack
aws cloudformation delete-stack --stack-name marketing-agent --region us-east-1

# Delete CloudWatch log group
aws logs delete-log-group --log-group-name /aws/apprunner/marketing-agent --region us-east-1
```

### Keep Only Last 3 ECR Images

```powershell
# List all images
aws ecr list-images --repository-name marketing-agent --region us-east-1

# Delete old images (keep latest 3)
aws ecr batch-delete-image ^
  --repository-name marketing-agent ^
  --image-ids imageTag=old-tag-1 imageTag=old-tag-2 ^
  --region us-east-1
```

---

## 📈 Monitoring Your Free Tier Usage

### Check App Runner Usage

```powershell
# Get service metrics
aws apprunner list-operations --service-arn YOUR_ARN --region us-east-1

# Check service status
aws apprunner describe-service --service-arn YOUR_ARN --region us-east-1
```

### Check ECR Storage

```powershell
# Check repository size
aws ecr describe-repositories --repository-names marketing-agent --region us-east-1
```

### Check CloudWatch Logs

```powershell
# Check log group size
aws logs describe-log-groups --log-group-name-prefix /aws/apprunner --region us-east-1
```

---

## 🎓 Free Tier Best Practices

### ✅ DO:
1. Use **App Runner** (easiest and cheapest)
2. Use **Upstash Redis** (free tier: 10K commands/day)
3. Set **billing alerts** immediately
4. Monitor **Cost Explorer** weekly
5. Use **lifecycle policies** for ECR
6. Keep **only 1 service** running
7. Use **smallest instance size**
8. Delete **unused resources**

### ❌ DON'T:
1. Don't use **ElastiCache** (not free tier)
2. Don't run **multiple environments** (staging + prod)
3. Don't enable **auto-scaling** (can exceed free tier)
4. Don't store **large files** in ECR
5. Don't forget to **delete test resources**
6. Don't use **load balancers** ($18+/month)
7. Don't enable **RDS** ($15+/month)
8. Don't ignore **billing emails**

---

## 🆘 Emergency: Stop All Charges

If you see unexpected charges:

```powershell
# 1. Delete App Runner service immediately
aws apprunner delete-service --service-arn YOUR_ARN --region us-east-1

# 2. Delete ECR repository
aws ecr delete-repository --repository-name marketing-agent --force --region us-east-1

# 3. Verify no other resources running
aws apprunner list-services --region us-east-1
aws ecs list-clusters --region us-east-1
aws ec2 describe-instances --region us-east-1

# 4. Contact AWS Support for billing adjustment
# https://console.aws.amazon.com/support
```

---

## 📚 Free Tier Monitoring Commands

```powershell
# Check current month's spending
aws ce get-cost-and-usage ^
  --time-period Start=$(Get-Date -Format yyyy-MM-01),End=$(Get-Date -Format yyyy-MM-dd) ^
  --granularity MONTHLY ^
  --metrics "UnblendedCost" ^
  --region us-east-1

# List all App Runner services
aws apprunner list-services --region us-east-1

# List all ECR repositories
aws ecr describe-repositories --region us-east-1

# Check CloudWatch log size
aws logs describe-log-groups --region us-east-1
```

---

## 💡 Pro Tips

1. **Use AWS Organizations** to separate billing
2. **Tag all resources** for better cost tracking
3. **Set up AWS Cost Anomaly Detection** (free)
4. **Review bills monthly** in Billing Console
5. **Use Spot Instances** if using EC2 (70% cheaper)
6. **Compress logs** before storing
7. **Use S3 lifecycle policies** if storing data
8. **Delete old CloudFormation stacks**

---

## 🎯 Summary: Your Free Tier Setup

| Component | Service | Cost |
|-----------|---------|------|
| **Compute** | App Runner (1 vCPU, 2GB) | $0 (free tier) |
| **Container Registry** | ECR (0.4 GB) | $0 (free tier) |
| **Cache** | Upstash Redis | $0 (free tier) |
| **Logging** | CloudWatch (0.1 GB) | $0 (free tier) |
| **Monitoring** | CloudWatch Alarms | $0 (free tier) |
| **TOTAL** | | **$0/month** ✅ |

---

**Remember**: Free tier is valid for **12 months** after account creation!
