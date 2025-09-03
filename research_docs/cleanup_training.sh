#!/bin/bash
# Cleanup script for completed Cyberwheel training

echo "🧹 Cyberwheel Training Cleanup"
echo "=============================="

# Create archive directory
mkdir -p /rds/general/user/moa324/home/projects/archive/logs_$(date +%Y%m%d)

# Archive completed logs
if [ -d "/rds/general/user/moa324/home/projects/logs" ]; then
    mv /rds/general/user/moa324/home/projects/logs/*.out /rds/general/user/moa324/home/projects/archive/logs_$(date +%Y%m%d)/ 2>/dev/null
    mv /rds/general/user/moa324/home/projects/logs/*.err /rds/general/user/moa324/home/projects/archive/logs_$(date +%Y%m%d)/ 2>/dev/null
fi

# Compress old model files
cd /rds/general/user/moa324/home/projects/cyberwheel/cyberwheel/data
if [ -d "models" ]; then
    tar -czf models_backup_$(date +%Y%m%d).tar.gz models/
fi
if [ -d "runs" ]; then
    tar -czf runs_backup_$(date +%Y%m%d).tar.gz runs/
fi

echo "✅ Cleanup completed"
echo "📦 Backups created with timestamp $(date +%Y%m%d)"
