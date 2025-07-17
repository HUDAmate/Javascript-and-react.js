# TikTube Studio 🎬

**Transform your long videos into engaging shorts with AI-powered segment selection, accurate subtitles, and theme-based effects.**

TikTube Studio adalah aplikasi web yang menggunakan kecerdasan buatan untuk menganalisis video panjang dan mengubahnya menjadi video shorts yang menarik. Aplikasi ini dilengkapi dengan kemampuan pemilihan segmen terbaik, pembuatan subtitle yang akurat, dan penerapan efek sesuai tema.

## ✨ Fitur Utama

### 🧠 AI-Powered Analysis
- **Analisis Cerdas**: Menggunakan AI untuk mengidentifikasi segmen terbaik berdasarkan kualitas konten dan tema
- **Deteksi Gerakan**: Analisis optical flow untuk mendeteksi bagian video dengan aksi terbaik
- **Analisis Audio**: Ekstraksi fitur audio seperti tempo, energi, dan kualitas suara
- **Scoring System**: Sistem penilaian komprehensif untuk setiap segmen video

### 🎯 Theme-Based Processing
- **Entertainment**: Efek dinamis dengan zoom dan peningkatan warna
- **Educational**: Fokus pada kejelasan dengan kontras dan kecerahan optimal
- **Music**: Efek sinkronisasi beat dengan pulse warna
- **Gaming**: High contrast dengan efek glitch dan saturasi tinggi
- **Lifestyle**: Filter hangat dengan soft glow untuk estetika
- **News**: Grading warna profesional yang netral

### 📝 Accurate Subtitles
- **Whisper Integration**: Menggunakan OpenAI Whisper untuk transkripsi yang akurat
- **Word-level Timestamps**: Subtitle dengan timing yang presisi
- **Multi-language Support**: Deteksi bahasa otomatis
- **Customizable Styling**: Font, warna, dan ukuran subtitle dapat disesuaikan

### 🎨 Smart Effects Engine
- **Auto Crop**: Otomatis crop ke format 9:16 untuk shorts
- **Color Grading**: Peningkatan warna berdasarkan tema
- **Visual Effects**: Zoom, transisi, dan efek visual lainnya
- **Professional Output**: Video berkualitas tinggi dengan bitrate optimal

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- FFmpeg
- Git

### Installation

1. **Clone Repository**
```bash
git clone <repository-url>
cd tiktube-studio
```

2. **Install Dependencies**
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

4. **Run Application**
```bash
python app.py
```

5. **Open Browser**
Buka browser dan kunjungi `http://localhost:5000`

## 📖 How to Use

### 1. Upload Video
- Drag & drop video file atau klik "Choose File"
- Format yang didukung: MP4, AVI, MOV, MKV, WMV, FLV
- Maksimal ukuran file: 500MB

### 2. Select Theme
Pilih tema yang sesuai dengan konten video Anda:
- **Entertainment**: Untuk konten hiburan yang dinamis
- **Educational**: Untuk konten pembelajaran
- **Music**: Untuk konten musik atau dance
- **Gaming**: Untuk gameplay dan konten gaming
- **Lifestyle**: Untuk vlog dan konten lifestyle
- **News**: Untuk berita dan konten profesional

### 3. Configure Settings
- **Target Duration**: Pilih durasi video shorts (15-180 detik)
- **Add Subtitles**: Enable/disable subtitle generation
- **Apply Theme Effects**: Enable/disable efek visual

### 4. AI Analysis
Sistem AI akan menganalisis video dan memberikan rekomendasi segmen terbaik berdasarkan:
- Kualitas visual (kontras, kecerahan, saturasi)
- Aktivitas audio (energi, kejelasan)
- Gerakan dan aksi
- Kesesuaian dengan tema

### 5. Select & Process
- Pilih segmen yang direkomendasikan
- Sistem akan memproses video dengan efek dan subtitle
- Download video shorts yang telah jadi

## 🏗️ Architecture

### Backend Components
```
├── app.py                  # Main Flask application
├── video_processor.py      # Video processing & effects
├── subtitle_generator.py   # Whisper-based subtitle generation
├── segment_analyzer.py     # AI-powered segment analysis
├── effect_engine.py        # Theme-based effects
└── requirements.txt        # Python dependencies
```

