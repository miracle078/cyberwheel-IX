# Cyberwheel Research Documentation

This folder contains comprehensive documentation, analysis, and experimental materials for the Cyberwheel cybersecurity reinforcement learning research project.

## Repository Structure

### 🎓 Foundational Learning Package ⭐ **START HERE** ⭐
- `FOUNDATIONAL_LEARNING_PACKAGE_README.md` - **MAIN ENTRY POINT** - Complete learning guide overview
- `cyberwheel_foundational_explanation.tex` - Step-by-step explanation of ALL research concepts from basics
- `LEARNING_PREREQUISITES_GUIDE.md` - 12 prerequisite areas with best learning resources & time estimates

### 📊 Technical Analysis Documents
- `cyberwheel_technical_analysis_index.md` - Master index for the complete technical analysis
- `cyberwheel_technical_analysis_part1.md` - Foundation and problem formulation analysis
- `cyberwheel_technical_analysis_part2.md` - Environmental and algorithmic framework analysis
- `cyberwheel_technical_analysis_part3.md` - Evaluation and experimental methodology analysis
- `cyberwheel_technical_analysis_part4.md` - Mathematical foundations and future directions
- `cyberwheel_technical_analysis.md` - (Empty) Main technical analysis file

### 📑 Comprehensive Report
- `cyberwheel_comprehensive_report.tex` - Main LaTeX source file
- `cyberwheel_comprehensive_report.pdf` - Final compiled PDF report (449KB)
- `cyberwheel_comprehensive_report copy.tex` - Backup/alternative version
- `cyberwheel_comprehensive_report copy.pdf` - Backup PDF (300KB)
- `cyberwheel_comprehensive_report.aux/.bbl/.blg/.log/.out/.toc` - LaTeX compilation files

### 📚 Explanatory Documentation
- `cyberwheel_simple_explanation.md` - Simplified explanation for broader audience
- `cyberwheel_explanation_part1.md` - Detailed explanation (Part 1)

### 📖 Training Guides and Notebooks
- `Cyberwheel_HPC_Training_Guide.ipynb` - Original HPC training guide
- `Cyberwheel_HPC_Training_Guide_Updated.ipynb` - Updated training guide (147KB)

### 🎯 Experimental Configuration Files

#### Phase 2: Blue Agent Training
- `Phase2_Blue_Small.pbs` - Small defensive configuration
- `Phase2_Blue_Medium.pbs` - Medium defensive configuration  
- `Phase2_Blue_HighDecoy.pbs` - High deception strategy
- `Phase2_Blue_PerfectDetection.pbs` - Perfect detection baseline

#### Phase 3: Red Agent Training
- `Phase3_Red_RL.pbs` - Reinforcement learning attacker
- `Phase3_Red_ART.pbs` - Adversarial robustness testing
- `Phase3_Red_Campaign.pbs` - Campaign-style attacks
- `Phase3_Red_Servers.pbs` - Server-focused attacks

#### Phase 4: Cross-Evaluation Matrix
- `Phase4_Cross_Phase2_Blue_HighDecoy_vs_artagent.pbs`
- `Phase4_Cross_Phase2_Blue_HighDecoy_vs_rlredagent.pbs`
- `Phase4_Cross_Phase2_Blue_Medium_vs_artagent.pbs`
- `Phase4_Cross_Phase2_Blue_Medium_vs_rlredagent.pbs`
- `Phase4_Cross_Phase2_Blue_PerfectDetection_vs_artagent.pbs`
- `Phase4_Cross_Phase2_Blue_PerfectDetection_vs_rlredagent.pbs`

#### Phase 5: SULI Co-Evolution
- `Phase5_SULI_Baseline.pbs` - Standard SULI configuration
- `Phase5_SULI_Large.pbs` - Large-scale SULI experiment
- `Phase5_SULI_Medium.pbs` - Medium-scale SULI experiment
- `Phase5_SULI_Small.pbs` - Small-scale SULI experiment

