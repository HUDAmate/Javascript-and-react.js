import cv2
import numpy as np
from moviepy.editor import VideoFileClip, CompositeVideoClip, ColorClip
import logging

logger = logging.getLogger(__name__)

class EffectEngine:
    def __init__(self):
        self.effect_templates = {
            'entertainment': {
                'type': 'entertainment',
                'zoom_intensity': 0.15,
                'color_boost': 1.2,
                'transition_style': 'dynamic',
                'motion_blur': False
            },
            'educational': {
                'type': 'educational',
                'zoom_intensity': 0.05,
                'color_boost': 1.05,
                'transition_style': 'smooth',
                'motion_blur': False
            },
            'music': {
                'type': 'music',
                'zoom_intensity': 0.2,
                'color_boost': 1.3,
                'transition_style': 'beat_sync',
                'motion_blur': True
            },
            'gaming': {
                'type': 'gaming',
                'zoom_intensity': 0.25,
                'color_boost': 1.4,
                'transition_style': 'glitch',
                'motion_blur': False
            },
            'lifestyle': {
                'type': 'lifestyle',
                'zoom_intensity': 0.08,
                'color_boost': 1.15,
                'transition_style': 'gentle',
                'motion_blur': False
            },
            'news': {
                'type': 'news',
                'zoom_intensity': 0.02,
                'color_boost': 1.0,
                'transition_style': 'fade',
                'motion_blur': False
            }
        }
    
    def get_theme_effects(self, theme):
        """Get effect configuration for a specific theme"""
        return self.effect_templates.get(theme, self.effect_templates['entertainment'])
    
    def apply_entertainment_effects(self, clip):
        """Apply entertainment-focused effects"""
        try:
            # Dynamic zoom effect
            def zoom_effect(get_frame, t):
                frame = get_frame(t)
                zoom_factor = 1 + 0.1 * np.sin(4 * np.pi * t / clip.duration)
                return self._apply_zoom_to_frame(frame, zoom_factor)
            
            zoomed_clip = clip.fl(zoom_effect, apply_to=[])
            
            # Color enhancement
            def color_pop(get_frame, t):
                frame = get_frame(t)
                return self._enhance_colors(frame, saturation_boost=1.3, brightness_boost=1.1)
            
            final_clip = zoomed_clip.fl(color_pop, apply_to=[])
            
            return final_clip
        
        except Exception as e:
            logger.error(f"Error applying entertainment effects: {str(e)}")
            return clip
    
    def apply_educational_effects(self, clip):
        """Apply educational-focused effects"""
        try:
            # Subtle brightness and contrast enhancement
            def enhance_clarity(get_frame, t):
                frame = get_frame(t)
                # Improve contrast and brightness for clarity
                enhanced = cv2.convertScaleAbs(frame, alpha=1.1, beta=10)
                return enhanced
            
            enhanced_clip = clip.fl(enhance_clarity, apply_to=[])
            
            # Add subtle vignette for focus
            def add_vignette(get_frame, t):
                frame = get_frame(t)
                return self._add_vignette(frame, intensity=0.3)
            
            final_clip = enhanced_clip.fl(add_vignette, apply_to=[])
            
            return final_clip
        
        except Exception as e:
            logger.error(f"Error applying educational effects: {str(e)}")
            return clip
    
    def apply_music_effects(self, clip):
        """Apply music-focused effects"""
        try:
            # Rhythmic zoom based on time
            def music_zoom(get_frame, t):
                frame = get_frame(t)
                # Create a beat-like zoom effect
                beat_factor = 1 + 0.15 * abs(np.sin(8 * np.pi * t / clip.duration))
                return self._apply_zoom_to_frame(frame, beat_factor)
            
            zoomed_clip = clip.fl(music_zoom, apply_to=[])
            
            # Add color pulse effect
            def color_pulse(get_frame, t):
                frame = get_frame(t)
                pulse_intensity = 1 + 0.2 * np.sin(6 * np.pi * t / clip.duration)
                return self._enhance_colors(frame, saturation_boost=pulse_intensity)
            
            final_clip = zoomed_clip.fl(color_pulse, apply_to=[])
            
            return final_clip
        
        except Exception as e:
            logger.error(f"Error applying music effects: {str(e)}")
            return clip
    
    def apply_gaming_effects(self, clip):
        """Apply gaming-focused effects"""
        try:
            # High contrast and saturation
            def gaming_enhance(get_frame, t):
                frame = get_frame(t)
                # Boost contrast and saturation for gaming aesthetics
                enhanced = self._enhance_colors(frame, saturation_boost=1.5, contrast_boost=1.3)
                return enhanced
            
            enhanced_clip = clip.fl(gaming_enhance, apply_to=[])
            
            # Add slight glitch effect occasionally
            def glitch_effect(get_frame, t):
                frame = get_frame(t)
                # Add glitch effect at certain intervals
                if int(t * 4) % 8 == 0:  # Glitch every 2 seconds
                    return self._add_glitch_effect(frame)
                return frame
            
            final_clip = enhanced_clip.fl(glitch_effect, apply_to=[])
            
            return final_clip
        
        except Exception as e:
            logger.error(f"Error applying gaming effects: {str(e)}")
            return clip
    
    def apply_lifestyle_effects(self, clip):
        """Apply lifestyle-focused effects"""
        try:
            # Warm color grading
            def warm_filter(get_frame, t):
                frame = get_frame(t)
                return self._apply_warm_tone(frame)
            
            warm_clip = clip.fl(warm_filter, apply_to=[])
            
            # Soft glow effect
            def soft_glow(get_frame, t):
                frame = get_frame(t)
                return self._add_soft_glow(frame)
            
            final_clip = warm_clip.fl(soft_glow, apply_to=[])
            
            return final_clip
        
        except Exception as e:
            logger.error(f"Error applying lifestyle effects: {str(e)}")
            return clip
    
    def apply_news_effects(self, clip):
        """Apply news/professional effects"""
        try:
            # Professional color correction
            def professional_grade(get_frame, t):
                frame = get_frame(t)
                # Neutral color grading with good contrast
                enhanced = cv2.convertScaleAbs(frame, alpha=1.05, beta=5)
                return enhanced
            
            professional_clip = clip.fl(professional_grade, apply_to=[])
            
            return professional_clip
        
        except Exception as e:
            logger.error(f"Error applying news effects: {str(e)}")
            return clip
    
    def _apply_zoom_to_frame(self, frame, zoom_factor):
        """Apply zoom effect to a single frame"""
        try:
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
        
        except Exception as e:
            logger.error(f"Error applying zoom: {str(e)}")
            return frame
    
    def _enhance_colors(self, frame, saturation_boost=1.2, brightness_boost=1.0, contrast_boost=1.0):
        """Enhance colors in a frame"""
        try:
            # Apply contrast and brightness
            if contrast_boost != 1.0 or brightness_boost != 1.0:
                frame = cv2.convertScaleAbs(frame, alpha=contrast_boost, beta=(brightness_boost - 1) * 50)
            
            # Apply saturation boost
            if saturation_boost != 1.0:
                hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV).astype(np.float32)
                hsv[:, :, 1] *= saturation_boost
                hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
                frame = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)
            
            return frame
        
        except Exception as e:
            logger.error(f"Error enhancing colors: {str(e)}")
            return frame
    
    def _add_vignette(self, frame, intensity=0.3):
        """Add vignette effect to frame"""
        try:
            h, w = frame.shape[:2]
            
            # Create vignette mask
            x = np.arange(w)
            y = np.arange(h)
            X, Y = np.meshgrid(x, y)
            
            center_x, center_y = w // 2, h // 2
            max_dist = np.sqrt((w // 2) ** 2 + (h // 2) ** 2)
            
            # Calculate distance from center
            dist = np.sqrt((X - center_x) ** 2 + (Y - center_y) ** 2)
            
            # Create vignette
            vignette = 1 - intensity * (dist / max_dist)
            vignette = np.clip(vignette, 0, 1)
            
            # Apply vignette
            if len(frame.shape) == 3:
                vignette = np.stack([vignette] * 3, axis=2)
            
            vignetted_frame = (frame * vignette).astype(np.uint8)
            
            return vignetted_frame
        
        except Exception as e:
            logger.error(f"Error adding vignette: {str(e)}")
            return frame
    
    def _add_glitch_effect(self, frame):
        """Add subtle glitch effect"""
        try:
            h, w = frame.shape[:2]
            glitched = frame.copy()
            
            # Random horizontal shifts
            for i in range(0, h, 20):
                if np.random.random() > 0.7:
                    shift = np.random.randint(-5, 6)
                    if shift > 0:
                        glitched[i:i+10, shift:] = frame[i:i+10, :-shift]
                    elif shift < 0:
                        glitched[i:i+10, :shift] = frame[i:i+10, -shift:]
            
            # Add color channel shift occasionally
            if np.random.random() > 0.8:
                glitched[:, :, 0] = np.roll(glitched[:, :, 0], 2, axis=1)  # Red channel shift
            
            return glitched
        
        except Exception as e:
            logger.error(f"Error adding glitch effect: {str(e)}")
            return frame
    
    def _apply_warm_tone(self, frame):
        """Apply warm color tone"""
        try:
            frame_float = frame.astype(np.float32)
            
            # Boost red and yellow tones
            frame_float[:, :, 0] *= 1.1  # Red
            frame_float[:, :, 1] *= 1.05  # Green
            frame_float[:, :, 2] *= 0.9  # Blue (reduce for warmth)
            
            return np.clip(frame_float, 0, 255).astype(np.uint8)
        
        except Exception as e:
            logger.error(f"Error applying warm tone: {str(e)}")
            return frame
    
    def _add_soft_glow(self, frame):
        """Add soft glow effect"""
        try:
            # Create a blurred version
            blurred = cv2.GaussianBlur(frame, (15, 15), 0)
            
            # Blend with original
            glow_frame = cv2.addWeighted(frame, 0.8, blurred, 0.2, 0)
            
            return glow_frame
        
        except Exception as e:
            logger.error(f"Error adding soft glow: {str(e)}")
            return frame
    
    def create_transition_effect(self, clip1, clip2, transition_type='fade', duration=0.5):
        """Create transition between two clips"""
        try:
            if transition_type == 'fade':
                return self._create_fade_transition(clip1, clip2, duration)
            elif transition_type == 'slide':
                return self._create_slide_transition(clip1, clip2, duration)
            elif transition_type == 'zoom':
                return self._create_zoom_transition(clip1, clip2, duration)
            else:
                # Default: simple concatenation
                return clip1.concatenate(clip2)
        
        except Exception as e:
            logger.error(f"Error creating transition: {str(e)}")
            return clip1.concatenate(clip2)
    
    def _create_fade_transition(self, clip1, clip2, duration):
        """Create fade transition"""
        try:
            # Fade out clip1
            clip1_faded = clip1.fadeout(duration)
            
            # Fade in clip2
            clip2_faded = clip2.fadein(duration)
            
            # Overlap the faded parts
            final_clip = CompositeVideoClip([
                clip1_faded,
                clip2_faded.set_start(clip1.duration - duration)
            ])
            
            return final_clip
        
        except Exception as e:
            logger.error(f"Error creating fade transition: {str(e)}")
            return clip1.concatenate(clip2)
    
    def _create_slide_transition(self, clip1, clip2, duration):
        """Create slide transition"""
        try:
            # This would require more complex implementation
            # For now, return simple concatenation
            return clip1.concatenate(clip2)
        
        except Exception as e:
            logger.error(f"Error creating slide transition: {str(e)}")
            return clip1.concatenate(clip2)
    
    def _create_zoom_transition(self, clip1, clip2, duration):
        """Create zoom transition"""
        try:
            # This would require more complex implementation
            # For now, return simple concatenation
            return clip1.concatenate(clip2)
        
        except Exception as e:
            logger.error(f"Error creating zoom transition: {str(e)}")
            return clip1.concatenate(clip2)