### Frontend Components
```
├── templates/
│   └── index.html         # Main web interface
├── static/
│   ├── css/
│   │   └── style.css      # Modern UI styling
│   └── js/
│       └── app.js         # Interactive frontend logic
```

### Processing Pipeline

1. **Video Upload & Analysis**
   ```python
   Video → FFmpeg Info → Duration/Resolution/FPS
   ```

2. **Segment Extraction**
   ```python
   Video → Sample Frames → Feature Extraction → Scoring
   ```

3. **AI Analysis**
   ```python
   Features → Theme Matching → Confidence Scoring → Ranking
   ```

4. **Video Processing**
   ```python
   Segment → Resize/Crop → Effects → Subtitles → Export
   ```

## ⚙️ Configuration

### Video Settings
```python
# In video_processor.py
TARGET_WIDTH = 1080      # Shorts width
TARGET_HEIGHT = 1920     # Shorts height
BITRATE = '8000k'        # Output bitrate
CODEC = 'libx264'        # Video codec
```

### Subtitle Settings
```python
# In subtitle_generator.py
MODEL_SIZE = 'base'           # Whisper model size
MAX_WORDS_PER_SUBTITLE = 6    # Words per subtitle
MAX_SUBTITLE_DURATION = 3.0   # Max subtitle duration
```

### Effect Settings
```python
# In effect_engine.py
ZOOM_INTENSITY = {
    'entertainment': 0.15,
    'educational': 0.05,
    'music': 0.2,
    # ... other themes
}
```

## 🛠️ Advanced Usage

### Custom Themes
Tambahkan tema baru dengan mengedit `effect_engine.py`:

```python
'custom_theme': {
    'type': 'custom_theme',
    'zoom_intensity': 0.1,
    'color_boost': 1.15,
    'transition_style': 'smooth',
    'motion_blur': False
}
```

### API Endpoints

- `POST /api/upload` - Upload video file
- `POST /api/analyze` - Analyze video segments  
- `POST /api/process` - Process selected segment
- `GET /api/themes` - Get available themes
- `GET /api/download/<filename>` - Download processed video

### Custom Effects
Implementasi efek kustom di `video_processor.py`:

```python
def _apply_custom_effect(self, clip):
    def custom_effect(get_frame, t):
        frame = get_frame(t)
        # Apply custom processing
        return processed_frame
    
    return clip.fl(custom_effect, apply_to=[])
```

## 🔧 Troubleshooting

### Common Issues

**1. FFmpeg Not Found**
```bash
# Install FFmpeg
sudo apt install ffmpeg  # Linux
brew install ffmpeg      # macOS
```

**2. Whisper Model Download**
Model Whisper akan didownload otomatis saat pertama kali dijalankan.

**3. Memory Issues**
Untuk video besar, pastikan RAM cukup (minimum 4GB).

**4. Processing Slow**
- Gunakan GPU jika tersedia
- Kurangi resolusi input
- Pilih segmen yang lebih pendek

### Log Files
Check logs untuk debugging:
```bash
tail -f app.log
```

## 📊 Performance

### Processing Times (Approximate)
- **1 minute video**: 30-60 seconds
- **5 minute video**: 2-5 minutes  
- **10 minute video**: 5-10 minutes

*Times vary based on hardware and video complexity*

### Hardware Requirements
- **Minimum**: 4GB RAM, 2 CPU cores
- **Recommended**: 8GB RAM, 4 CPU cores, GPU
- **Storage**: 2GB free space

## 🤝 Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🙏 Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) for speech recognition
- [MoviePy](https://github.com/Zulko/moviepy) for video processing
- [OpenCV](https://opencv.org/) for computer vision
- [Flask](https://flask.palletsprojects.com/) for web framework
- [Bootstrap](https://getbootstrap.com/) for UI components

## 📞 Support

Jika Anda mengalami masalah atau memiliki pertanyaan:

1. Check [Issues](../../issues) untuk masalah yang sudah ada
2. Buat [New Issue](../../issues/new) untuk bug report atau feature request
3. Baca dokumentasi lengkap di repository

---

**TikTube Studio** - Transform your content with AI 🚀