#### Phase 6: Scalability Testing
- `Phase6_Scale_1K.pbs` - 1,000 host scalability test
- `Phase6_Scale_5K.pbs` - 5,000 host scalability test
- `Phase6_Scale_10K.pbs` - 10,000 host scalability test

### 🔧 Management Scripts
- `submit_all_jobs.sh` - Batch job submission script
- `monitor_training.sh` - Training progress monitoring
- `cleanup_training.sh` - Training cleanup utilities

### 📋 Project Management
- `STREAMLINED_WORKFLOW.md` - Optimized research workflow documentation
- `SUPERVISOR_MEETING_SUMMARY.md` - Meeting notes and decisions
- `THESIS_SUPERVISION_GUIDE.md` - Comprehensive supervision guidelines

### 📖 References and Styling
- `cyberwheel_refs.bib` - Bibliography database
- `cyberwheel_refs_new.bib` - Updated bibliography
- `commands.sty` - Custom LaTeX styling commands

## Research Overview

This research focuses on **Adversarial Reinforcement Learning for Cyber Defense** using the Cyberwheel framework. Key contributions include:

### 🎯 Core Innovations
1. **SULI Training Methodology** - Self-play with Uniform Learning Initialization
2. **Comprehensive Agent Evaluation** - 8×5 matrix of defensive vs. offensive strategies
3. **Enterprise-Scale Validation** - Networks up to 10,000 hosts
4. **Seven-Phase Experimental Framework** - Progressive complexity validation

### 📊 Key Results
- **90% reduction** in training instabilities using SULI
- **40 unique combinations** of agent strategies evaluated
- **Statistical significance** validated across multiple experimental seeds
- **Real-world applicability** demonstrated through HPC deployment

## File Organization Logic

### By Document Type
- **Analysis**: Technical deep-dives with mathematical rigor
- **Reports**: Comprehensive formal documentation
- **Guides**: Practical implementation instructions
- **Configurations**: Experimental setup files
- **Management**: Project workflow and supervision

### By Research Phase
1. **Foundation** (Parts 1-2): Problem formulation and framework
2. **Methodology** (Parts 3-4): Experimental design and theory
3. **Validation** (Phases 1-3): Agent training and testing
4. **Evaluation** (Phases 4-6): Cross-validation and scaling
5. **Documentation** (Reports/Guides): Knowledge transfer

## Usage Instructions

## Quick Start Guide

### 🚀 **New to This Research? START HERE!**
1. **Read:** `FOUNDATIONAL_LEARNING_PACKAGE_README.md` - Complete overview of the learning package
2. **Assess:** `LEARNING_PREREQUISITES_GUIDE.md` - Identify which prerequisite topics you need to learn
3. **Learn:** Follow the recommended learning path (4-18 months depending on background)
4. **Understand:** Read `cyberwheel_foundational_explanation.tex` - Step-by-step research explanation
5. **Deep Dive:** Progress to technical analysis parts 1-4 for complete mathematical details

### 📖 For Technical Analysis
1. Start with `cyberwheel_technical_analysis_index.md` for overview
2. Read parts 1-4 sequentially for complete understanding
3. Reference comprehensive report PDF for formal presentation

### For Experimental Reproduction
1. Review `STREAMLINED_WORKFLOW.md` for process overview
2. Use training guides for environment setup
3. Execute PBS files in phase order (2→3→4→5→6)
4. Monitor with provided scripts

### For Academic Reference
- **Citations**: Use bibliography files
- **Figures**: Extract from comprehensive report PDF
- **Methodology**: Reference technical analysis parts 2-3

## Data Storage Information

- **Total Size**: ~1.8GB compressed documentation
- **Key Files**: 
  - Technical analysis: ~70KB total
  - Comprehensive report PDF: 449KB
  - Training guides: 270KB total
  - PBS configurations: ~15KB total

Last Updated: August 12, 2025
Repository: cyberwheel-IX (imperial-hpc branch)
