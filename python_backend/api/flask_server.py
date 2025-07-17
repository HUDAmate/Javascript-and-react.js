from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import os
import uuid
import threading
import logging
from typing import Dict, Optional
import tempfile
import json
from datetime import datetime
import traceback

from ..core.video_processor import VideoProcessor

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS untuk komunikasi dengan Java frontend

# Global variables
video_processor = VideoProcessor()
processing_jobs = {}  # Store processing jobs status
upload_folder = tempfile.mkdtemp()

# Ensure upload folder exists
os.makedirs(upload_folder, exist_ok=True)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'TikTub Studio Backend'
    })

@app.route('/api/upload', methods=['POST'])
def upload_video():
    """Upload video file endpoint"""
    try:
        if 'video' not in request.files:
            return jsonify({'error': 'No video file provided'}), 400
        
        file = request.files['video']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        file_extension = os.path.splitext(file.filename)[1]
        filename = f"{file_id}{file_extension}"
        
        # Save file
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        # Get file info
        file_size = os.path.getsize(file_path)
        
        logger.info(f"Video uploaded: {filename}, size: {file_size} bytes")
        
        return jsonify({
            'success': True,
            'file_id': file_id,
            'filename': filename,
            'file_path': file_path,
            'file_size': file_size,
            'message': 'Video uploaded successfully'
        })
        
    except Exception as e:
        logger.error(f"Error uploading video: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_video():
    """Analyze video content endpoint"""
    try:
        data = request.get_json()
        file_path = data.get('file_path')
        
        if not file_path or not os.path.exists(file_path):
            return jsonify({'error': 'Invalid file path'}), 400
        
        # Analyze video
        analysis_result = video_processor.video_analyzer.analyze_video(file_path)
        
        return jsonify({
            'success': True,
            'analysis': analysis_result,
            'message': 'Video analyzed successfully'
        })
        
    except Exception as e:
        logger.error(f"Error analyzing video: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-subtitles', methods=['POST'])
def generate_subtitles():
    """Generate subtitles endpoint"""
    try:
        data = request.get_json()
        file_path = data.get('file_path')
        language = data.get('language', 'auto')
        
        if not file_path or not os.path.exists(file_path):
            return jsonify({'error': 'Invalid file path'}), 400
        
        # Generate subtitles
        subtitle_result = video_processor.subtitle_generator.generate_subtitle(file_path, language)
        
        return jsonify({
            'success': True,
            'subtitles': subtitle_result,
            'message': 'Subtitles generated successfully'
        })
        
    except Exception as e:
        logger.error(f"Error generating subtitles: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-effects', methods=['POST'])
def generate_effects():
    """Generate effects endpoint"""
    try:
        data = request.get_json()
        file_path = data.get('file_path')
        theme = data.get('theme', 'auto')
        subtitle_data = data.get('subtitle_data')
        
        if not file_path or not os.path.exists(file_path):
            return jsonify({'error': 'Invalid file path'}), 400
        
        # Generate effects
        effects_result = video_processor.effect_generator.generate_effects(
            file_path, theme, subtitle_data
        )
        
        return jsonify({
            'success': True,
            'effects': effects_result,
            'message': 'Effects generated successfully'
        })
        
    except Exception as e:
        logger.error(f"Error generating effects: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/process', methods=['POST'])
def process_video():
    """Process video to short videos endpoint"""
    try:
        data = request.get_json()
        file_path = data.get('file_path')
        config = data.get('config', {})
        
        if not file_path or not os.path.exists(file_path):
            return jsonify({'error': 'Invalid file path'}), 400
        
        # Generate job ID
        job_id = str(uuid.uuid4())
        
        # Default config
        default_config = {
            'platform': 'tiktok',
            'max_segments': 3,
            'segment_duration': 60,
            'auto_effects': True,
            'theme': 'auto',
            'language': 'auto',
            'output_dir': os.path.join(upload_folder, 'output', job_id)
        }
        
        # Merge with provided config
        final_config = {**default_config, **config}
        
        # Initialize job status
        processing_jobs[job_id] = {
            'status': 'processing',
            'progress': 0,
            'start_time': datetime.now(),
            'file_path': file_path,
            'config': final_config,
            'result': None,
            'error': None
        }
        
        # Start processing in background thread
        thread = threading.Thread(
            target=_process_video_background,
            args=(job_id, file_path, final_config)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'job_id': job_id,
            'message': 'Video processing started',
            'estimated_time': '2-5 minutes'
        })
        
    except Exception as e:
        logger.error(f"Error starting video processing: {str(e)}")
        return jsonify({'error': str(e)}), 500

def _process_video_background(job_id: str, file_path: str, config: Dict):
    """Background processing function"""
    try:
        logger.info(f"Starting background processing for job {job_id}")
        
        # Update status
        processing_jobs[job_id]['status'] = 'analyzing'
        processing_jobs[job_id]['progress'] = 10
        
        # Process video
        result = video_processor.process_video(file_path, config)
        
        # Update status
        processing_jobs[job_id]['status'] = 'completed'
        processing_jobs[job_id]['progress'] = 100
        processing_jobs[job_id]['result'] = result
        processing_jobs[job_id]['end_time'] = datetime.now()
        
        logger.info(f"Background processing completed for job {job_id}")
        
    except Exception as e:
        logger.error(f"Error in background processing for job {job_id}: {str(e)}")
        processing_jobs[job_id]['status'] = 'error'
        processing_jobs[job_id]['error'] = str(e)
        processing_jobs[job_id]['traceback'] = traceback.format_exc()

@app.route('/api/status/<job_id>', methods=['GET'])
def get_processing_status(job_id: str):
    """Get processing status endpoint"""
    try:
        if job_id not in processing_jobs:
            return jsonify({'error': 'Job not found'}), 404
        
        job_status = processing_jobs[job_id].copy()
        
        # Calculate elapsed time
        if 'start_time' in job_status:
            elapsed = datetime.now() - job_status['start_time']
            job_status['elapsed_seconds'] = elapsed.total_seconds()
        
        # Remove sensitive data
        if 'file_path' in job_status:
            del job_status['file_path']
        
        return jsonify({
            'success': True,
            'job_status': job_status
        })
        
    except Exception as e:
        logger.error(f"Error getting job status: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<job_id>', methods=['GET'])
def download_results(job_id: str):
    """Download processing results endpoint"""
    try:
        if job_id not in processing_jobs:
            return jsonify({'error': 'Job not found'}), 404
        
        job = processing_jobs[job_id]
        
        if job['status'] != 'completed':
            return jsonify({'error': 'Job not completed yet'}), 400
        
        result = job['result']
        if not result or 'final_videos' not in result:
            return jsonify({'error': 'No results available'}), 404
        
        # Return list of downloadable files
        downloadable_files = []
        for video in result['final_videos']:
            if os.path.exists(video['output_path']):
                downloadable_files.append({
                    'filename': video['filename'],
                    'download_url': f"/api/download-file/{job_id}/{video['filename']}",
                    'duration': video['duration'],
                    'theme': video['theme'],
                    'resolution': video['resolution']
                })
        
        return jsonify({
            'success': True,
            'files': downloadable_files,
            'output_directory': result['output_directory']
        })
        
    except Exception as e:
        logger.error(f"Error getting download info: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/download-file/<job_id>/<filename>', methods=['GET'])
def download_file(job_id: str, filename: str):
    """Download specific file endpoint"""
    try:
        if job_id not in processing_jobs:
            return jsonify({'error': 'Job not found'}), 404
        
        job = processing_jobs[job_id]
        
        if job['status'] != 'completed':
            return jsonify({'error': 'Job not completed yet'}), 400
        
        result = job['result']
        output_dir = result['output_directory']
        file_path = os.path.join(output_dir, filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(file_path, as_attachment=True, download_name=filename)
        
    except Exception as e:
        logger.error(f"Error downloading file: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/preview/<job_id>/<filename>', methods=['GET'])
def preview_file(job_id: str, filename: str):
    """Preview video file endpoint"""
    try:
        if job_id not in processing_jobs:
            return jsonify({'error': 'Job not found'}), 404
        
        job = processing_jobs[job_id]
        
        if job['status'] != 'completed':
            return jsonify({'error': 'Job not completed yet'}), 400
        
        result = job['result']
        output_dir = result['output_directory']
        file_path = os.path.join(output_dir, filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(file_path, mimetype='video/mp4')
        
    except Exception as e:
        logger.error(f"Error previewing file: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/jobs', methods=['GET'])
def list_jobs():
    """List all processing jobs endpoint"""
    try:
        jobs_summary = []
        
        for job_id, job_data in processing_jobs.items():
            summary = {
                'job_id': job_id,
                'status': job_data['status'],
                'progress': job_data['progress'],
                'start_time': job_data['start_time'].isoformat(),
                'config': {
                    'platform': job_data['config'].get('platform'),
                    'max_segments': job_data['config'].get('max_segments'),
                    'theme': job_data['config'].get('theme')
                }
            }
            
            if 'end_time' in job_data:
                summary['end_time'] = job_data['end_time'].isoformat()
            
            if job_data['status'] == 'completed' and job_data.get('result'):
                summary['video_count'] = len(job_data['result'].get('final_videos', []))
            
            jobs_summary.append(summary)
        
        return jsonify({
            'success': True,
            'jobs': jobs_summary,
            'total_jobs': len(jobs_summary)
        })
        
    except Exception as e:
        logger.error(f"Error listing jobs: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/cleanup/<job_id>', methods=['DELETE'])
def cleanup_job(job_id: str):
    """Cleanup job data endpoint"""
    try:
        if job_id not in processing_jobs:
            return jsonify({'error': 'Job not found'}), 404
        
        job = processing_jobs[job_id]
        
        # Remove output files
        if job.get('result') and 'output_directory' in job['result']:
            output_dir = job['result']['output_directory']
            if os.path.exists(output_dir):
                import shutil
                shutil.rmtree(output_dir)
        
        # Remove job from memory
        del processing_jobs[job_id]
        
        return jsonify({
            'success': True,
            'message': 'Job cleaned up successfully'
        })
        
    except Exception as e:
        logger.error(f"Error cleaning up job: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info("Starting TikTub Studio Flask Server")
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True
    )