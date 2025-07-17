import cv2
import numpy as np
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ColorClip
from moviepy.video.fx import resize, fadein, fadeout, speedx
import torch
from transformers import pipeline, BlipProcessor, BlipForConditionalGeneration
from keybert import KeyBERT
import logging
from typing import List, Dict, Tuple, Optional
import colorsys
import random
from PIL import Image, ImageFilter, ImageEnhance

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EffectGenerator:
    """
    Kelas untuk generate efek video yang sesuai dengan tema dan konten
    """
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Initialize models for content analysis
        self.image_captioning_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.image_captioning_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        
        # Initialize keyword extraction
        self.keyword_extractor = KeyBERT()
        
        # Define effect templates based on content themes
        self.effect_templates = {
            'energetic': {
                'transitions': ['quick_cuts', 'zoom_in', 'shake'],
                'colors': ['vibrant', 'high_contrast', 'saturated'],
                'text_style': 'bold_animated',
                'background_music_style': 'upbeat'
            },
            'calm': {
                'transitions': ['smooth_fade', 'slow_pan', 'gentle_zoom'],
                'colors': ['soft', 'pastel', 'low_contrast'],
                'text_style': 'elegant_fade',
                'background_music_style': 'ambient'
            },
            'educational': {
                'transitions': ['clean_cut', 'slide', 'highlight'],
                'colors': ['professional', 'blue_tones', 'clear'],
                'text_style': 'clear_readable',
                'background_music_style': 'neutral'
            },
            'entertainment': {
                'transitions': ['dynamic', 'bounce', 'spin'],
                'colors': ['colorful', 'bright', 'varied'],
                'text_style': 'playful_bounce',
                'background_music_style': 'fun'
            },
            'dramatic': {
                'transitions': ['dramatic_fade', 'slow_motion', 'cinematic'],
                'colors': ['dark', 'high_contrast', 'moody'],
                'text_style': 'dramatic_reveal',
                'background_music_style': 'cinematic'
            }
        }
    
    def generate_effects(self, video_path: str, theme: str = "auto", 
                        subtitle_data: Optional[Dict] = None) -> Dict:
        """
        Generate efek berdasarkan analisis konten dan tema
        """
        try:
            # Analyze content jika theme adalah auto
            if theme == "auto":
                theme = self._analyze_content_theme(video_path, subtitle_data)
            
            # Generate visual effects
            visual_effects = self._generate_visual_effects(video_path, theme)
            
            # Generate text effects for subtitles
            text_effects = self._generate_text_effects(theme, subtitle_data)
            
            # Generate color corrections
            color_effects = self._generate_color_effects(video_path, theme)
            
            # Generate transition effects
            transition_effects = self._generate_transition_effects(theme)
            
            return {
                'theme': theme,
                'visual_effects': visual_effects,
                'text_effects': text_effects,
                'color_effects': color_effects,
                'transition_effects': transition_effects,
                'recommended_music_style': self.effect_templates[theme]['background_music_style']
            }
            
        except Exception as e:
            logger.error(f"Error generating effects: {str(e)}")
            raise
    
    def _analyze_content_theme(self, video_path: str, subtitle_data: Optional[Dict] = None) -> str:
        """
        Analyze konten video untuk menentukan tema
        """
        try:
            # Analyze visual content
            visual_features = self._analyze_visual_features(video_path)
            
            # Analyze text content if available
            text_features = []
            if subtitle_data and 'segments' in subtitle_data:
                text_content = ' '.join([segment['text'] for segment in subtitle_data['segments']])
                text_features = self._analyze_text_features(text_content)
            
            # Determine theme based on features
            theme_scores = {
                'energetic': 0,
                'calm': 0,
                'educational': 0,
                'entertainment': 0,
                'dramatic': 0
            }
            
            # Score based on visual features
            if visual_features['motion_intensity'] > 0.7:
                theme_scores['energetic'] += 2
                theme_scores['entertainment'] += 1
            elif visual_features['motion_intensity'] < 0.3:
                theme_scores['calm'] += 2
                theme_scores['educational'] += 1
            
            if visual_features['color_variety'] > 0.8:
                theme_scores['entertainment'] += 2
                theme_scores['energetic'] += 1
            elif visual_features['color_variety'] < 0.4:
                theme_scores['dramatic'] += 1
                theme_scores['educational'] += 1
            
            if visual_features['brightness'] < 0.3:
                theme_scores['dramatic'] += 2
            elif visual_features['brightness'] > 0.7:
                theme_scores['energetic'] += 1
                theme_scores['entertainment'] += 1
            
            # Score based on text features
            for keyword, category in text_features:
                if category in ['education', 'learning', 'tutorial']:
                    theme_scores['educational'] += 2
                elif category in ['fun', 'funny', 'entertainment']:
                    theme_scores['entertainment'] += 2
                elif category in ['calm', 'peaceful', 'relax']:
                    theme_scores['calm'] += 2
                elif category in ['exciting', 'action', 'energy']:
                    theme_scores['energetic'] += 2
                elif category in ['serious', 'dramatic', 'emotional']:
                    theme_scores['dramatic'] += 2
            
            # Return theme with highest score
            best_theme = max(theme_scores.items(), key=lambda x: x[1])[0]
            logger.info(f"Detected theme: {best_theme} with scores: {theme_scores}")
            
            return best_theme
            
        except Exception as e:
            logger.error(f"Error analyzing content theme: {str(e)}")
            return 'educational'  # Default fallback
    
    def _analyze_visual_features(self, video_path: str) -> Dict:
        """
        Analyze visual features dari video
        """
        cap = cv2.VideoCapture(video_path)
        
        motion_scores = []
        brightness_scores = []
        color_variety_scores = []
        
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        # Sample frames
        sample_interval = max(1, int(fps))  # Sample every second
        prev_frame = None
        
        for i in range(0, frame_count, sample_interval):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            
            if not ret:
                break
            
            # Motion analysis
            if prev_frame is not None:
                motion_score = self._calculate_motion(prev_frame, frame)
                motion_scores.append(motion_score)
            
            # Brightness analysis
            brightness = np.mean(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)) / 255.0
            brightness_scores.append(brightness)
            
            # Color variety analysis
            color_variety = self._calculate_color_variety(frame)
            color_variety_scores.append(color_variety)
            
            prev_frame = frame
        
        cap.release()
        
        return {
            'motion_intensity': np.mean(motion_scores) if motion_scores else 0.5,
            'brightness': np.mean(brightness_scores) if brightness_scores else 0.5,
            'color_variety': np.mean(color_variety_scores) if color_variety_scores else 0.5
        }
    
    def _calculate_motion(self, prev_frame: np.ndarray, curr_frame: np.ndarray) -> float:
        """
        Calculate motion intensity between frames
        """
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate optical flow
        flow = cv2.calcOpticalFlowPyrLK(prev_gray, curr_gray, None, None)
        
        # Calculate motion magnitude
        diff = cv2.absdiff(prev_gray, curr_gray)
        motion_intensity = np.mean(diff) / 255.0
        
        return motion_intensity
    
    def _calculate_color_variety(self, frame: np.ndarray) -> float:
        """
        Calculate color variety dalam frame
        """
        # Convert to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Calculate histogram
        hist_h = cv2.calcHist([hsv], [0], None, [180], [0, 180])
        hist_s = cv2.calcHist([hsv], [1], None, [256], [0, 256])
        
        # Calculate variety based on histogram distribution
        h_variety = np.count_nonzero(hist_h) / 180.0
        s_variety = np.count_nonzero(hist_s) / 256.0
        
        return (h_variety + s_variety) / 2.0
    
    def _analyze_text_features(self, text: str) -> List[Tuple[str, str]]:
        """
        Analyze text untuk extract keywords dan kategori
        """
        try:
            # Extract keywords
            keywords = self.keyword_extractor.extract_keywords(text, keyphrase_ngram_range=(1, 2), 
                                                              stop_words='english', top_k=10)
            
            # Categorize keywords
            categorized_keywords = []
            for keyword, score in keywords:
                category = self._categorize_keyword(keyword.lower())
                categorized_keywords.append((keyword, category))
            
            return categorized_keywords
            
        except Exception as e:
            logger.error(f"Error analyzing text features: {str(e)}")
            return []
    
    def _categorize_keyword(self, keyword: str) -> str:
        """
        Categorize keyword berdasarkan context
        """
        education_words = ['learn', 'tutorial', 'how', 'guide', 'explain', 'teach', 'study', 'education']
        entertainment_words = ['fun', 'funny', 'laugh', 'entertainment', 'game', 'play', 'comedy']
        calm_words = ['calm', 'peaceful', 'relax', 'meditation', 'quiet', 'gentle', 'soft']
        energetic_words = ['energy', 'exciting', 'action', 'fast', 'quick', 'dynamic', 'power']
        dramatic_words = ['dramatic', 'serious', 'emotional', 'intense', 'deep', 'story']
        
        for word in education_words:
            if word in keyword:
                return 'education'
        for word in entertainment_words:
            if word in keyword:
                return 'entertainment'
        for word in calm_words:
            if word in keyword:
                return 'calm'
        for word in energetic_words:
            if word in keyword:
                return 'energy'
        for word in dramatic_words:
            if word in keyword:
                return 'dramatic'
        
        return 'neutral'
    
    def _generate_visual_effects(self, video_path: str, theme: str) -> Dict:
        """
        Generate visual effects berdasarkan tema
        """
        template = self.effect_templates[theme]
        
        effects = {
            'zoom_effects': [],
            'motion_effects': [],
            'filter_effects': [],
            'overlay_effects': []
        }
        
        # Zoom effects
        if 'zoom_in' in template['transitions']:
            effects['zoom_effects'].append({
                'type': 'zoom_in',
                'intensity': 1.2,
                'duration': 0.5
            })
        
        if 'gentle_zoom' in template['transitions']:
            effects['zoom_effects'].append({
                'type': 'gentle_zoom',
                'intensity': 1.05,
                'duration': 1.0
            })
        
        # Motion effects
        if 'shake' in template['transitions']:
            effects['motion_effects'].append({
                'type': 'shake',
                'intensity': 5,
                'frequency': 10
            })
        
        if 'bounce' in template['transitions']:
            effects['motion_effects'].append({
                'type': 'bounce',
                'intensity': 10,
                'frequency': 2
            })
        
        # Filter effects berdasarkan color style
        color_style = template['colors'][0] if template['colors'] else 'clear'
        
        if color_style == 'vibrant':
            effects['filter_effects'].append({
                'type': 'saturation',
                'value': 1.3
            })
        elif color_style == 'soft':
            effects['filter_effects'].append({
                'type': 'saturation',
                'value': 0.8
            })
        elif color_style == 'dark':
            effects['filter_effects'].append({
                'type': 'brightness',
                'value': 0.7
            })
        
        return effects
    
    def _generate_text_effects(self, theme: str, subtitle_data: Optional[Dict] = None) -> Dict:
        """
        Generate text effects untuk subtitle
        """
        template = self.effect_templates[theme]
        text_style = template['text_style']
        
        effects = {
            'animation': 'fade_in',
            'font_family': 'Arial',
            'font_size': 24,
            'color': '#FFFFFF',
            'outline_color': '#000000',
            'outline_width': 2,
            'shadow': True,
            'position': 'bottom_center'
        }
        
        if text_style == 'bold_animated':
            effects.update({
                'animation': 'bounce_in',
                'font_family': 'Arial Black',
                'font_size': 28,
                'color': '#FFFF00',
                'outline_width': 3
            })
        elif text_style == 'elegant_fade':
            effects.update({
                'animation': 'fade_in_slow',
                'font_family': 'Georgia',
                'font_size': 22,
                'color': '#F0F0F0'
            })
        elif text_style == 'clear_readable':
            effects.update({
                'animation': 'slide_up',
                'font_family': 'Helvetica',
                'font_size': 24,
                'color': '#FFFFFF',
                'background_color': 'rgba(0, 0, 0, 0.8)'
            })
        elif text_style == 'playful_bounce':
            effects.update({
                'animation': 'bounce_in',
                'font_family': 'Comic Sans MS',
                'font_size': 26,
                'color': '#FF6B6B',
                'outline_color': '#FFE66D'
            })
        elif text_style == 'dramatic_reveal':
            effects.update({
                'animation': 'typewriter',
                'font_family': 'Times New Roman',
                'font_size': 24,
                'color': '#CCCCCC',
                'outline_color': '#333333'
            })
        
        return effects
    
    def _generate_color_effects(self, video_path: str, theme: str) -> Dict:
        """
        Generate color correction effects
        """
        template = self.effect_templates[theme]
        color_styles = template['colors']
        
        effects = {
            'brightness': 1.0,
            'contrast': 1.0,
            'saturation': 1.0,
            'hue_shift': 0,
            'gamma': 1.0,
            'color_balance': {'red': 1.0, 'green': 1.0, 'blue': 1.0}
        }
        
        for style in color_styles:
            if style == 'vibrant':
                effects.update({
                    'saturation': 1.3,
                    'contrast': 1.2
                })
            elif style == 'soft':
                effects.update({
                    'saturation': 0.8,
                    'contrast': 0.9,
                    'brightness': 1.1
                })
            elif style == 'high_contrast':
                effects.update({
                    'contrast': 1.4,
                    'brightness': 0.95
                })
            elif style == 'dark':
                effects.update({
                    'brightness': 0.7,
                    'contrast': 1.3,
                    'saturation': 0.9
                })
            elif style == 'blue_tones':
                effects.update({
                    'color_balance': {'red': 0.9, 'green': 0.95, 'blue': 1.1}
                })
        
        return effects
    
    def _generate_transition_effects(self, theme: str) -> Dict:
        """
        Generate transition effects antar segment
        """
        template = self.effect_templates[theme]
        transitions = template['transitions']
        
        effects = {
            'type': 'fade',
            'duration': 0.5,
            'easing': 'ease_in_out'
        }
        
        if 'quick_cuts' in transitions:
            effects.update({
                'type': 'cut',
                'duration': 0.1
            })
        elif 'smooth_fade' in transitions:
            effects.update({
                'type': 'fade',
                'duration': 1.0,
                'easing': 'ease_in_out'
            })
        elif 'slide' in transitions:
            effects.update({
                'type': 'slide',
                'duration': 0.7,
                'direction': 'left'
            })
        elif 'dramatic_fade' in transitions:
            effects.update({
                'type': 'fade',
                'duration': 1.5,
                'easing': 'ease_in'
            })
        
        return effects
    
    def apply_effects_to_video(self, video_path: str, effects_config: Dict, 
                              output_path: str) -> str:
        """
        Apply generated effects ke video
        """
        try:
            clip = VideoFileClip(video_path)
            
            # Apply color effects
            clip = self._apply_color_effects(clip, effects_config['color_effects'])
            
            # Apply visual effects
            clip = self._apply_visual_effects(clip, effects_config['visual_effects'])
            
            # Save processed video
            clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
            clip.close()
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error applying effects to video: {str(e)}")
            raise
    
    def _apply_color_effects(self, clip: VideoFileClip, color_effects: Dict) -> VideoFileClip:
        """
        Apply color effects ke video clip
        """
        # This would typically use more sophisticated color grading
        # For now, we'll implement basic adjustments
        
        def color_adjust(get_frame, t):
            frame = get_frame(t)
            
            # Apply brightness
            if color_effects['brightness'] != 1.0:
                frame = frame * color_effects['brightness']
            
            # Apply contrast (simplified)
            if color_effects['contrast'] != 1.0:
                frame = (frame - 128) * color_effects['contrast'] + 128
            
            # Ensure values are in valid range
            frame = np.clip(frame, 0, 255).astype(np.uint8)
            
            return frame
        
        return clip.fl(color_adjust)
    
    def _apply_visual_effects(self, clip: VideoFileClip, visual_effects: Dict) -> VideoFileClip:
        """
        Apply visual effects ke video clip
        """
        # Apply zoom effects
        for zoom_effect in visual_effects.get('zoom_effects', []):
            if zoom_effect['type'] == 'zoom_in':
                clip = clip.resize(zoom_effect['intensity'])
        
        # Apply motion effects would be more complex
        # This is a simplified implementation
        
        return clip