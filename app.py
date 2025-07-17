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