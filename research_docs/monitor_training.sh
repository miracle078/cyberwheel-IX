#!/bin/bash
# Job monitoring and status script

echo "🔍 Cyberwheel HPC Training Status"
echo "======================================"

# Check current job status
echo "📊 Current Job Status:"
qstat -u moa324

echo ""
echo "💾 Disk Usage:"
df -h /rds/general/user/moa324/home/projects

echo ""
echo "📁 Recent Training Results:"
if [ -d "/rds/general/user/moa324/home/projects/cyberwheel/cyberwheel/data/runs/" ]; then
    ls -la /rds/general/user/moa324/home/projects/cyberwheel/cyberwheel/data/runs/ | tail -10
else
    echo "No training results directory found yet"
fi

echo ""
echo "📈 Latest Log Entries:"
if [ -d "/rds/general/user/moa324/home/projects/logs" ]; then
    find /rds/general/user/moa324/home/projects/logs -name "*.out" -type f -exec tail -3 {} + 2>/dev/null | tail -20
else
    echo "No logs directory found yet"
fi

echo ""
echo "🎯 Resource Usage Summary:"
echo "Jobs Running: $(qstat -u moa324 2>/dev/null | grep " R " | wc -l)"
echo "Jobs Queued: $(qstat -u moa324 2>/dev/null | grep " Q " | wc -l)"
if [ -d "/rds/general/user/moa324/home/projects/cyberwheel/cyberwheel/data/models" ]; then
    echo "Completed Models: $(ls /rds/general/user/moa324/home/projects/cyberwheel/cyberwheel/data/models/*.zip 2>/dev/null | wc -l)"
else
    echo "Completed Models: 0 (models directory not found)"
fi
