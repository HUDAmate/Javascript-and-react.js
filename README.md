# 🎬 TikTub Studio

**AI-Powered Short Video Creator** - Transform long videos into engaging short clips with automatic subtitles and smart effects.

![TikTub Studio](https://img.shields.io/badge/Version-1.0.0-brightgreen) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Java](https://img.shields.io/badge/Java-11+-orange) ![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

### 🎯 Smart Video Analysis
- **AI-powered content analysis** untuk menentukan bagian terbaik video
- **Motion detection** untuk mengidentifikasi scene yang menarik
- **Audio analysis** untuk mencari segment dengan audio berkualitas
- **Visual scoring** berdasarkan kontras, warna, dan komposisi

### 🗣️ Accurate Subtitle Generation
- **Whisper AI integration** untuk transcription akurat
- **Multi-language support** (Indonesia, English, dll)
- **Automatic punctuation** dan capitalization
- **Smart text formatting** untuk readability optimal
- **Multiple subtitle formats** (SRT, VTT, JSON)

### 🎨 Intelligent Effect System
- **Theme detection** otomatis berdasarkan konten
- **5 effect themes**: Energetic, Calm, Educational, Entertainment, Dramatic
- **Smart color grading** sesuai dengan mood video
- **Animated text effects** yang responsif
- **Transition effects** yang smooth

### 📱 Multi-Platform Output
- **TikTok** (9:16, optimal untuk portrait)
- **YouTube Shorts** (9:16, dengan metadata optimization)
- **Instagram Reels** (9:16, dengan hashtag suggestions)
- **Custom formats** sesuai kebutuhan

### 💻 Modern User Interface
- **Desktop application** dengan Java Swing + FlatLaf
- **Dark theme** yang nyaman untuk mata
- **Real-time progress** tracking
- **Drag & drop** file upload
- **Preview system** untuk hasil video

## 🏗️ Architecture

```
TikTub Studio
├── 🐍 Python Backend (AI & Processing)
│   ├── Video Analysis (OpenCV, scikit-learn)
│   ├── Subtitle Generation (Whisper, NLTK)
│   ├── Effect Generation (MoviePy, Transformers)
│   ├── Video Processing (FFmpeg, MoviePy)
│   └── REST API (Flask)
└── ☕ Java Frontend (GUI)
    ├── Modern UI (Swing + FlatLaf)
    ├── API Client (Apache HTTP)
    ├── File Management
    └── Video Preview
```

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** dengan pip
- **Java 11+** dengan Maven
- **FFmpeg** (untuk video processing)
- **4GB+ RAM** (recommended 8GB)
- **GPU support** (optional, untuk processing lebih cepat)

### Installation

1. **Clone repository**
```bash
git clone https://github.com/your-username/tiktub-studio.git
cd tiktub-studio
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Install FFmpeg**
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

4. **Start Backend Server**
```bash
python run_backend.py
```

5. **Start Frontend Application**
```bash
./run_frontend.sh  # Linux/macOS
# atau
run_frontend.bat   # Windows
```

## 📖 User Guide

### 1. Upload Video
- Klik **"Choose Video"** untuk memilih file
- Supported formats: MP4, MOV, AVI, MKV
- Optimal duration: 5-30 minutes
- Max file size: 2GB

### 2. Configure Processing
- **Platform**: Pilih target platform (TikTok, YouTube, Instagram)
- **Segments**: Tentukan jumlah short video (1-10)
- **Theme**: Auto-detect atau manual selection
- **Language**: Bahasa untuk subtitle (Auto/ID/EN)

### 3. Start Processing
- Klik **"Start Processing"**
- Monitor progress real-time
- Processing time: 2-10 minutes (tergantung durasi video)

### 4. Download Results
- Preview generated videos
- Download individual files
- Batch download semua hasil

## 🔧 Configuration

### Backend Configuration
Edit `python_backend/config.py`:
```python
# AI Models
WHISPER_MODEL_SIZE = "medium"  # tiny, base, small, medium, large
EFFECT_ANALYSIS_DEPTH = "balanced"  # fast, balanced, thorough

# Processing
MAX_CONCURRENT_JOBS = 2
VIDEO_QUALITY = "high"  # low, medium, high
OUTPUT_FORMAT = "mp4"

# Server
HOST = "0.0.0.0"
PORT = 5000
DEBUG = False
```

### Frontend Configuration
Edit `java_frontend/src/main/resources/config.properties`:
```properties
# API Settings
api.base.url=http://localhost:5000
api.timeout=30000

# UI Settings
ui.theme=dark
ui.language=id
ui.auto.preview=true

# File Settings
upload.max.size=2147483648
temp.directory=./temp
```

## 🎯 Advanced Features

### Custom Effect Templates
Create custom effect configurations:
```json
{
  "theme_name": "corporate",
  "transitions": ["clean_cut", "fade"],
  "colors": ["professional", "blue_tones"],
  "text_style": "corporate_clean",
  "music_style": "corporate"
}
```

### Batch Processing
Process multiple videos:
```python
from python_backend.core.video_processor import VideoProcessor

processor = VideoProcessor()
videos = ["video1.mp4", "video2.mp4", "video3.mp4"]

for video in videos:
    result = processor.process_video(video, config)
    print(f"Processed: {result['final_videos']}")
```

### API Integration
Use REST API directly:
```bash
# Upload video
curl -X POST -F "video=@input.mp4" http://localhost:5000/api/upload

# Start processing
curl -X POST -H "Content-Type: application/json" \
  -d '{"file_path":"/path/to/video.mp4","config":{"platform":"tiktok"}}' \
  http://localhost:5000/api/process

# Check status
curl http://localhost:5000/api/status/{job_id}
```

## 🔍 Technical Details

### AI Models Used
- **Whisper** (OpenAI) - Speech-to-text transcription
- **BLIP** (Salesforce) - Image captioning untuk content analysis
- **Sentence Transformers** - Text embedding untuk keyword extraction
- **KeyBERT** - Keyword extraction dari subtitle

### Video Processing Pipeline
1. **Analysis Phase** (10%)
   - Extract key frames (1 fps sampling)
   - Audio feature extraction
   - Motion detection dengan optical flow
   - Content scoring algorithm

2. **Subtitle Generation Phase** (30%)
   - Audio extraction dengan MoviePy
   - Whisper transcription dengan beam search
   - Text cleaning dan punctuation
   - Segment optimization untuk readability

3. **Effect Generation Phase** (20%)
   - Theme classification dari visual + text features
   - Color grading parameter calculation
   - Transition effect selection
   - Text animation parameter tuning

4. **Rendering Phase** (40%)
   - Video segmentation berdasarkan analysis
   - Subtitle overlay dengan custom styling
   - Effect application dengan MoviePy
   - Multi-format output generation

### Performance Optimization
- **GPU acceleration** untuk AI models (CUDA support)
- **Multi-threading** untuk parallel processing
- **Memory management** untuk large video files
- **Caching system** untuk reused computations

## 🐛 Troubleshooting

### Common Issues

**Backend tidak bisa start**
```bash
# Check Python version
python --version

# Install dependencies manually
pip install --upgrade torch whisper opencv-python moviepy flask

# Check FFmpeg
ffmpeg -version
```

**Frontend build error**
```bash
# Check Java version
java -version

# Clean Maven cache
mvn clean

# Update dependencies
mvn dependency:resolve
```

**Processing terlalu lambat**
- Gunakan GPU jika tersedia
- Kurangi resolusi video input
- Gunakan model Whisper yang lebih kecil
- Tutup aplikasi lain yang berat

**Subtitle tidak akurat**
- Pastikan audio jelas dan tidak berisik
- Pilih bahasa yang tepat
- Gunakan model Whisper yang lebih besar
- Check mikrofon quality dari video original

## 🤝 Contributing

Kami welcome contributions! Please read [CONTRIBUTING.md](CONTRIBUTING.md) untuk guidelines.

### Development Setup
```bash
# Backend development
pip install -r requirements-dev.txt
python -m pytest tests/

# Frontend development
cd java_frontend
mvn test
```

### Code Style
- Python: Follow PEP 8, use Black formatter
- Java: Follow Google Java Style Guide
- Commit messages: Use Conventional Commits format

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) - Outstanding speech recognition
- [MoviePy](https://github.com/Zulko/moviepy) - Powerful video editing library
- [FlatLaf](https://github.com/JFormDesigner/FlatLaf) - Modern Swing look and feel
- [Transformers](https://github.com/huggingface/transformers) - State-of-the-art NLP models

## 📞 Support

- 📧 Email: support@tiktubstudio.com
- 💬 Discord: [TikTub Studio Community](https://discord.gg/tiktubstudio)
- 📖 Documentation: [docs.tiktubstudio.com](https://docs.tiktubstudio.com)
- 🐛 Issues: [GitHub Issues](https://github.com/your-username/tiktub-studio/issues)

---

**Made with ❤️ for content creators worldwide**

*Transform your long-form content into viral short videos with the power of AI!*