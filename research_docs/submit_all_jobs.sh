#!/bin/bash
# Master submission script for all Cyberwheel training phases
# Execute from: /rds/general/user/moa324/home/projects/

echo "🚀 Starting Cyberwheel HPC Training Pipeline"
echo "📅 Started at: $(date)"

# Phase 1: System Validation (run first, wait for completion)
echo "📋 Phase 1: System Validation"
if [ -f "Phase1_Validation.pbs" ]; then
    qsub Phase1_Validation.pbs
    echo "Waiting for Phase 1 completion..."
    sleep 300  # Wait 5 minutes for validation
fi

# Phase 2: Blue Agent Training (can run in parallel)
echo "🔵 Phase 2: Blue Agent Training"
for job in Phase2_Blue_*.pbs; do
    if [ -f "$job" ]; then
        qsub "$job"
        echo "Submitted: $job"
    fi
done

# Phase 3: Red Agent Training (can run in parallel with Phase 2)
echo "🔴 Phase 3: Red Agent Training"
for job in Phase3_Red_*.pbs; do
    if [ -f "$job" ]; then
        qsub "$job"
        echo "Submitted: $job"
        sleep 30  # Stagger submissions
    fi
done

# Phase 5: SULI Training (requires more resources)
echo "🔄 Phase 5: SULI Co-Evolution"
for job in Phase5_SULI_*.pbs; do
    if [ -f "$job" ]; then
        qsub "$job"
        echo "Submitted: $job"
        sleep 60  # Stagger resource-intensive jobs
    fi
done

# Phase 6: Scalability Testing (GPU required)
echo "📈 Phase 6: Scalability Testing"
for job in Phase6_Scale_*.pbs; do
    if [ -f "$job" ]; then
        qsub "$job"
        echo "Submitted: $job"
        sleep 120  # Stagger GPU jobs
    fi
done

# Start monitoring services
echo "📊 Starting Monitoring Services"
if [ -f "launch_tensorboard.pbs" ]; then
    qsub launch_tensorboard.pbs
fi
if [ -f "launch_visualizer.pbs" ]; then
    qsub launch_visualizer.pbs
fi

echo "✅ All jobs submitted successfully"
echo "📊 Monitor progress with: qstat -u moa324"
echo "📈 Access TensorBoard on port 6006"
echo "🎯 Access Cyberwheel dashboard on port 8050"
