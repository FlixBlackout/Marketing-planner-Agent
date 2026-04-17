# Docker Installation Guide for Windows

## Quick Overview

This guide will help you install Docker Desktop on Windows so you can run the Marketing Planning Assistant with Docker.

---

## Method 1: Install Docker Desktop (Recommended)

### Step 1: Check System Requirements

- **Windows 10/11**: 64-bit Pro, Enterprise, or Education
- **RAM**: Minimum 4GB (8GB recommended)
- **Virtualization**: Must be enabled in BIOS
- **WSL 2**: Windows Subsystem for Linux 2

### Step 2: Enable WSL 2

Open **PowerShell as Administrator** and run:

```powershell
# Enable WSL
wsl --install

# If already installed, update to WSL 2
wsl --set-default-version 2
```

Restart your computer when prompted.

### Step 3: Download Docker Desktop

1. Visit: **https://www.docker.com/products/docker-desktop/**
2. Click **"Download for Windows"**
3. Save the installer file (Docker Desktop Installer.exe)

### Step 4: Install Docker Desktop

1. Double-click `Docker Desktop Installer.exe`
2. Follow these settings:
   - ✅ **Use WSL 2 instead of Hyper-V** (recommended)
   - ✅ Add shortcut to desktop (optional)
3. Click **"OK"** to start installation
4. Wait for installation to complete (5-10 minutes)
5. Click **"Close and restart"**

### Step 5: Start Docker Desktop

1. Open **Docker Desktop** from Start Menu
2. Accept the **Service Agreement**
3. Optionally skip the survey
4. Wait for Docker to start (you'll see the whale icon in system tray)
5. Status should show: **"Docker Desktop is running"**

### Step 6: Verify Installation

Open **PowerShell** or **Command Prompt** and run:

```powershell
# Check Docker version
docker --version

# Check Docker Compose version
docker-compose --version

# Test Docker
docker run hello-world
```

You should see:
```
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

---

## Method 2: Use Without Docker (Alternative)

If you can't install Docker, you can run the project directly with Python:

### Quick Start (No Docker)

1. **Double-click**: `run-without-docker.bat`
   
   This will:
   - ✅ Create virtual environment
   - ✅ Install dependencies
   - ✅ Start the application

2. **Or run manually**:
   ```powershell
   cd "c:\Planner Agent\marketing_agent"
   
   # Create virtual environment
   python -m venv venv
   
   # Activate
   venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run the application
   python api.py
   ```

3. **Access the application**:
   - API: http://localhost:8000
   - Health: http://localhost:8000/health

---

## Running the Project with Docker

Once Docker is installed, follow these steps:

### Option 1: Interactive Quick Start

```powershell
# Navigate to project
cd "c:\Planner Agent\marketing_agent"

# Run the quick start script
.\quick-start.sh
# Or in PowerShell:
bash quick-start.sh
```

### Option 2: Docker Compose (Recommended)

```powershell
# Navigate to project
cd "c:\Planner Agent\marketing_agent"

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

### Option 3: Build and Run Manually

```powershell
# Build Docker image
docker build -t marketing-agent:latest .

# Run container
docker run -d `
  --name marketing-agent `
  -p 8000:8000 `
  --env-file .env `
  marketing-agent:latest

# View logs
docker logs -f marketing-agent

# Stop container
docker stop marketing-agent
docker rm marketing-agent
```

---

## Troubleshooting Docker Installation

### Issue: WSL 2 not enabled

**Solution**:
```powershell
# Run as Administrator
wsl --install
wsl --set-default-version 2
```
Restart computer.

### Issue: Virtualization not enabled

**Solution**:
1. Restart computer and enter BIOS/UEFI
2. Look for **Virtualization Technology** or **Intel VT-x/AMD-V**
3. Enable it
4. Save and exit BIOS

### Issue: Docker Desktop won't start

**Solution**:
```powershell
# Reset Docker to defaults
# Click Docker tray icon → Settings → Reset → Reset to factory defaults

# Or reinstall Docker Desktop
```

### Issue: Port already in use

**Solution**:
```powershell
# Check what's using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or use a different port in docker-compose.yml
```

---

## Docker Commands Cheat Sheet

### Basic Commands

```powershell
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Rebuild and start
docker-compose up -d --build

# View running containers
docker ps

# View all containers
docker ps -a

# Remove unused images
docker image prune -a

# Check disk usage
docker system df
```

### Development Commands

```powershell
# Execute command in running container
docker-compose exec api bash

# View container details
docker inspect marketing-agent-api

# Copy files from container
docker cp marketing-agent-api:/app/logs ./logs

# Scale services
docker-compose up -d --scale api=3
```

---

## Next Steps After Docker Installation

1. **Verify Docker is running**:
   ```powershell
   docker ps
   ```

2. **Start the project**:
   ```powershell
   cd "c:\Planner Agent\marketing_agent"
   docker-compose up -d
   ```

3. **Access the application**:
   - Open browser: http://localhost:8000
   - Test API: http://localhost:8000/health

4. **View logs**:
   ```powershell
   docker-compose logs -f api
   ```

---

## Team Collaboration with Docker

### Share Your Setup

Once Docker is working, share this with your team:

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd marketing_agent
   ```

2. **Set up environment**:
   ```bash
   cp .env.example .env
   # Edit .env with API keys
   ```

3. **Start with one command**:
   ```bash
   docker-compose up -d
   ```

Everyone will have the **exact same environment**! 🎉

---

## Need Help?

- **Docker Docs**: https://docs.docker.com/desktop/windows/
- **Docker Compose**: https://docs.docker.com/compose/
- **Project Guide**: See DOCKER_GUIDE.md in this directory

---

**Pro Tip**: Docker ensures your application runs identically on all team members' machines and in production! 🚀
