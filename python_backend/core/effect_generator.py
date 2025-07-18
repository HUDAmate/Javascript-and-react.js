import cv2
import numpy as np
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ColorClip, ImageClip
from moviepy.video.fx import resize, fadein, fadeout, speedx, colorx, lum_contrast
from moviepy.video.tools.drawing import circle
import torch
from transformers import pipeline, BlipProcessor, BlipForConditionalGeneration
from keybert import KeyBERT
import logging
from typing import List, Dict, Tuple, Optional
import colorsys
import random
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont
import json
import math
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EffectGenerator:
    """
    Enhanced AI-powered effect generator untuk menciptakan efek video yang sophisticated
    dengan analisis konten otomatis dan efek yang responsif terhadap tema video
    """
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Initialize models for content analysis
        try:
            self.image_captioning_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
            self.image_captioning_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        except:
            logger.warning("BLIP model tidak tersedia, menggunakan analisis basic")
            self.image_captioning_processor = None
            self.image_captioning_model = None
        
        # Initialize keyword extraction
        self.keyword_extractor = KeyBERT()
        
        # Enhanced effect templates dengan AI-driven customization
        self.effect_templates = {
            'energetic': {
                'transitions': {
                    'quick_zoom': {'duration': 0.3, 'intensity': 1.2},
                    'fast_cut': {'duration': 0.1, 'intensity': 1.0},
                    'shake': {'duration': 0.2, 'intensity': 5},
                    'flash': {'duration': 0.15, 'intensity': 0.8},
                    'spin': {'duration': 0.4, 'intensity': 180}
                },
                'color_grading': {
                    'saturation': 1.3,
                    'contrast': 1.2,
                    'warmth': 1.1,
                    'vibrancy': 1.25
                },
                'text_style': {
                    'font_family': 'Arial Black',
                    'animation': 'bounce_in',
                    'color_scheme': ['#FF1744', '#FF6B35', '#F7931E'],
                    'stroke_width': 3,
                    'shadow': True
                },
                'audio_sync': True,
                'beat_detection': True
            },
            'calm': {
                'transitions': {
                    'fade': {'duration': 1.0, 'intensity': 0.8},
                    'slow_zoom': {'duration': 2.0, 'intensity': 1.05},
                    'gentle_pan': {'duration': 1.5, 'intensity': 0.1},
                    'dissolve': {'duration': 1.2, 'intensity': 0.9}
                },
                'color_grading': {
                    'saturation': 0.85,
                    'contrast': 0.95,
                    'warmth': 0.9,
                    'softness': 1.1
                },
                'text_style': {
                    'font_family': 'Georgia',
                    'animation': 'fade_in',
                    'color_scheme': ['#2E7D32', '#388E3C', '#43A047'],
                    'stroke_width': 1,
                    'shadow': False
                },
                'audio_sync': False,
                'beat_detection': False
            },
            'educational': {
                'transitions': {
                    'clean_cut': {'duration': 0.2, 'intensity': 1.0},
                    'smooth_fade': {'duration': 0.5, 'intensity': 1.0},
                    'highlight': {'duration': 0.3, 'intensity': 1.1},
                    'slide_in': {'duration': 0.4, 'intensity': 1.0}
                },
                'color_grading': {
                    'saturation': 1.0,
                    'contrast': 1.05,
                    'clarity': 1.1,
                    'professional': True
                },
                'text_style': {
                    'font_family': 'Open Sans',
                    'animation': 'slide_up',
                    'color_scheme': ['#1976D2', '#1565C0', '#0D47A1'],
                    'stroke_width': 2,
                    'shadow': True
                },
                'audio_sync': False,
                'beat_detection': False
            },
            'entertainment': {
                'transitions': {
                    'creative_cut': {'duration': 0.25, 'intensity': 1.1},
                    'bounce': {'duration': 0.5, 'intensity': 1.3},
                    'slide': {'duration': 0.3, 'intensity': 1.0},
                    'glitch': {'duration': 0.1, 'intensity': 0.7},
                    'zoom_blur': {'duration': 0.4, 'intensity': 1.15}
                },
                'color_grading': {
                    'saturation': 1.15,
                    'contrast': 1.1,
                    'vibrancy': 1.2,
                    'fun_filter': True
                },
                'text_style': {
                    'font_family': 'Comic Sans MS',
                    'animation': 'pop_in',
                    'color_scheme': ['#E91E63', '#9C27B0', '#673AB7'],
                    'stroke_width': 4,
                    'shadow': True
                },
                'audio_sync': True,
                'beat_detection': True
            },
            'dramatic': {
                'transitions': {
                    'dramatic_zoom': {'duration': 1.5, 'intensity': 1.4},
                    'slow_motion': {'duration': 2.0, 'intensity': 0.5},
                    'fade_to_black': {'duration': 1.0, 'intensity': 1.0},
                    'lens_flare': {'duration': 0.8, 'intensity': 1.2}
                },
                'color_grading': {
                    'saturation': 0.8,
                    'contrast': 1.3,
                    'shadows': 1.2,
                    'highlights': 0.9,
                    'cinematic': True
                },
                'text_style': {
                    'font_family': 'Times New Roman',
                    'animation': 'dramatic_reveal',
                    'color_scheme': ['#8BC34A', '#689F38', '#558B2F'],
                    'stroke_width': 2,
                    'shadow': True
                },
                'audio_sync': False,
                'beat_detection': False
            }
        }
        
        # Advanced animation presets
        self.animation_presets = {
            'bounce_in': self._create_bounce_animation,
            'fade_in': self._create_fade_animation,
            'slide_up': self._create_slide_animation,
            'pop_in': self._create_pop_animation,
            'dramatic_reveal': self._create_dramatic_animation,
            'typewriter': self._create_typewriter_animation,
            'neon_glow': self._create_neon_animation
        }

    def generate_effects(self, video_clip: VideoFileClip, theme: str, 
                        subtitle_data: Optional[Dict] = None, 
                        custom_config: Optional[Dict] = None) -> VideoFileClip:
        """
        Generate comprehensive effects untuk video berdasarkan tema dan analisis AI
        
        Args:
            video_clip: VideoFileClip yang akan diproses
            theme: Tema efek ('energetic', 'calm', 'educational', 'entertainment', 'dramatic')
            subtitle_data: Data subtitle untuk sinkronisasi teks
            custom_config: Konfigurasi custom untuk override default
        
        Returns:
            VideoFileClip dengan efek yang telah diterapkan
        """
        try:
            logger.info(f"Menerapkan efek tema '{theme}' dengan AI enhancement")
            
            # Get theme configuration
            config = self.effect_templates.get(theme, self.effect_templates['educational'])
            if custom_config:
                config = self._merge_configs(config, custom_config)
            
            # Analyze video content untuk adaptive effects
            content_analysis = self._analyze_video_content(video_clip)
            
            # Apply color grading
            enhanced_clip = self._apply_color_grading(video_clip, config['color_grading'], content_analysis)
            
            # Apply transitions and effects
            enhanced_clip = self._apply_dynamic_transitions(enhanced_clip, config['transitions'], content_analysis)
            
            # Apply visual effects
            enhanced_clip = self._apply_visual_effects(enhanced_clip, theme, content_analysis)
            
            # Add animated text/subtitles
            if subtitle_data:
                enhanced_clip = self._add_animated_subtitles(
                    enhanced_clip, subtitle_data, config['text_style'], theme
                )
            
            # Add theme-specific overlays
            enhanced_clip = self._add_theme_overlays(enhanced_clip, theme, content_analysis)
            
            # Final polish effects
            enhanced_clip = self._apply_final_polish(enhanced_clip, theme)
            
            logger.info("Efek berhasil diterapkan dengan AI optimization")
            return enhanced_clip
            
        except Exception as e:
            logger.error(f"Error dalam generate effects: {str(e)}")
            return video_clip

    def _analyze_video_content(self, video_clip: VideoFileClip) -> Dict:
        """
        Analisis mendalam konten video untuk adaptive effects
        """
        analysis = {
            'dominant_colors': [],
            'brightness_level': 0.5,
            'motion_intensity': 0.5,
            'scene_types': [],
            'color_temperature': 'neutral',
            'composition_style': 'balanced'
        }
        
        try:
            # Sample beberapa frame untuk analisis
            duration = video_clip.duration
            sample_times = np.linspace(1, duration-1, min(10, int(duration)))
            
            frames_analysis = []
            
            for t in sample_times:
                frame = video_clip.get_frame(t)
                frame_analysis = self._analyze_single_frame(frame)
                frames_analysis.append(frame_analysis)
            
            # Aggregate analysis results
            analysis['dominant_colors'] = self._get_dominant_colors(frames_analysis)
            analysis['brightness_level'] = np.mean([f['brightness'] for f in frames_analysis])
            analysis['color_temperature'] = self._determine_color_temperature(frames_analysis)
            analysis['composition_style'] = self._analyze_composition(frames_analysis)
            
            # Motion analysis
            if duration > 2:
                analysis['motion_intensity'] = self._analyze_motion_intensity(video_clip)
            
        except Exception as e:
            logger.warning(f"Error dalam content analysis: {e}")
            
        return analysis

    def _analyze_single_frame(self, frame: np.ndarray) -> Dict:
        """
        Analisis detail single frame
        """
        # Convert to different color spaces
        frame_rgb = frame
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        frame_lab = cv2.cvtColor(frame, cv2.COLOR_RGB2LAB)
        
        # Brightness analysis
        brightness = np.mean(frame_lab[:, :, 0]) / 255.0
        
        # Color analysis
        colors = frame_rgb.reshape(-1, 3)
        dominant_colors = self._extract_dominant_colors(colors, k=5)
        
        # Composition analysis
        thirds_points = self._analyze_rule_of_thirds(frame_rgb)
        
        return {
            'brightness': brightness,
            'dominant_colors': dominant_colors,
            'composition_points': thirds_points,
            'saturation': np.mean(frame_hsv[:, :, 1]) / 255.0,
            'hue_distribution': np.histogram(frame_hsv[:, :, 0], bins=12)[0]
        }

    def _extract_dominant_colors(self, colors: np.ndarray, k: int = 5) -> List[Tuple[int, int, int]]:
        """
        Extract dominant colors menggunakan K-means
        """
        from sklearn.cluster import KMeans
        
        # Sample colors untuk efisiensi
        if len(colors) > 10000:
            indices = np.random.choice(len(colors), 10000, replace=False)
            colors = colors[indices]
        
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(colors)
        
        # Get cluster centers (dominant colors)
        dominant_colors = kmeans.cluster_centers_.astype(int)
        
        return [tuple(color) for color in dominant_colors]

    def _apply_color_grading(self, clip: VideoFileClip, grading_config: Dict, 
                           content_analysis: Dict) -> VideoFileClip:
        """
        Apply advanced color grading berdasarkan tema dan analisis konten
        """
        try:
            # Base color adjustments
            if 'saturation' in grading_config:
                clip = colorx(clip, grading_config['saturation'])
            
            if 'contrast' in grading_config:
                clip = lum_contrast(clip, contrast=grading_config['contrast'])
            
            # Adaptive adjustments berdasarkan analisis
            brightness = content_analysis.get('brightness_level', 0.5)
            
            # Auto-adjust exposure jika terlalu gelap atau terang
            if brightness < 0.3:
                clip = clip.fx(lambda c: c.multiply_volume(1.2))  # Brighten
            elif brightness > 0.8:
                clip = clip.fx(lambda c: c.multiply_volume(0.8))   # Darken
            
            # Apply cinematic grading untuk dramatic theme
            if grading_config.get('cinematic', False):
                clip = self._apply_cinematic_grading(clip, content_analysis)
            
            # Apply warmth/coolness
            if 'warmth' in grading_config:
                clip = self._apply_temperature_adjustment(clip, grading_config['warmth'])
            
            return clip
            
        except Exception as e:
            logger.warning(f"Error dalam color grading: {e}")
            return clip

    def _apply_cinematic_grading(self, clip: VideoFileClip, content_analysis: Dict) -> VideoFileClip:
        """
        Apply cinematic color grading dengan orange-teal look
        """
        def cinematic_filter(get_frame, t):
            frame = get_frame(t)
            
            # Convert to float
            frame_float = frame.astype(np.float32) / 255.0
            
            # Orange-teal color grading
            frame_float[:, :, 0] *= 1.1  # Boost reds
            frame_float[:, :, 1] *= 0.95 # Slightly reduce greens
            frame_float[:, :, 2] *= 0.9  # Reduce blues for orange tint
            
            # Add subtle vignette
            h, w = frame_float.shape[:2]
            Y, X = np.ogrid[:h, :w]
            center_x, center_y = w/2, h/2
            mask = ((X - center_x)**2 + (Y - center_y)**2) / (w*h/4)
            vignette = 1 - 0.3 * np.clip(mask, 0, 1)
            
            for i in range(3):
                frame_float[:, :, i] *= vignette
            
            return np.clip(frame_float * 255, 0, 255).astype(np.uint8)
        
        return clip.fl(cinematic_filter)

    def _apply_temperature_adjustment(self, clip: VideoFileClip, warmth: float) -> VideoFileClip:
        """
        Adjust color temperature (warmth/coolness)
        """
        def temperature_filter(get_frame, t):
            frame = get_frame(t)
            frame_float = frame.astype(np.float32)
            
            if warmth > 1.0:  # Warmer
                frame_float[:, :, 0] *= warmth  # Boost reds
                frame_float[:, :, 1] *= (1 + (warmth - 1) * 0.5)  # Slight green boost
                frame_float[:, :, 2] *= (1 / warmth)  # Reduce blues
            elif warmth < 1.0:  # Cooler
                frame_float[:, :, 0] *= warmth  # Reduce reds
                frame_float[:, :, 1] *= warmth  # Reduce greens
                frame_float[:, :, 2] *= (2 - warmth)  # Boost blues
            
            return np.clip(frame_float, 0, 255).astype(np.uint8)
        
        return clip.fl(temperature_filter)

    def _apply_dynamic_transitions(self, clip: VideoFileClip, transitions_config: Dict, 
                                 content_analysis: Dict) -> VideoFileClip:
        """
        Apply dynamic transitions berdasarkan content analysis
        """
        try:
            duration = clip.duration
            
            # Tentukan timing untuk transitions
            transition_points = self._calculate_transition_points(duration, content_analysis)
            
            clips = []
            prev_end = 0
            
            for i, point in enumerate(transition_points):
                start_time = prev_end
                end_time = min(point, duration)
                
                if end_time - start_time < 0.5:  # Skip jika segment terlalu pendek
                    continue
                
                segment = clip.subclip(start_time, end_time)
                
                # Pilih transition effect berdasarkan konten
                transition_type = self._select_transition_type(transitions_config, content_analysis, i)
                
                # Apply transition
                if transition_type in transitions_config:
                    segment = self._apply_transition_effect(segment, transition_type, transitions_config[transition_type])
                
                clips.append(segment)
                prev_end = end_time
            
            # Handle remaining segment
            if prev_end < duration:
                final_segment = clip.subclip(prev_end, duration)
                clips.append(final_segment)
            
            if clips:
                from moviepy.video.fx.all import concatenate_videoclips
                return concatenate_videoclips(clips)
            else:
                return clip
                
        except Exception as e:
            logger.warning(f"Error dalam dynamic transitions: {e}")
            return clip

    def _calculate_transition_points(self, duration: float, content_analysis: Dict) -> List[float]:
        """
        Calculate optimal transition points berdasarkan konten
        """
        motion_intensity = content_analysis.get('motion_intensity', 0.5)
        
        # Base transition interval berdasarkan motion
        if motion_intensity > 0.7:
            base_interval = 3.0  # Fast cuts untuk high motion
        elif motion_intensity > 0.4:
            base_interval = 5.0  # Medium cuts
        else:
            base_interval = 8.0  # Slow cuts untuk low motion
        
        points = []
        current = base_interval
        
        while current < duration - 1:
            # Add some randomness untuk natural feel
            variance = base_interval * 0.3
            next_point = current + random.uniform(-variance, variance)
            points.append(max(current, next_point))
            current += base_interval
        
        return points

    def _select_transition_type(self, transitions_config: Dict, content_analysis: Dict, index: int) -> str:
        """
        Select appropriate transition type berdasarkan konten dan posisi
        """
        brightness = content_analysis.get('brightness_level', 0.5)
        motion = content_analysis.get('motion_intensity', 0.5)
        
        available_transitions = list(transitions_config.keys())
        
        # Logic pemilihan transition
        if brightness > 0.7 and motion > 0.6:
            # Bright and active: quick transitions
            preferred = ['quick_zoom', 'fast_cut', 'flash']
        elif brightness < 0.4:
            # Dark scenes: smooth transitions
            preferred = ['fade', 'dissolve', 'slow_zoom']
        elif motion > 0.7:
            # High motion: energetic transitions
            preferred = ['shake', 'spin', 'bounce']
        else:
            # Default: balanced transitions
            preferred = ['smooth_fade', 'slide', 'clean_cut']
        
        # Filter available transitions
        suitable = [t for t in preferred if t in available_transitions]
        
        if suitable:
            return random.choice(suitable)
        else:
            return random.choice(available_transitions)

    def _apply_transition_effect(self, clip: VideoFileClip, transition_type: str, config: Dict) -> VideoFileClip:
        """
        Apply specific transition effect
        """
        duration = config.get('duration', 0.5)
        intensity = config.get('intensity', 1.0)
        
        try:
            if transition_type == 'quick_zoom':
                return self._apply_zoom_effect(clip, intensity, duration)
            elif transition_type == 'shake':
                return self._apply_shake_effect(clip, intensity, duration)
            elif transition_type == 'flash':
                return self._apply_flash_effect(clip, intensity, duration)
            elif transition_type == 'spin':
                return self._apply_spin_effect(clip, intensity, duration)
            elif transition_type == 'fade':
                return fadein(fadeout(clip, duration), duration)
            elif transition_type == 'slow_zoom':
                return self._apply_zoom_effect(clip, intensity, duration * 2)
            else:
                return clip
                
        except Exception as e:
            logger.warning(f"Error applying transition {transition_type}: {e}")
            return clip

    def _apply_zoom_effect(self, clip: VideoFileClip, intensity: float, duration: float) -> VideoFileClip:
        """
        Apply zoom effect dengan smooth animation
        """
        def zoom_function(t):
            progress = min(t / duration, 1.0)
            return 1.0 + (intensity - 1.0) * progress
        
        return resize(clip, zoom_function)

    def _apply_shake_effect(self, clip: VideoFileClip, intensity: float, duration: float) -> VideoFileClip:
        """
        Apply shake effect untuk dramatic moments
        """
        def shake_function(get_frame, t):
            if t < duration:
                shake_x = random.uniform(-intensity, intensity)
                shake_y = random.uniform(-intensity, intensity)
                frame = get_frame(t)
                
                # Simple translation untuk shake effect
                M = np.float32([[1, 0, shake_x], [0, 1, shake_y]])
                shaken_frame = cv2.warpAffine(frame, M, (frame.shape[1], frame.shape[0]))
                return shaken_frame
            else:
                return get_frame(t)
        
        return clip.fl(shake_function)

    def _apply_flash_effect(self, clip: VideoFileClip, intensity: float, duration: float) -> VideoFileClip:
        """
        Apply flash effect untuk highlight moments
        """
        def flash_function(get_frame, t):
            if t < duration:
                frame = get_frame(t)
                flash_strength = intensity * (1 - t / duration)  # Fade out flash
                
                # Add white overlay
                white_overlay = np.full_like(frame, 255, dtype=np.uint8)
                flashed_frame = cv2.addWeighted(frame, 1 - flash_strength, white_overlay, flash_strength, 0)
                
                return flashed_frame
            else:
                return get_frame(t)
        
        return clip.fl(flash_function)

    def _apply_spin_effect(self, clip: VideoFileClip, intensity: float, duration: float) -> VideoFileClip:
        """
        Apply subtle spin effect untuk dynamic feeling
        """
        def spin_function(get_frame, t):
            if t < duration:
                frame = get_frame(t)
                angle = intensity * (t / duration)  # Gradual rotation
                
                # Get frame center
                h, w = frame.shape[:2]
                center = (w // 2, h // 2)
                
                # Rotation matrix
                M = cv2.getRotationMatrix2D(center, angle, 1.0)
                rotated_frame = cv2.warpAffine(frame, M, (w, h))
                
                return rotated_frame
            else:
                return get_frame(t)
        
        return clip.fl(spin_function)

    def _add_animated_subtitles(self, clip: VideoFileClip, subtitle_data: Dict, 
                              text_style: Dict, theme: str) -> VideoFileClip:
        """
        Add animated subtitles dengan style yang sesuai tema
        """
        try:
            text_clips = []
            
            for subtitle in subtitle_data.get('segments', []):
                start_time = subtitle.get('start', 0)
                end_time = subtitle.get('end', start_time + 2)
                text = subtitle.get('text', '').strip()
                
                if not text or end_time <= start_time:
                    continue
                
                # Create animated text clip
                text_clip = self._create_animated_text(
                    text, end_time - start_time, text_style, theme
                ).set_start(start_time).set_duration(end_time - start_time)
                
                text_clips.append(text_clip)
            
            if text_clips:
                return CompositeVideoClip([clip] + text_clips)
            else:
                return clip
                
        except Exception as e:
            logger.warning(f"Error adding subtitles: {e}")
            return clip

    def _create_animated_text(self, text: str, duration: float, style: Dict, theme: str) -> TextClip:
        """
        Create advanced animated text dengan berbagai effects
        """
        # Text configuration
        font_family = style.get('font_family', 'Arial')
        animation_type = style.get('animation', 'fade_in')
        color_scheme = style.get('color_scheme', ['#FFFFFF'])
        stroke_width = style.get('stroke_width', 2)
        
        # Base text clip
        text_clip = TextClip(
            text,
            fontsize=50,
            font=font_family,
            color='white',
            stroke_color='black',
            stroke_width=stroke_width,
            method='caption',
            size=(1080, None)
        ).set_duration(duration)
        
        # Apply animation
        if animation_type in self.animation_presets:
            text_clip = self.animation_presets[animation_type](text_clip, duration, style)
        
        # Position text (bottom center untuk mobile format)
        text_clip = text_clip.set_position(('center', 'bottom')).set_margin(50)
        
        return text_clip

    def _create_bounce_animation(self, text_clip: TextClip, duration: float, style: Dict) -> TextClip:
        """
        Create bounce animation effect
        """
        def bounce_position(t):
            if t < 0.5:
                # Bounce in
                progress = t / 0.5
                y_offset = -100 * (1 - progress) ** 2
                return ('center', max(1920 - 200 + y_offset, 1920 - 200))
            else:
                return ('center', 1920 - 200)
        
        return text_clip.set_position(bounce_position)

    def _create_fade_animation(self, text_clip: TextClip, duration: float, style: Dict) -> TextClip:
        """
        Create smooth fade animation
        """
        fade_duration = min(0.5, duration / 4)
        return fadein(fadeout(text_clip, fade_duration), fade_duration)

    def _create_slide_animation(self, text_clip: TextClip, duration: float, style: Dict) -> TextClip:
        """
        Create slide up animation
        """
        def slide_position(t):
            if t < 0.3:
                progress = t / 0.3
                y_offset = 100 * (1 - progress)
                return ('center', 1920 - 200 + y_offset)
            else:
                return ('center', 1920 - 200)
        
        return text_clip.set_position(slide_position)

    def _create_pop_animation(self, text_clip: TextClip, duration: float, style: Dict) -> TextClip:
        """
        Create pop-in scale animation
        """
        def scale_function(t):
            if t < 0.2:
                return 0.1 + 0.9 * (t / 0.2)
            else:
                return 1.0
        
        return resize(text_clip, scale_function)

    def _create_dramatic_animation(self, text_clip: TextClip, duration: float, style: Dict) -> TextClip:
        """
        Create dramatic reveal animation
        """
        fade_clip = fadein(text_clip, min(1.0, duration / 2))
        return resize(fade_clip, lambda t: 0.8 + 0.2 * min(t / 0.5, 1.0))

    def _create_typewriter_animation(self, text_clip: TextClip, duration: float, style: Dict) -> TextClip:
        """
        Create typewriter effect (untuk educational theme)
        """
        # This would require more complex implementation
        # For now, return fade animation
        return self._create_fade_animation(text_clip, duration, style)

    def _create_neon_animation(self, text_clip: TextClip, duration: float, style: Dict) -> TextClip:
        """
        Create neon glow effect
        """
        # Add glow effect (simplified)
        return fadein(text_clip, 0.2)

    def _add_theme_overlays(self, clip: VideoFileClip, theme: str, content_analysis: Dict) -> VideoFileClip:
        """
        Add theme-specific overlays dan particles
        """
        try:
            if theme == 'energetic':
                return self._add_energy_particles(clip)
            elif theme == 'dramatic':
                return self._add_cinematic_bars(clip)
            elif theme == 'entertainment':
                return self._add_fun_elements(clip)
            else:
                return clip
                
        except Exception as e:
            logger.warning(f"Error adding theme overlays: {e}")
            return clip

    def _add_energy_particles(self, clip: VideoFileClip) -> VideoFileClip:
        """
        Add energy particles untuk energetic theme
        """
        # Create simple particle overlay
        def create_particles(get_frame, t):
            frame = get_frame(t)
            
            # Add random bright pixels untuk spark effect
            if random.random() < 0.3:  # 30% chance per frame
                for _ in range(5):
                    x = random.randint(0, frame.shape[1] - 1)
                    y = random.randint(0, frame.shape[0] - 1)
                    frame[y, x] = [255, 255, 255]  # White spark
            
            return frame
        
        return clip.fl(create_particles)

    def _add_cinematic_bars(self, clip: VideoFileClip) -> VideoFileClip:
        """
        Add cinematic black bars untuk dramatic theme
        """
        def add_bars(get_frame, t):
            frame = get_frame(t)
            h, w = frame.shape[:2]
            
            # Add top and bottom black bars (cinematic aspect ratio)
            bar_height = int(h * 0.1)
            frame[:bar_height, :] = [0, 0, 0]
            frame[-bar_height:, :] = [0, 0, 0]
            
            return frame
        
        return clip.fl(add_bars)

    def _add_fun_elements(self, clip: VideoFileClip) -> VideoFileClip:
        """
        Add fun elements untuk entertainment theme
        """
        # Add subtle color shifts
        def fun_filter(get_frame, t):
            frame = get_frame(t)
            
            # Slight color cycling
            shift = int(10 * math.sin(t * 2))
            if shift != 0:
                frame_shifted = np.roll(frame, shift, axis=2)
                frame = cv2.addWeighted(frame, 0.9, frame_shifted, 0.1, 0)
            
            return frame
        
        return clip.fl(fun_filter)

    def _apply_final_polish(self, clip: VideoFileClip, theme: str) -> VideoFileClip:
        """
        Apply final polish effects untuk overall quality enhancement
        """
        try:
            # Subtle sharpening
            def sharpen_filter(get_frame, t):
                frame = get_frame(t)
                
                # Unsharp mask untuk sharpening
                gaussian = cv2.GaussianBlur(frame, (0, 0), 2.0)
                sharpened = cv2.addWeighted(frame, 1.5, gaussian, -0.5, 0)
                
                return np.clip(sharpened, 0, 255).astype(np.uint8)
            
            # Apply sharpening untuk themes yang membutuhkan clarity
            if theme in ['educational', 'entertainment']:
                clip = clip.fl(sharpen_filter)
            
            return clip
            
        except Exception as e:
            logger.warning(f"Error dalam final polish: {e}")
            return clip

    def _analyze_motion_intensity(self, clip: VideoFileClip) -> float:
        """
        Analyze motion intensity dalam video
        """
        try:
            # Sample beberapa frame pairs
            duration = clip.duration
            sample_times = np.linspace(1, duration-1, min(5, int(duration-1)))
            
            motion_scores = []
            
            for i in range(len(sample_times) - 1):
                frame1 = clip.get_frame(sample_times[i])
                frame2 = clip.get_frame(sample_times[i + 1])
                
                # Convert to grayscale
                gray1 = cv2.cvtColor(frame1, cv2.COLOR_RGB2GRAY)
                gray2 = cv2.cvtColor(frame2, cv2.COLOR_RGB2GRAY)
                
                # Calculate optical flow magnitude
                flow = cv2.calcOpticalFlowPyrLK(gray1, gray2, None, None)
                if flow[0] is not None:
                    motion_magnitude = np.mean(np.abs(flow[0] - flow[1]))
                    motion_scores.append(motion_magnitude)
            
            return np.mean(motion_scores) / 50.0 if motion_scores else 0.5
            
        except Exception as e:
            logger.warning(f"Error analyzing motion: {e}")
            return 0.5

    def _get_dominant_colors(self, frames_analysis: List[Dict]) -> List[Tuple[int, int, int]]:
        """
        Get overall dominant colors dari multiple frames
        """
        all_colors = []
        for frame_analysis in frames_analysis:
            all_colors.extend(frame_analysis.get('dominant_colors', []))
        
        if not all_colors:
            return [(128, 128, 128)]  # Default gray
        
        # Cluster colors untuk mendapat dominan colors
        return self._extract_dominant_colors(np.array(all_colors), k=3)

    def _determine_color_temperature(self, frames_analysis: List[Dict]) -> str:
        """
        Determine overall color temperature dari frames
        """
        total_warmth = 0
        
        for frame_analysis in frames_analysis:
            colors = frame_analysis.get('dominant_colors', [])
            for r, g, b in colors:
                if r > b:  # More red than blue = warm
                    total_warmth += 1
                elif b > r:  # More blue than red = cool
                    total_warmth -= 1
        
        if total_warmth > 0:
            return 'warm'
        elif total_warmth < 0:
            return 'cool'
        else:
            return 'neutral'

    def _analyze_composition(self, frames_analysis: List[Dict]) -> str:
        """
        Analyze overall composition style
        """
        # Simplified composition analysis
        # In a real implementation, this would analyze rule of thirds, symmetry, etc.
        return 'balanced'

    def _analyze_rule_of_thirds(self, frame: np.ndarray) -> Dict:
        """
        Analyze rule of thirds composition
        """
        h, w = frame.shape[:2]
        
        # Rule of thirds grid points
        third_x = w // 3
        third_y = h // 3
        
        points = {
            'top_left': frame[third_y, third_x],
            'top_right': frame[third_y, 2 * third_x],
            'bottom_left': frame[2 * third_y, third_x],
            'bottom_right': frame[2 * third_y, 2 * third_x]
        }
        
        return points

    def _merge_configs(self, base_config: Dict, custom_config: Dict) -> Dict:
        """
        Merge custom configuration dengan base configuration
        """
        merged = base_config.copy()
        
        for key, value in custom_config.items():
            if isinstance(value, dict) and key in merged:
                merged[key].update(value)
            else:
                merged[key] = value
        
        return merged