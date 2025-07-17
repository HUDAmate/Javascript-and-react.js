#!/usr/bin/env python3
"""
Script untuk menjalankan TikTub Studio Backend Server
"""

import os
import sys
import logging
import subprocess
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_python_version():
    """Check Python version compatibility"""
    if sys.version_info < (3, 8):
        logger.error("Python 3.8 or higher is required")
        sys.exit(1)
    logger.info(f"Python version: {sys.version}")

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import torch
        import whisper
        import cv2
        import moviepy
        logger.info("All required dependencies are available")
        return True
    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        logger.info("Installing dependencies...")
        return install_dependencies()

def install_dependencies():
    """Install required dependencies"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        logger.info("Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install dependencies: {e}")
        return False

def check_ffmpeg():
    """Check if FFmpeg is available"""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        logger.info("FFmpeg is available")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.warning("FFmpeg not found. Please install FFmpeg for video processing")
        return False

def setup_environment():
    """Setup environment variables and directories"""
    # Create necessary directories
    os.makedirs("temp", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Set environment variables
    os.environ.setdefault("FLASK_ENV", "production")
    os.environ.setdefault("PYTHONPATH", str(Path(__file__).parent))
    
    logger.info("Environment setup completed")

def main():
    """Main function to start the backend server"""
    logger.info("Starting TikTub Studio Backend Server...")
    
    # Check system requirements
    check_python_version()
    
    if not check_dependencies():
        logger.error("Failed to install dependencies. Exiting...")
        sys.exit(1)
    
    check_ffmpeg()
    setup_environment()
    
    try:
        # Import and start Flask server
        from python_backend.api.flask_server import app
        
        logger.info("Backend server starting on http://localhost:5000")
        logger.info("Press Ctrl+C to stop the server")
        
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            threaded=True
        )
        
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()