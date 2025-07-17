#!/usr/bin/env python3
"""
Demo script untuk testing TikTub Studio backend
Menjalankan semua fitur utama tanpa frontend GUI
"""

import requests
import json
import time
import sys
import os
from pathlib import Path

# Configuration
BACKEND_URL = "http://localhost:5000"
DEMO_VIDEO_URL = "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4"  # Sample video

def print_banner():
    """Print banner aplikasi"""
    print("🎬" + "="*60 + "🎬")
    print("     TikTub Studio Backend Demo")
    print("     AI-Powered Short Video Creator")
    print("🎬" + "="*60 + "🎬")
    print()

def check_backend_health():
    """Check apakah backend server running"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend server is healthy")
            print(f"   Service: {data.get('service', 'Unknown')}")
            print(f"   Timestamp: {data.get('timestamp', 'Unknown')}")
            return True
        else:
            print(f"❌ Backend server returned status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to backend server: {e}")
        print(f"   Make sure backend is running on {BACKEND_URL}")
        return False

def download_demo_video():
    """Download demo video untuk testing"""
    demo_video_path = "demo_video.mp4"
    
    if os.path.exists(demo_video_path):
        print(f"✅ Demo video already exists: {demo_video_path}")
        return demo_video_path
    
    print("📥 Downloading demo video...")
    try:
        response = requests.get(DEMO_VIDEO_URL, stream=True)
        response.raise_for_status()
        
        with open(demo_video_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✅ Demo video downloaded: {demo_video_path}")
        return demo_video_path
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to download demo video: {e}")
        print("💡 You can use your own video file instead")
        return None

def upload_video(video_path):
    """Upload video ke backend"""
    if not os.path.exists(video_path):
        print(f"❌ Video file not found: {video_path}")
        return None
    
    print(f"📤 Uploading video: {video_path}")
    
    try:
        with open(video_path, 'rb') as f:
            files = {'video': f}
            response = requests.post(f"{BACKEND_URL}/api/upload", files=files)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Video uploaded successfully")
            print(f"   File ID: {data.get('file_id')}")
            print(f"   File size: {data.get('file_size')} bytes")
            return data
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Upload error: {e}")
        return None

def start_processing(file_path):
    """Start video processing"""
    print(f"🚀 Starting video processing...")
    
    config = {
        'platform': 'tiktok',
        'max_segments': 3,
        'segment_duration': 60,
        'auto_effects': True,
        'theme': 'auto',
        'language': 'auto'
    }
    
    payload = {
        'file_path': file_path,
        'config': config
    }
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/process",
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Processing started")
            print(f"   Job ID: {data.get('job_id')}")
            print(f"   Estimated time: {data.get('estimated_time')}")
            return data.get('job_id')
        else:
            print(f"❌ Processing failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Processing error: {e}")
        return None

def monitor_processing(job_id):
    """Monitor processing progress"""
    print(f"📊 Monitoring processing progress...")
    
    while True:
        try:
            response = requests.get(f"{BACKEND_URL}/api/status/{job_id}")
            
            if response.status_code == 200:
                data = response.json()
                job_status = data.get('job_status', {})
                
                status = job_status.get('status', 'unknown')
                progress = job_status.get('progress', 0)
                
                print(f"   Status: {status} ({progress}%)")
                
                if status == 'completed':
                    print(f"✅ Processing completed successfully!")
                    return True
                elif status == 'error':
                    error = job_status.get('error', 'Unknown error')
                    print(f"❌ Processing failed: {error}")
                    return False
                
                time.sleep(2)  # Check every 2 seconds
            else:
                print(f"❌ Status check failed: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Status check error: {e}")
            return False
        except KeyboardInterrupt:
            print(f"\n⏸️  Monitoring interrupted by user")
            return False

def get_results(job_id):
    """Get processing results"""
    print(f"📥 Getting processing results...")
    
    try:
        response = requests.get(f"{BACKEND_URL}/api/download/{job_id}")
        
        if response.status_code == 200:
            data = response.json()
            files = data.get('files', [])
            
            print(f"✅ Processing results:")
            print(f"   Total files: {len(files)}")
            
            for i, file_info in enumerate(files, 1):
                print(f"   {i}. {file_info.get('filename')}")
                print(f"      Duration: {file_info.get('duration')}s")
                print(f"      Theme: {file_info.get('theme')}")
                print(f"      Resolution: {file_info.get('resolution')}")
                print(f"      Download URL: {BACKEND_URL}{file_info.get('download_url')}")
                print()
            
            return files
        else:
            print(f"❌ Failed to get results: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Results error: {e}")
        return None

def list_all_jobs():
    """List semua processing jobs"""
    print(f"📋 Listing all processing jobs...")
    
    try:
        response = requests.get(f"{BACKEND_URL}/api/jobs")
        
        if response.status_code == 200:
            data = response.json()
            jobs = data.get('jobs', [])
            
            print(f"✅ Found {len(jobs)} jobs:")
            
            for job in jobs:
                print(f"   Job ID: {job.get('job_id')}")
                print(f"   Status: {job.get('status')}")
                print(f"   Progress: {job.get('progress')}%")
                print(f"   Start time: {job.get('start_time')}")
                if job.get('end_time'):
                    print(f"   End time: {job.get('end_time')}")
                print()
            
            return jobs
        else:
            print(f"❌ Failed to list jobs: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Jobs listing error: {e}")
        return None

def main():
    """Main demo function"""
    print_banner()
    
    # Check backend health
    if not check_backend_health():
        print("\n💡 To start backend server, run: python run_backend.py")
        sys.exit(1)
    
    print()
    
    # Option 1: Use demo video
    print("🎯 Demo Options:")
    print("1. Download and use demo video")
    print("2. Use your own video file")
    print("3. List existing jobs")
    print("4. Exit")
    
    try:
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == "1":
            # Download demo video
            video_path = download_demo_video()
            if not video_path:
                sys.exit(1)
        elif choice == "2":
            # Use custom video
            video_path = input("Enter video file path: ").strip()
            if not os.path.exists(video_path):
                print(f"❌ File not found: {video_path}")
                sys.exit(1)
        elif choice == "3":
            # List jobs
            list_all_jobs()
            sys.exit(0)
        elif choice == "4":
            print("👋 Goodbye!")
            sys.exit(0)
        else:
            print("❌ Invalid option")
            sys.exit(1)
        
        print()
        
        # Upload video
        upload_result = upload_video(video_path)
        if not upload_result:
            sys.exit(1)
        
        print()
        
        # Start processing
        job_id = start_processing(upload_result['file_path'])
        if not job_id:
            sys.exit(1)
        
        print()
        
        # Monitor processing
        if monitor_processing(job_id):
            print()
            # Get results
            results = get_results(job_id)
            
            if results:
                print("🎉 Demo completed successfully!")
                print(f"💡 You can now download the generated videos from the URLs above")
        
    except KeyboardInterrupt:
        print(f"\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")

if __name__ == "__main__":
    main()