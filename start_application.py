#!/usr/bin/env python3
"""
TikTub Studio Application Launcher
Menjalankan backend dan frontend secara bersamaan
"""

import os
import sys
import time
import signal
import subprocess
import threading
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('tiktub_studio.log')
    ]
)
logger = logging.getLogger(__name__)

class TikTubStudioLauncher:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.running = True
        
    def start_backend(self):
        """Start Python backend server"""
        try:
            logger.info("Starting Python backend server...")
            
            # Check if backend dependencies are available
            self.check_backend_dependencies()
            
            # Start backend process
            self.backend_process = subprocess.Popen(
                [sys.executable, "run_backend.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for backend to be ready
            self.wait_for_backend()
            logger.info("✅ Backend server started successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to start backend: {e}")
            self.stop_application()
    
    def start_frontend(self):
        """Start Java frontend application"""
        try:
            logger.info("Starting Java frontend application...")
            
            # Check if frontend dependencies are available
            self.check_frontend_dependencies()
            
            # Change to frontend directory
            frontend_dir = Path("java_frontend")
            if not frontend_dir.exists():
                raise FileNotFoundError("Frontend directory not found")
            
            # Start frontend process
            self.frontend_process = subprocess.Popen(
                ["mvn", "exec:java", "-Dexec.mainClass=com.tiktubstudio.TikTubStudioApp"],
                cwd=frontend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            logger.info("✅ Frontend application started successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to start frontend: {e}")
            self.stop_application()
    
    def check_backend_dependencies(self):
        """Check if backend dependencies are installed"""
        try:
            import flask
            import torch
            import whisper
            import cv2
            import moviepy
            logger.info("✅ Backend dependencies verified")
        except ImportError as e:
            logger.error(f"❌ Missing backend dependency: {e}")
            logger.info("Installing backend dependencies...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    def check_frontend_dependencies(self):
        """Check if frontend dependencies are available"""
        # Check Java
        try:
            result = subprocess.run(["java", "-version"], capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception("Java not found")
            logger.info("✅ Java runtime verified")
        except Exception:
            raise Exception("Java 11+ is required but not found")
        
        # Check Maven
        try:
            result = subprocess.run(["mvn", "-version"], capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception("Maven not found")
            logger.info("✅ Maven build tool verified")
        except Exception:
            raise Exception("Apache Maven is required but not found")
    
    def wait_for_backend(self):
        """Wait for backend server to be ready"""
        import requests
        
        max_attempts = 30
        for attempt in range(max_attempts):
            try:
                response = requests.get("http://localhost:5000/api/health", timeout=1)
                if response.status_code == 200:
                    return True
            except:
                pass
            
            time.sleep(1)
            logger.info(f"Waiting for backend... ({attempt + 1}/{max_attempts})")
        
        raise Exception("Backend server failed to start within 30 seconds")
    
    def monitor_processes(self):
        """Monitor backend and frontend processes"""
        while self.running:
            try:
                # Check backend process
                if self.backend_process and self.backend_process.poll() is not None:
                    logger.error("❌ Backend process stopped unexpectedly")
                    self.stop_application()
                    break
                
                # Check frontend process
                if self.frontend_process and self.frontend_process.poll() is not None:
                    logger.info("Frontend application closed")
                    self.stop_application()
                    break
                
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Error monitoring processes: {e}")
                break
    
    def stop_application(self):
        """Stop both backend and frontend"""
        logger.info("Stopping TikTub Studio...")
        self.running = False
        
        # Stop frontend
        if self.frontend_process and self.frontend_process.poll() is None:
            logger.info("Stopping frontend...")
            self.frontend_process.terminate()
            try:
                self.frontend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.frontend_process.kill()
        
        # Stop backend
        if self.backend_process and self.backend_process.poll() is None:
            logger.info("Stopping backend...")
            self.backend_process.terminate()
            try:
                self.backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.backend_process.kill()
        
        logger.info("✅ TikTub Studio stopped")
    
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C signal"""
        logger.info("Received interrupt signal")
        self.stop_application()
        sys.exit(0)
    
    def run(self):
        """Main run method"""
        try:
            # Setup signal handler
            signal.signal(signal.SIGINT, self.signal_handler)
            
            logger.info("🎬 Starting TikTub Studio...")
            logger.info("=" * 50)
            
            # Start backend in thread
            backend_thread = threading.Thread(target=self.start_backend)
            backend_thread.daemon = True
            backend_thread.start()
            
            # Wait a moment for backend to start
            time.sleep(3)
            
            # Start frontend in thread
            frontend_thread = threading.Thread(target=self.start_frontend)
            frontend_thread.daemon = True
            frontend_thread.start()
            
            # Monitor processes
            self.monitor_processes()
            
        except KeyboardInterrupt:
            logger.info("Application interrupted by user")
        except Exception as e:
            logger.error(f"Application error: {e}")
        finally:
            self.stop_application()

def main():
    """Main function"""
    print("🎬 TikTub Studio Launcher")
    print("=" * 30)
    print("AI-Powered Short Video Creator")
    print()
    
    # Check system requirements
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)
    
    # Create and run launcher
    launcher = TikTubStudioLauncher()
    launcher.run()

if __name__ == "__main__":
    main()