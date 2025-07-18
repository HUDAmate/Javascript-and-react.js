# 🎬 TikTub Studio - Enhanced Setup Guide

## AI-Powered Short Video Creator

Transform your long videos into viral shorts with advanced AI analysis, automatic subtitles, and professional effects - just like Duolingo's smooth UX!

## ✨ New Features

### 🤖 Enhanced AI Video Analysis
- **Advanced scene detection** with YOLO object recognition
- **Face detection** and tracking for optimal framing
- **Motion analysis** with optical flow algorithms
- **Audio quality assessment** with speech detection
- **Technical quality scoring** (focus, exposure, stability)

### 🎨 Professional Effects System
- **AI-driven color grading** with cinematic filters
- **Dynamic transitions** based on content analysis
- **Animated text effects** with multiple styles
- **Theme-aware visual effects** (energetic, calm, educational, entertainment, dramatic)

### 📱 Modern Duolingo-Inspired UI
- **Card-based design** with smooth animations
- **Drag-and-drop** video upload
- **Real-time progress tracking** with visual feedback
- **Responsive interface** optimized for efficiency

## 🚀 Quick Start

### 1. Install Dependencies

#### Python Backend
```bash
cd python_backend
pip install -r ../requirements.txt
```

#### Java Frontend
```bash
cd java_frontend
mvn clean install
```

### 2. Start the Application

#### Option A: Using the startup script
```bash
python start_application.py
```

#### Option B: Manual startup
```bash
# Terminal 1 - Start Python backend
python run_backend.py

# Terminal 2 - Start Java frontend  
cd java_frontend
mvn exec:java -Dexec.mainClass="com.tiktubstudio.TikTubStudioApp"
```

### 3. Open TikTub Studio
The application will automatically open the modern GUI interface.

## 🛠️ System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.14+, Ubuntu 18.04+
- **RAM**: 8GB (16GB recommended)
- **Storage**: 10GB free space
- **GPU**: Optional (CUDA-compatible for faster processing)
- **Java**: 11 or higher
- **Python**: 3.8 or higher

### Recommended for Best Performance
- **RAM**: 16GB+
- **GPU**: NVIDIA RTX series with 6GB+ VRAM
- **CPU**: Multi-core processor (Intel i7/AMD Ryzen 7+)
- **Storage**: SSD with 50GB+ free space

## 📋 Usage Guide

### Step 1: Upload Your Video
1. **Drag & Drop** your video file onto the upload area
2. **Or click** "Choose Video File" to browse
3. Supported formats: MP4, MOV, AVI, MKV (max 2GB)
4. Preview your video details

### Step 2: Configure Processing Options
1. **Select platform**: TikTok, YouTube Shorts, Instagram Reels, or Custom
2. **Choose effect theme**: 
   - **Auto**: AI detects the best theme
   - **Energetic**: Fast cuts, vibrant colors, dynamic effects
   - **Calm**: Smooth transitions, soft colors, gentle effects
   - **Educational**: Clean cuts, professional appearance
   - **Entertainment**: Creative transitions, fun effects
   - **Dramatic**: Cinematic grading, slow motion, intense effects
3. **Set parameters**:
   - Number of short videos to generate (1-5)
   - Target duration (15-90 seconds)
   - Subtitle language
   - Quality settings

### Step 3: AI Processing
The AI will automatically:
1. **Analyze** your video content with multiple algorithms
2. **Identify** the most engaging segments
3. **Generate** accurate subtitles with speech recognition
4. **Apply** appropriate effects based on content theme
5. **Create** multiple short video variants

### Step 4: Review & Export
1. **Preview** generated videos
2. **Download** your favorites
3. **Share** directly to social platforms
4. **Adjust** settings and regenerate if needed

## 🎯 AI Features Explained

### Scene Detection Algorithm
Our enhanced AI uses multiple factors to identify the best video segments:

- **Visual Appeal** (25%): Composition, contrast, color distribution
- **Motion Activity** (20%): Movement intensity, scene changes
- **Audio Quality** (15%): Speech clarity, background noise levels
- **Face Presence** (15%): Human faces for engagement
- **Object Interest** (10%): Interesting objects detected by YOLO
- **Scene Diversity** (10%): Variety to avoid monotony
- **Technical Quality** (5%): Focus, exposure, stability

### Smart Effects System
Effects are automatically selected based on:

- **Content analysis**: What's happening in the video
- **Motion intensity**: How much movement is present
- **Color temperature**: Warm vs cool tones
- **Brightness levels**: Dark vs bright scenes
- **Audio characteristics**: Speech vs music vs silence

