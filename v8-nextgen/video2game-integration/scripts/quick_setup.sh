#!/bin/bash
# Quick setup script for video2game integration
# Run this after cloning video2game repository

set -e

echo "============================================"
echo "Video2Game Integration - Quick Setup"
echo "============================================"
echo ""

# Check if video2game repo exists
if [ ! -d "video2game" ]; then
    echo "Cloning video2game repository..."
    git clone https://github.com/video2game/video2game.git
else
    echo "✓ video2game repository already exists"
fi

# Check if conda is available
if command -v conda &> /dev/null; then
    echo ""
    echo "Found conda. Creating environment..."

    # Check if environment exists
    if conda env list | grep -q "video2game"; then
        echo "✓ video2game environment already exists"
    else
        echo "Creating new conda environment..."
        conda create -n video2game python=3.7 -y
    fi

    echo ""
    echo "To activate the environment:"
    echo "  conda activate video2game"

elif command -v pyenv &> /dev/null; then
    echo ""
    echo "Found pyenv. Setting up environment..."

    # Check if Python 3.7 is installed
    if pyenv versions | grep -q "3.7"; then
        echo "✓ Python 3.7 found in pyenv"
    else
        echo "Installing Python 3.7..."
        pyenv install 3.7.16
    fi

    # Create virtualenv
    if pyenv virtualenvs | grep -q "video2game"; then
        echo "✓ video2game virtualenv already exists"
    else
        echo "Creating virtualenv..."
        pyenv virtualenv 3.7.16 video2game
    fi

    echo ""
    echo "To activate the environment:"
    echo "  pyenv activate video2game"

else
    echo ""
    echo "WARNING: Neither conda nor pyenv found."
    echo "Please install one of them to create a Python 3.7 environment."
    echo ""
    echo "Install options:"
    echo "  - Conda: https://docs.conda.io/en/latest/miniconda.html"
    echo "  - Pyenv: https://github.com/pyenv/pyenv"
fi

echo ""
echo "============================================"
echo "Next Steps:"
echo "============================================"
echo "1. Activate the environment (see above)"
echo "2. Follow docs/INSTALLATION.md to install dependencies"
echo "3. Place your walkthrough video in input/"
echo "4. Run: python process_walkthrough.py --video ../input/video.mp4"
echo ""
echo "For detailed instructions, see:"
echo "  - docs/INSTALLATION.md"
echo "  - docs/PIPELINE_GUIDE.md"
echo "  - docs/INTEGRATION_GUIDE.md"
echo ""
