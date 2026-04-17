@echo off
REM =============================================================================
REM Kubernetes Cleanup Script
REM =============================================================================

echo.
echo ========================================================================
echo   Kubernetes Cleanup - Marketing Planning Assistant
echo ========================================================================
echo.

echo This will remove all Kubernetes resources for the marketing agent.
echo.
set /p CONFIRM="Are you sure? (y/n): "

if /i not "%CONFIRM%"=="y" (
    echo Cleanup cancelled.
    pause
    exit /b 0
)

echo.
echo [1/3] Deleting namespace (this removes all resources)...
kubectl delete namespace marketing-agent

if %errorlevel% neq 0 (
    echo [WARNING] Namespace may not exist or already deleted
) else (
    echo [OK] Namespace deleted!
)

echo.
echo [2/3] Removing Docker image...
docker rmi marketing-agent:k8s 2>nul
if %errorlevel% neq 0 (
    echo [INFO] Docker image may not exist
) else (
    echo [OK] Docker image removed!
)

echo.
echo [3/3] Cleanup complete!
echo.

echo ========================================================================
echo   To re-deploy, run: setup-k8s.bat
echo ========================================================================
echo.

pause