### Intelligent Subtitles
- **Whisper AI** for accurate transcription
- **Multi-language support** with auto-detection
- **Smart punctuation** and capitalization
- **Animated text styles** that match the video theme
- **Mobile-optimized** positioning and sizing

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
# API Configuration
FLASK_HOST=localhost
FLASK_PORT=5000
FLASK_DEBUG=False

# AI Model Settings
WHISPER_MODEL_SIZE=medium
YOLO_MODEL_PATH=yolov8n.pt
USE_GPU=True

# Processing Settings
MAX_VIDEO_SIZE=2147483648  # 2GB
MAX_PROCESSING_TIME=600   # 10 minutes
TEMP_DIR=/tmp/tiktubstudio

# Output Settings
DEFAULT_OUTPUT_FORMAT=mp4
DEFAULT_QUALITY=high
DEFAULT_RESOLUTION=1080x1920
```

### Advanced Settings
Edit `config.json` for advanced configuration:

```json
{
  "ai_analysis": {
    "scene_detection_threshold": 0.7,
    "face_detection_confidence": 0.5,
    "motion_sensitivity": 0.6,
    "quality_weights": {
      "visual_appeal": 0.25,
      "motion_activity": 0.20,
      "audio_quality": 0.15,
      "face_presence": 0.15,
      "object_interest": 0.10,
      "scene_diversity": 0.10,
      "technical_quality": 0.05
    }
  },
  "effects": {
    "enable_color_grading": true,
    "enable_dynamic_transitions": true,
    "enable_audio_sync": true,
    "max_effect_intensity": 1.5
  },
  "subtitles": {
    "max_words_per_line": 8,
    "min_display_duration": 1.0,
    "animation_duration": 0.3,
    "font_size_mobile": 50
  }
}
```

## 🐛 Troubleshooting

### Common Issues

#### "Failed to load YOLO model"
```bash
# Download YOLO model manually
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

#### "CUDA out of memory"
- Reduce video resolution or length
- Close other GPU-intensive applications
- Set `USE_GPU=False` in environment variables

#### "Whisper model download failed"
```bash
# Download Whisper model manually
python -c "import whisper; whisper.load_model('medium')"
```

#### "Java application won't start"
```bash
# Check Java version
java -version

# Should be Java 11 or higher
# Install if needed: https://adoptium.net/
```

#### "Processing takes too long"
- Use smaller video files (under 10 minutes)
- Reduce the number of output videos
- Close other applications to free up resources
- Consider using GPU acceleration

### Performance Optimization

#### For Better Speed:
1. **Use GPU acceleration** if available
2. **Close unnecessary applications**
3. **Use SSD storage** for temp files
4. **Increase RAM allocation** for Java JVM
5. **Use smaller input videos** (under 10 minutes)

#### For Better Quality:
1. **Use high-resolution source videos**
2. **Ensure good audio quality**
3. **Avoid heavily compressed videos**
4. **Use adequate lighting** in source videos
5. **Include clear speech** for better subtitles

## 📚 API Reference

### Python Backend Endpoints

```python
# Upload video
POST /api/upload
Content-Type: multipart/form-data

# Analyze video
POST /api/analyze/{video_id}
{
  "target_segments": 3,
  "analysis_depth": "full"
}

# Generate effects
POST /api/effects/{video_id}
{
  "theme": "auto",
  "intensity": 1.0,
  "custom_config": {}
}

# Process video
POST /api/process/{video_id}
{
  "platform": "tiktok",
  "segments": 3,
  "theme": "energetic",
  "subtitle_language": "auto"
}
```

### Java Frontend Architecture

```java
// Main components
com.tiktubstudio.ui.MainWindow          // Main application window
com.tiktubstudio.ui.components.*        // Reusable UI components
com.tiktubstudio.ui.panels.*           // Card-based panels
com.tiktubstudio.api.ApiClient         // Backend communication

// Key classes
ModernButton                           // Duolingo-style buttons
RoundedPanel                          // Card containers
VideoUploadCard                       // Drag-and-drop upload
ProcessingOptionsCard                 // Configuration panel
ProgressCard                          // Real-time progress
ResultsCard                           // Preview and download
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### Code Style
- **Python**: Follow PEP 8
- **Java**: Follow Google Java Style Guide
- **UI**: Maintain Duolingo-inspired design consistency

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI Whisper** for speech recognition
- **Ultralytics YOLO** for object detection
- **MoviePy** for video processing
- **FlatLaf** for modern Java UI
- **Duolingo** for UI/UX inspiration

## 📞 Support

- **GitHub Issues**: [Report bugs](https://github.com/your-repo/issues)
- **Documentation**: [Full docs](https://docs.tiktubstudio.com)
- **Email**: support@tiktubstudio.com
- **Discord**: [Join our community](https://discord.gg/tiktubstudio)

---

**Happy video creating! 🎬✨**