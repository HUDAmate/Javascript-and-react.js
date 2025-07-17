import os
import json
import logging
from typing import List, Dict, Optional, Tuple
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, concatenate_videoclips
from moviepy.video.fx import speedx, fadein, fadeout
import tempfile
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

from .video_analyzer import VideoAnalyzer
from .subtitle_generator import SubtitleGenerator
from .effect_generator import EffectGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoProcessor:
    """
    Kelas utama untuk memproses video panjang menjadi short video
    dengan subtitle otomatis dan efek yang sesuai
    """
    
    def __init__(self):
        self.video_analyzer = VideoAnalyzer()
        self.subtitle_generator = SubtitleGenerator()
        self.effect_generator = EffectGenerator()
        
        # Configuration
        self.temp_dir = tempfile.mkdtemp()
        self.output_formats = ['mp4', 'mov']
        self.target_resolutions = {
            'tiktok': (1080, 1920),     # 9:16
            'youtube_shorts': (1080, 1920),  # 9:16
            'instagram_reels': (1080, 1920), # 9:16
            'custom': (1080, 1080)      # 1:1
        }
    
    def process_video(self, video_path: str, config: Dict) -> Dict:
        """
        Process video utama dengan semua fitur
        
        Args:
            video_path: Path ke video input
            config: Konfigurasi processing {
                'platform': 'tiktok|youtube_shorts|instagram_reels|custom',
                'max_segments': 5,
                'segment_duration': 60,
                'auto_effects': True,
                'theme': 'auto|energetic|calm|educational|entertainment|dramatic',
                'language': 'auto|id|en',
                'output_dir': 'path/to/output'
            }
        
        Returns:
            Dict dengan informasi hasil processing
        """
        try:
            logger.info(f"Starting video processing: {video_path}")
            
            # Validate input
            if not os.path.exists(video_path):
                raise FileNotFoundError(f"Video file not found: {video_path}")
            
            # Setup output directory
            output_dir = config.get('output_dir', './output')
            os.makedirs(output_dir, exist_ok=True)
            
            # Step 1: Analyze video
            logger.info("Step 1: Analyzing video content...")
            analysis_result = self.video_analyzer.analyze_video(video_path)
            
            # Step 2: Generate subtitles
            logger.info("Step 2: Generating subtitles...")
            subtitle_result = self.subtitle_generator.generate_subtitle(
                video_path, 
                config.get('language', 'auto')
            )
            
            # Step 3: Generate effects
            logger.info("Step 3: Generating effects...")
            effects_result = self.effect_generator.generate_effects(
                video_path,
                config.get('theme', 'auto'),
                subtitle_result
            )
            
            # Step 4: Create short video segments
            logger.info("Step 4: Creating short video segments...")
            segments_result = self._create_short_segments(
                video_path,
                analysis_result,
                subtitle_result,
                effects_result,
                config
            )
            
            # Step 5: Apply effects and render final videos
            logger.info("Step 5: Rendering final videos...")
            final_videos = self._render_final_videos(
                segments_result,
                config,
                output_dir
            )
            
            # Cleanup temp files
            self._cleanup()
            
            result = {
                'success': True,
                'original_video': video_path,
                'analysis': analysis_result,
                'subtitles': subtitle_result,
                'effects': effects_result,
                'segments': segments_result,
                'final_videos': final_videos,
                'output_directory': output_dir
            }
            
            logger.info("Video processing completed successfully!")
            return result
            
        except Exception as e:
            logger.error(f"Error processing video: {str(e)}")
            self._cleanup()
            raise
    
    def _create_short_segments(self, video_path: str, analysis_result: Dict,
                             subtitle_result: Dict, effects_result: Dict,
                             config: Dict) -> List[Dict]:
        """
        Create segmen-segmen short video berdasarkan analisis
        """
        best_segments = analysis_result['best_segments']
        max_segments = config.get('max_segments', 5)
        target_duration = config.get('segment_duration', 60)
        
        segments = []
        
        # Pilih segmen terbaik
        selected_segments = best_segments[:max_segments]
        
        for i, segment in enumerate(selected_segments):
            logger.info(f"Processing segment {i+1}/{len(selected_segments)}")
            
            # Extract segment dari video original
            segment_path = self._extract_video_segment(
                video_path,
                segment['start_time'],
                segment['end_time'],
                f"segment_{i+1}.mp4"
            )
            
            # Extract subtitle untuk segment ini
            segment_subtitles = self._extract_segment_subtitles(
                subtitle_result,
                segment['start_time'],
                segment['end_time']
            )
            
            # Adjust timing subtitle untuk segment
            adjusted_subtitles = self._adjust_subtitle_timing(
                segment_subtitles,
                segment['start_time']
            )
            
            segments.append({
                'id': i + 1,
                'video_path': segment_path,
                'start_time': segment['start_time'],
                'end_time': segment['end_time'],
                'duration': segment['duration'],
                'score': segment['score'],
                'confidence': segment['confidence'],
                'subtitles': adjusted_subtitles,
                'theme': effects_result['theme']
            })
        
        return segments
    
    def _extract_video_segment(self, video_path: str, start_time: float,
                             end_time: float, filename: str) -> str:
        """
        Extract segment dari video original
        """
        try:
            clip = VideoFileClip(video_path)
            segment_clip = clip.subclip(start_time, end_time)
            
            segment_path = os.path.join(self.temp_dir, filename)
            segment_clip.write_videofile(segment_path, codec='libx264', audio_codec='aac')
            
            clip.close()
            segment_clip.close()
            
            return segment_path
            
        except Exception as e:
            logger.error(f"Error extracting video segment: {str(e)}")
            raise
    
    def _extract_segment_subtitles(self, subtitle_result: Dict,
                                 start_time: float, end_time: float) -> List[Dict]:
        """
        Extract subtitle untuk segment tertentu
        """
        segment_subtitles = []
        
        for subtitle in subtitle_result['segments']:
            # Check jika subtitle berada dalam range segment
            if (subtitle['start'] >= start_time and subtitle['end'] <= end_time) or \
               (subtitle['start'] < end_time and subtitle['end'] > start_time):
                
                # Adjust timing jika subtitle terpotong
                adjusted_start = max(subtitle['start'], start_time)
                adjusted_end = min(subtitle['end'], end_time)
                
                if adjusted_end > adjusted_start:  # Pastikan valid
                    segment_subtitles.append({
                        'start': adjusted_start,
                        'end': adjusted_end,
                        'text': subtitle['text'],
                        'confidence': subtitle['confidence']
                    })
        
        return segment_subtitles
    
    def _adjust_subtitle_timing(self, subtitles: List[Dict], offset: float) -> List[Dict]:
        """
        Adjust timing subtitle relatif terhadap segment
        """
        adjusted_subtitles = []
        
        for subtitle in subtitles:
            adjusted_subtitles.append({
                'start': subtitle['start'] - offset,
                'end': subtitle['end'] - offset,
                'text': subtitle['text'],
                'confidence': subtitle['confidence']
            })
        
        return adjusted_subtitles
    
    def _render_final_videos(self, segments: List[Dict], config: Dict,
                           output_dir: str) -> List[Dict]:
        """
        Render video final dengan subtitle dan efek
        """
        platform = config.get('platform', 'tiktok')
        target_resolution = self.target_resolutions[platform]
        
        final_videos = []
        
        # Process each segment in parallel
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_to_segment = {
                executor.submit(
                    self._render_single_video,
                    segment,
                    target_resolution,
                    output_dir,
                    config
                ): segment for segment in segments
            }
            
            for future in as_completed(future_to_segment):
                segment = future_to_segment[future]
                try:
                    rendered_video = future.result()
                    final_videos.append(rendered_video)
                except Exception as e:
                    logger.error(f"Error rendering segment {segment['id']}: {str(e)}")
        
        # Sort berdasarkan ID
        final_videos.sort(key=lambda x: x['segment_id'])
        
        return final_videos
    
    def _render_single_video(self, segment: Dict, target_resolution: Tuple[int, int],
                           output_dir: str, config: Dict) -> Dict:
        """
        Render single video dengan subtitle dan efek
        """
        try:
            # Load video clip
            clip = VideoFileClip(segment['video_path'])
            
            # Resize untuk target platform
            clip = self._resize_for_platform(clip, target_resolution)
            
            # Add subtitle overlay
            if segment['subtitles']:
                clip = self._add_subtitle_overlay(clip, segment['subtitles'])
            
            # Apply effects jika enabled
            if config.get('auto_effects', True):
                clip = self._apply_segment_effects(clip, segment)
            
            # Generate output filename
            output_filename = f"short_video_{segment['id']}_{segment['theme']}.mp4"
            output_path = os.path.join(output_dir, output_filename)
            
            # Render final video
            clip.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                fps=30,
                preset='medium'
            )
            
            clip.close()
            
            # Generate metadata
            metadata = {
                'segment_id': segment['id'],
                'output_path': output_path,
                'filename': output_filename,
                'duration': segment['duration'],
                'theme': segment['theme'],
                'resolution': target_resolution,
                'subtitle_count': len(segment['subtitles']),
                'confidence_score': segment['confidence'],
                'quality_score': segment['score']
            }
            
            logger.info(f"Successfully rendered: {output_filename}")
            return metadata
            
        except Exception as e:
            logger.error(f"Error rendering single video: {str(e)}")
            raise
    
    def _resize_for_platform(self, clip: VideoFileClip,
                           target_resolution: Tuple[int, int]) -> VideoFileClip:
        """
        Resize video untuk platform target
        """
        target_width, target_height = target_resolution
        original_width, original_height = clip.size
        
        # Calculate scaling
        scale_width = target_width / original_width
        scale_height = target_height / original_height
        scale = max(scale_width, scale_height)  # Scale to fill
        
        # Resize dan crop
        resized_clip = clip.resize(scale)
        
        # Center crop
        if resized_clip.size[0] > target_width or resized_clip.size[1] > target_height:
            x_center = resized_clip.size[0] / 2
            y_center = resized_clip.size[1] / 2
            
            x1 = int(x_center - target_width / 2)
            y1 = int(y_center - target_height / 2)
            x2 = int(x_center + target_width / 2)
            y2 = int(y_center + target_height / 2)
            
            resized_clip = resized_clip.crop(x1=x1, y1=y1, x2=x2, y2=y2)
        
        return resized_clip
    
    def _add_subtitle_overlay(self, clip: VideoFileClip, subtitles: List[Dict]) -> VideoFileClip:
        """
        Add subtitle overlay ke video
        """
        subtitle_clips = []
        
        for subtitle in subtitles:
            # Create text clip
            txt_clip = TextClip(
                subtitle['text'],
                fontsize=50,
                color='white',
                font='Arial-Bold',
                stroke_color='black',
                stroke_width=2
            ).set_start(subtitle['start']).set_end(subtitle['end'])
            
            # Position subtitle
            txt_clip = txt_clip.set_position(('center', 'bottom')).set_margin(50)
            
            subtitle_clips.append(txt_clip)
        
        # Composite video dengan subtitle
        if subtitle_clips:
            final_clip = CompositeVideoClip([clip] + subtitle_clips)
            return final_clip
        
        return clip
    
    def _apply_segment_effects(self, clip: VideoFileClip, segment: Dict) -> VideoFileClip:
        """
        Apply efek ke segment video
        """
        # Simplified effect application
        # Dalam implementasi lengkap, ini akan menggunakan EffectGenerator
        
        theme = segment['theme']
        
        if theme == 'energetic':
            # Add slight speed up
            clip = clip.fx(speedx, 1.1)
        elif theme == 'calm':
            # Add fade in/out
            clip = clip.fx(fadein, 0.5).fx(fadeout, 0.5)
        
        return clip
    
    def _cleanup(self):
        """
        Cleanup temporary files
        """
        try:
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
        except Exception as e:
            logger.warning(f"Error cleaning up temp directory: {str(e)}")
    
    def get_processing_status(self, job_id: str) -> Dict:
        """
        Get status processing job (untuk future implementation)
        """
        # Placeholder untuk async processing status
        return {
            'job_id': job_id,
            'status': 'completed',
            'progress': 100
        }
    
    def export_project_data(self, result: Dict, output_path: str) -> str:
        """
        Export project data untuk future editing
        """
        try:
            project_data = {
                'version': '1.0',
                'timestamp': str(datetime.now()),
                'original_video': result['original_video'],
                'analysis': result['analysis'],
                'segments': result['segments'],
                'effects_config': result['effects']
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, indent=2, ensure_ascii=False)
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error exporting project data: {str(e)}")
            raise