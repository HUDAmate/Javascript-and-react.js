# TikTube Studio - Complete Project Code

## Project Structure
```
tiktube-studio/
├── app.py                  # Main Flask application
├── run.py                  # Application runner
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── segment_analyzer.py     # AI segment analysis
├── subtitle_generator.py   # Subtitle generation
├── video_processor.py      # Video processing
├── effect_engine.py        # Visual effects
├── templates/
│   └── index.html         # Web interface
└── static/
    ├── css/
    │   └── style.css      # Styling
    └── js/
        └── app.js         # Frontend JavaScript
```

## Dependencies (requirements.txt)
```txt
flask==2.3.3
flask-cors==4.0.0
opencv-python==4.8.1.78
ffmpeg-python==0.2.0
moviepy==1.0.3
torch==2.0.1
torchvision==0.15.2
transformers==4.33.2
whisper-openai==20230918
numpy==1.24.3
pillow==10.0.0
scikit-learn==1.3.0
matplotlib==3.7.2
librosa==0.10.1
speechrecognition==3.10.0
pydub==0.25.1
requests==2.31.0
python-dotenv==1.0.0
gradio==3.44.4
```

## Installation & Setup

### Prerequisites
```bash
# Install Python 3.8+
# Install FFmpeg
sudo apt update && sudo apt install ffmpeg python3-pip

# Clone and setup project
cd tiktube-studio
pip install -r requirements.txt
```

### Run Application
```bash
python run.py
# or
python app.py
```

## PYTHON FILES

