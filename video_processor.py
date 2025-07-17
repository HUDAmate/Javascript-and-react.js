import cv2
import ffmpeg
import numpy as np
import os
import tempfile
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class VideoProcessor:
    def __init__(self):
        self.supported_formats = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv']
    
    def get_video_info(self, video_path):
        """Get basic information about the video"""
        try:
            with VideoFileClip(video_path) as clip:
                return {
                    'duration': clip.duration,
                    'fps': clip.fps,
                    'size': clip.size,
                    'aspect_ratio': clip.size[0] / clip.size[1] if clip.size[1] != 0 else 1,
                    'audio': clip.audio is not None
                }
        except Exception as e:
            logger.error(f"Error getting video info: {str(e)}")
            raise
    
    def extract_segment(self, video_path, start_time, end_time):
        """Extract a segment from the video"""
        try:
            output_path = os.path.join('temp', f'segment_{int(datetime.now().timestamp())}.mp4')
            
            with VideoFileClip(video_path) as clip:
                segment = clip.subclip(start_time, end_time)
                segment.write_videofile(
                    output_path,
                    codec='libx264',
                    audio_codec='aac',
                    temp_audiofile='temp-audio.m4a',
                    remove_temp=True,
                    verbose=False,
                    logger=None
                )
            
            return output_path
        
        except Exception as e:
            logger.error(f"Error extracting segment: {str(e)}")
            raise
    
    def create_shorts_video(self, video_path, subtitles=None, effects=None, options=None):
        """Create a shorts video with specified effects and subtitles"""
        try:
            if options is None:
                options = {}
            
            output_path = os.path.join('outputs', f'shorts_{int(datetime.now().timestamp())}.mp4')
            
            with VideoFileClip(video_path) as main_clip:
                # Resize to shorts format (9:16 aspect ratio)
                target_width = 1080
                target_height = 1920
                
                # Calculate scaling to maintain aspect ratio
                video_aspect = main_clip.w / main_clip.h
                target_aspect = target_width / target_height
                
                if video_aspect > target_aspect:
                    # Video is wider, scale by height
                    new_height = target_height
                    new_width = int(main_clip.w * (target_height / main_clip.h))
                else:
                    # Video is taller, scale by width
                    new_width = target_width
                    new_height = int(main_clip.h * (target_width / main_clip.w))
                
                # Resize and center crop
                resized_clip = main_clip.resize((new_width, new_height))
                
                # Center crop to target dimensions
                x_center = new_width // 2
                y_center = new_height // 2
                x1 = max(0, x_center - target_width // 2)
                y1 = max(0, y_center - target_height // 2)
                x2 = min(new_width, x1 + target_width)
                y2 = min(new_height, y1 + target_height)
                
                cropped_clip = resized_clip.crop(x1=x1, y1=y1, x2=x2, y2=y2)
                
                # Apply effects if specified
                if effects:
                    cropped_clip = self._apply_effects(cropped_clip, effects, options)
                
                # Create composite with subtitles
                clips = [cropped_clip]
                
                if subtitles:
                    subtitle_clips = self._create_subtitle_clips(subtitles, cropped_clip.duration, options)
                    clips.extend(subtitle_clips)
                
                # Create final composite
                final_clip = CompositeVideoClip(clips, size=(target_width, target_height))
                
                # Write final video
                final_clip.write_videofile(
                    output_path,
                    codec='libx264',
                    audio_codec='aac',
                    bitrate='8000k',
                    temp_audiofile='temp-audio.m4a',
                    remove_temp=True,
                    verbose=False,
                    logger=None
                )
            
            return output_path
        
        except Exception as e:
            logger.error(f"Error creating shorts video: {str(e)}")
            raise
    
    def _apply_effects(self, clip, effects_config, options):
        """Apply visual effects based on theme"""
        try:
            effect_type = effects_config.get('type', 'none')
            
            if effect_type == 'entertainment':
                # Add zoom effect for entertainment
                clip = self._apply_zoom_effect(clip)
                clip = self._apply_color_enhancement(clip)
                
            elif effect_type == 'educational':
                # Clean and focused effects
                clip = self._apply_brightness_adjustment(clip, 1.1)
                clip = self._apply_contrast_adjustment(clip, 1.1)
                
            elif effect_type == 'music':
                # Music-synchronized effects would go here
                # For now, apply a subtle color pop
                clip = self._apply_color_pop(clip)
                
            elif effect_type == 'gaming':
                # High contrast, vibrant colors
                clip = self._apply_contrast_adjustment(clip, 1.3)
                clip = self._apply_saturation_boost(clip)
                
            elif effect_type == 'lifestyle':
                # Warm, aesthetic filters
                clip = self._apply_warm_filter(clip)
                
            elif effect_type == 'news':
                # Professional, clean look
                clip = self._apply_brightness_adjustment(clip, 1.05)
            
            return clip
        
        except Exception as e:
            logger.error(f"Error applying effects: {str(e)}")
            return clip
    
    def _apply_zoom_effect(self, clip):
        """Apply subtle zoom effect"""
        def zoom_func(get_frame, t):
            frame = get_frame(t)
            zoom_factor = 1 + 0.1 * np.sin(2 * np.pi * t / clip.duration)
            h, w = frame.shape[:2]
            center_x, center_y = w // 2, h // 2
            
            # Calculate new dimensions
            new_w, new_h = int(w * zoom_factor), int(h * zoom_factor)
            
            # Resize frame
            resized = cv2.resize(frame, (new_w, new_h))
            
            # Crop to original size
            start_x = max(0, (new_w - w) // 2)
            start_y = max(0, (new_h - h) // 2)
            
            if new_w >= w and new_h >= h:
                cropped = resized[start_y:start_y + h, start_x:start_x + w]
            else:
                # If zoomed out, pad the frame
                cropped = np.zeros_like(frame)
                end_y = min(h, new_h)
                end_x = min(w, new_w)
                cropped[:end_y, :end_x] = resized[:end_y, :end_x]
            
            return cropped
        
        return clip.fl(zoom_func, apply_to=[])
    
    def _apply_color_enhancement(self, clip):
        """Enhance colors for more vibrant look"""
        def color_enhance(get_frame, t):
            frame = get_frame(t)
            # Convert to HSV for better color manipulation
            hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV).astype(np.float32)
            hsv[:, :, 1] *= 1.2  # Increase saturation
            hsv[:, :, 2] *= 1.1  # Increase brightness
            hsv = np.clip(hsv, 0, 255).astype(np.uint8)
            return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
        
        return clip.fl(color_enhance, apply_to=[])
    
    def _apply_brightness_adjustment(self, clip, factor):
        """Adjust brightness"""
        def brightness_func(get_frame, t):
            frame = get_frame(t)
            return np.clip(frame * factor, 0, 255).astype(np.uint8)
        
        return clip.fl(brightness_func, apply_to=[])
    
    def _apply_contrast_adjustment(self, clip, factor):
        """Adjust contrast"""
        def contrast_func(get_frame, t):
            frame = get_frame(t)
            return np.clip((frame - 128) * factor + 128, 0, 255).astype(np.uint8)
        
        return clip.fl(contrast_func, apply_to=[])
    
    def _apply_color_pop(self, clip):
        """Apply color pop effect"""
        def color_pop(get_frame, t):
            frame = get_frame(t)
            hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV).astype(np.float32)
            hsv[:, :, 1] *= 1.3  # Boost saturation
            hsv = np.clip(hsv, 0, 255).astype(np.uint8)
            return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
        
        return clip.fl(color_pop, apply_to=[])
    
    def _apply_saturation_boost(self, clip):
        """Boost saturation for gaming content"""
        def saturation_boost(get_frame, t):
            frame = get_frame(t)
            hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV).astype(np.float32)
            hsv[:, :, 1] *= 1.4  # Strong saturation boost
            hsv = np.clip(hsv, 0, 255).astype(np.uint8)
            return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
        
        return clip.fl(saturation_boost, apply_to=[])
    
    def _apply_warm_filter(self, clip):
        """Apply warm filter for lifestyle content"""
        def warm_filter(get_frame, t):
            frame = get_frame(t).astype(np.float32)
            # Add warm tone by boosting red and reducing blue
            frame[:, :, 0] *= 1.1  # Red
            frame[:, :, 2] *= 0.9  # Blue
            return np.clip(frame, 0, 255).astype(np.uint8)
        
        return clip.fl(warm_filter, apply_to=[])
    
    def _create_subtitle_clips(self, subtitles, duration, options):
        """Create subtitle text clips"""
        subtitle_clips = []
        
        try:
            font_size = options.get('subtitle_font_size', 60)
            font_color = options.get('subtitle_color', 'white')
            stroke_color = options.get('subtitle_stroke_color', 'black')
            stroke_width = options.get('subtitle_stroke_width', 3)
            
            for subtitle in subtitles:
                start_time = subtitle['start']
                end_time = subtitle['end']
                text = subtitle['text']
                
                # Create text clip
                txt_clip = TextClip(
                    text,
                    fontsize=font_size,
                    color=font_color,
                    stroke_color=stroke_color,
                    stroke_width=stroke_width,
                    font='Arial-Bold',
                    method='caption',
                    size=(1000, None)
                ).set_start(start_time).set_end(end_time).set_position(('center', 1600))
                
                subtitle_clips.append(txt_clip)
        
        except Exception as e:
            logger.error(f"Error creating subtitle clips: {str(e)}")
        
        return subtitle_clips