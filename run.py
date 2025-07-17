#!/usr/bin/env python3
"""
TikTube Studio - Startup Script
Transform your long videos into engaging shorts with AI
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")

def check_ffmpeg():
    """Check if FFmpeg is installed"""
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      capture_output=True, check=True)
        print("✅ FFmpeg is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ FFmpeg not found")
        print_ffmpeg_install_instructions()
        return False

def print_ffmpeg_install_instructions():
    """Print platform-specific FFmpeg installation instructions"""
    system = platform.system().lower()
    
    print("\n📦 FFmpeg Installation Instructions:")
    if system == "linux":
        print("   Ubuntu/Debian: sudo apt update && sudo apt install ffmpeg")
        print("   CentOS/RHEL:   sudo yum install ffmpeg")
        print("   Arch Linux:    sudo pacman -S ffmpeg")
    elif system == "darwin":  # macOS
        print("   macOS: brew install ffmpeg")
        print("   (Install Homebrew first: https://brew.sh/)")
    elif system == "windows":
        print("   Windows: Download from https://ffmpeg.org/download.html")
        print("   Or use Chocolatey: choco install ffmpeg")
    
    print("\nPlease install FFmpeg and run this script again.")

def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing Python dependencies...")
    
    try:
        # Upgrade pip first
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'],
                      check=True)
        
        # Install requirements
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
                      check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    dirs = ['uploads', 'outputs', 'temp']
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
    print("✅ Created necessary directories")

def check_disk_space():
    """Check available disk space"""
    try:
        import shutil
        total, used, free = shutil.disk_usage('.')
        free_gb = free // (1024**3)
        
        if free_gb < 2:
            print(f"⚠️  Warning: Low disk space ({free_gb}GB available)")
            print("   Recommended: At least 2GB free space")
        else:
            print(f"✅ Disk space: {free_gb}GB available")
    except Exception:
        print("⚠️  Could not check disk space")

def start_application():
    """Start the TikTube Studio application"""
    print("\n🚀 Starting TikTube Studio...")
    print("   URL: http://localhost:5000")
    print("   Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n\n👋 TikTube Studio stopped. Thank you for using our app!")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")

def main():
    """Main startup routine"""
    print("🎬 TikTube Studio - Startup")
    print("=" * 50)
    
    # Check system requirements
    check_python_version()
    
    if not check_ffmpeg():
        sys.exit(1)
    
    check_disk_space()
    
    # Setup application
    create_directories()
    
    # Check if requirements.txt exists
    if not Path('requirements.txt').exists():
        print("❌ requirements.txt not found")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    print("\n✅ All checks passed!")
    print("🎯 TikTube Studio is ready to launch")
    
    # Start the application
    start_application()

if __name__ == "__main__":
    main()