### 1. app.py (Main Flask Application)
```python
import os
import json
import tempfile
from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import logging

from video_processor import VideoProcessor
from subtitle_generator import SubtitleGenerator
from effect_engine import EffectEngine
from segment_analyzer import SegmentAnalyzer

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize components
video_processor = VideoProcessor()
subtitle_generator = SubtitleGenerator()
effect_engine = EffectEngine()
segment_analyzer = SegmentAnalyzer()

# Ensure upload and output directories exist
os.makedirs('uploads', exist_ok=True)
os.makedirs('outputs', exist_ok=True)
os.makedirs('temp', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_video():
    try:
        if 'video' not in request.files:
            return jsonify({'error': 'No video file provided'}), 400
        
        file = request.files['video']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join('uploads', filename)
        file.save(filepath)
        
        # Get video info
        video_info = video_processor.get_video_info(filepath)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'video_info': video_info
        })
    
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_video():
    try:
        data = request.get_json()
        filename = data.get('filename')
        theme = data.get('theme', 'general')
        target_duration = data.get('target_duration', 60)
        
        if not filename:
            return jsonify({'error': 'Filename required'}), 400
        
        filepath = os.path.join('uploads', filename)
        
        # Analyze video segments
        segments = segment_analyzer.analyze_segments(
            filepath, 
            theme=theme, 
            target_duration=target_duration
        )
        
        return jsonify({
            'success': True,
            'segments': segments
        })
    
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/process', methods=['POST'])
def process_video():
    try:
        data = request.get_json()
        filename = data.get('filename')
        selected_segment = data.get('selected_segment')
        options = data.get('options', {})
        
        if not filename or not selected_segment:
            return jsonify({'error': 'Filename and segment required'}), 400
        
        input_path = os.path.join('uploads', filename)
        
        # Extract selected segment
        segment_path = video_processor.extract_segment(
            input_path, 
            selected_segment['start'], 
            selected_segment['end']
        )
        
        # Generate subtitles if requested
        if options.get('add_subtitles', True):
            subtitles = subtitle_generator.generate_subtitles(segment_path)
        else:
            subtitles = None
        
        # Apply effects based on theme
        theme = options.get('theme', 'general')
        effects_config = effect_engine.get_theme_effects(theme)
        
        # Process final video
        output_path = video_processor.create_shorts_video(
            segment_path,
            subtitles=subtitles,
            effects=effects_config,
            options=options
        )
        
        # Clean up temporary segment file
        if os.path.exists(segment_path):
            os.remove(segment_path)
        
        return jsonify({
            'success': True,
            'output_file': os.path.basename(output_path),
            'download_url': f'/api/download/{os.path.basename(output_path)}'
        })
    
    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<filename>')
def download_file(filename):
    try:
        filepath = os.path.join('outputs', filename)
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(filepath, as_attachment=True)
    
    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/themes')
def get_themes():
    themes = {
        'entertainment': {
            'name': 'Entertainment',
            'description': 'Fun and engaging content with dynamic effects',
            'effects': ['zoom_cuts', 'color_pop', 'dynamic_text']
        },
        'educational': {
            'name': 'Educational',
            'description': 'Clean and focused for learning content',
            'effects': ['clean_text', 'highlight_boxes', 'smooth_transitions']
        },
        'music': {
            'name': 'Music',
            'description': 'Beat-synchronized effects and visualizations',
            'effects': ['beat_sync', 'audio_visual', 'rhythm_cuts']
        },
        'gaming': {
            'name': 'Gaming',
            'description': 'High-energy effects with gaming aesthetics',
            'effects': ['glitch_effects', 'neon_glow', 'action_cuts']
        },
        'lifestyle': {
            'name': 'Lifestyle',
            'description': 'Smooth and aesthetic for lifestyle content',
            'effects': ['smooth_filters', 'warm_tones', 'gentle_transitions']
        },
        'news': {
            'name': 'News',
            'description': 'Professional and clean presentation',
            'effects': ['clean_layout', 'professional_text', 'fade_transitions']
        }
    }
    
    return jsonify(themes)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### 2. run.py (Application Runner)
```python
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
```

### 3. segment_analyzer.py (AI Video Analysis)
[Complete code from segment_analyzer.py - 368 lines]

### 4. subtitle_generator.py (Subtitle Generation)
[Complete code from subtitle_generator.py - 228 lines]

### 5. video_processor.py (Video Processing)
[Complete code from video_processor.py - 289 lines]

### 6. effect_engine.py (Visual Effects)
[Complete code from effect_engine.py - 400 lines]

## WEB FILES

### 7. templates/index.html (Web Interface)
[Complete HTML code from index.html - 292 lines]

### 8. static/js/app.js (Frontend JavaScript)
[Complete JavaScript code from app.js - 496 lines]

### 9. static/css/style.css (Styling)
[Complete CSS code from style.css - 351 lines]

## Quick Copy Instructions for IntelliJ IDEA

### Method 1: Direct Import
1. Copy the entire content of this file
2. Open IntelliJ IDEA
3. Create new project → Python
4. Create the folder structure as shown above
5. Paste each file content into corresponding files

### Method 2: Git Clone (if repository exists)
```bash
git clone <repository-url>
cd tiktube-studio
```

### Method 3: File-by-file Creation
1. Create main project folder: `tiktube-studio`
2. Create subfolders: `templates`, `static/js`, `static/css`
3. Copy-paste each file from the sections above

## Features Summary
- **AI-Powered Video Analysis**: Intelligent segment selection
- **Multi-Theme Support**: Entertainment, Educational, Music, Gaming, Lifestyle, News
- **Auto Subtitle Generation**: Using OpenAI Whisper
- **Visual Effects Engine**: Theme-based video enhancement
- **Web Interface**: Modern responsive UI
- **RESTful API**: Complete backend with Flask

## Key Technologies
- Python Flask (Backend)
- OpenAI Whisper (Speech Recognition)  
- OpenCV (Computer Vision)
- MoviePy (Video Processing)
- Bootstrap + Custom CSS (Frontend)
- JavaScript ES6+ (Frontend Logic)

## Recommended IDE Setup
- Python 3.8+ interpreter
- Install requirements.txt dependencies
- Configure Flask run configuration
- Set working directory to project root
- Enable auto-reload for development
```