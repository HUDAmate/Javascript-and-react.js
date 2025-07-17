import cv2
import numpy as np
import librosa
from moviepy.editor import VideoFileClip
from sklearn.cluster import KMeans
import logging

logger = logging.getLogger(__name__)

class SegmentAnalyzer:
    def __init__(self):
        self.segment_duration = 30  # Default target segment duration
        self.overlap_duration = 5   # Overlap between segments for scoring
    
    def analyze_segments(self, video_path, theme='general', target_duration=60):
        """Analyze video and suggest best segments based on theme"""
        try:
            segments = []
            
            with VideoFileClip(video_path) as clip:
                total_duration = clip.duration
                
                # Calculate segment parameters
                segment_size = min(target_duration, self.segment_duration)
                step_size = max(5, segment_size - self.overlap_duration)
                
                # Extract features for each potential segment
                potential_segments = []
                
                for start_time in np.arange(0, total_duration - segment_size, step_size):
                    end_time = min(start_time + segment_size, total_duration)
                    
                    # Extract features for this segment
                    features = self._extract_segment_features(clip, start_time, end_time, theme)
                    
                    potential_segments.append({
                        'start': start_time,
                        'end': end_time,
                        'duration': end_time - start_time,
                        'features': features,
                        'score': 0  # Will be calculated later
                    })
                
                # Score segments based on theme
                scored_segments = self._score_segments(potential_segments, theme)
                
                # Select top segments
                top_segments = sorted(scored_segments, key=lambda x: x['score'], reverse=True)[:5]
                
                # Format for frontend
                for i, segment in enumerate(top_segments):
                    segments.append({
                        'id': i,
                        'start': round(segment['start'], 2),
                        'end': round(segment['end'], 2),
                        'duration': round(segment['duration'], 2),
                        'score': round(segment['score'], 3),
                        'confidence': self._calculate_confidence(segment['features'], theme),
                        'description': self._generate_description(segment['features'], theme),
                        'thumbnail_time': round(segment['start'] + segment['duration'] / 2, 2)
                    })
            
            return segments
        
        except Exception as e:
            logger.error(f"Error analyzing segments: {str(e)}")
            return []
    
    def _extract_segment_features(self, clip, start_time, end_time, theme):
        """Extract features from a video segment"""
        features = {}
        
        try:
            # Extract subclip
            segment = clip.subclip(start_time, end_time)
            
            # Visual features
            visual_features = self._extract_visual_features(segment)
            features.update(visual_features)
            
            # Audio features
            if segment.audio:
                audio_features = self._extract_audio_features(segment)
                features.update(audio_features)
            
            # Motion features
            motion_features = self._extract_motion_features(segment)
            features.update(motion_features)
            
            # Theme-specific features (pass existing features)
            theme_features = self._extract_theme_features(features, theme)
            features.update(theme_features)
        
        except Exception as e:
            logger.error(f"Error extracting features: {str(e)}")
        
        return features
    
    def _extract_visual_features(self, segment):
        """Extract visual features like brightness, contrast, color distribution"""
        features = {}
        
        try:
            # Sample frames from the segment
            sample_times = np.linspace(0, segment.duration, min(10, int(segment.duration) + 1))
            frames = []
            
            for t in sample_times:
                if t < segment.duration:
                    frame = segment.get_frame(t)
                    frames.append(frame)
            
            if frames:
                frames = np.array(frames)
                
                # Average brightness
                features['brightness'] = np.mean(frames)
                
                # Contrast (standard deviation)
                features['contrast'] = np.std(frames)
                
                # Color distribution
                features['color_variance'] = np.var(frames, axis=(0, 1, 2))
                
                # Edge density (indicates detail/complexity)
                gray_frames = [cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY) for frame in frames]
                edges = [cv2.Canny(gray, 50, 150) for gray in gray_frames]
                features['edge_density'] = np.mean([np.sum(edge > 0) / edge.size for edge in edges])
                
                # Color saturation
                hsv_frames = [cv2.cvtColor(frame, cv2.COLOR_RGB2HSV) for frame in frames]
                features['saturation'] = np.mean([np.mean(hsv[:, :, 1]) for hsv in hsv_frames])
        
        except Exception as e:
            logger.error(f"Error extracting visual features: {str(e)}")
        
        return features
    
    def _extract_audio_features(self, segment):
        """Extract audio features like energy, tempo, spectral features"""
        features = {}
        
        try:
            # Extract audio as numpy array
            audio_array = segment.audio.to_soundarray(fps=22050)
            if len(audio_array.shape) > 1:
                audio_array = np.mean(audio_array, axis=1)  # Convert to mono
            
            # RMS energy
            features['audio_energy'] = np.sqrt(np.mean(audio_array ** 2))
            
            # Zero crossing rate (indicates speech vs music)
            features['zero_crossing_rate'] = np.mean(librosa.feature.zero_crossing_rate(audio_array))
            
            # Spectral centroid (brightness of sound)
            features['spectral_centroid'] = np.mean(librosa.feature.spectral_centroid(y=audio_array))
            
            # Tempo estimation
            tempo, _ = librosa.beat.beat_track(y=audio_array, sr=22050)
            features['tempo'] = tempo
            
            # Spectral rolloff
            features['spectral_rolloff'] = np.mean(librosa.feature.spectral_rolloff(y=audio_array))
            
            # Dynamic range
            features['dynamic_range'] = np.max(audio_array) - np.min(audio_array)
        
        except Exception as e:
            logger.error(f"Error extracting audio features: {str(e)}")
        
        return features
    
    def _extract_motion_features(self, segment):
        """Extract motion-related features"""
        features = {}
        
        try:
            # Sample frames for motion analysis
            if segment.duration > 1:
                sample_times = np.linspace(0, segment.duration - 0.1, min(20, int(segment.duration * 2)))
                motion_vectors = []
                
                prev_frame = None
                for t in sample_times:
                    if t < segment.duration:
                        frame = segment.get_frame(t)
                        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                        
                        if prev_frame is not None:
                            # Calculate optical flow
                            flow = cv2.calcOpticalFlowPyrLK(
                                prev_frame, gray,
                                np.array([[100, 100]], dtype=np.float32).reshape(-1, 1, 2),
                                None
                            )[0]
                            if flow is not None:
                                motion_vectors.append(np.linalg.norm(flow))
                        
                        prev_frame = gray
                
                if motion_vectors:
                    features['motion_intensity'] = np.mean(motion_vectors)
                    features['motion_variance'] = np.var(motion_vectors)
                else:
                    features['motion_intensity'] = 0
                    features['motion_variance'] = 0
            else:
                features['motion_intensity'] = 0
                features['motion_variance'] = 0
        
        except Exception as e:
            logger.error(f"Error extracting motion features: {str(e)}")
            features['motion_intensity'] = 0
            features['motion_variance'] = 0
        
        return features
    
    def _extract_theme_features(self, existing_features, theme):
        """Extract theme-specific features"""
        features = {}
        
        try:
            if theme == 'entertainment':
                # Look for dynamic content, faces, movement
                features['entertainment_score'] = (
                    existing_features.get('motion_intensity', 0) * 0.4 +
                    existing_features.get('audio_energy', 0) * 0.3 +
                    existing_features.get('color_variance', 0) * 0.3
                )
            
            elif theme == 'educational':
                # Look for stable content, clear audio, good contrast
                features['educational_score'] = (
                    existing_features.get('contrast', 0) * 0.3 +
                    (1 - existing_features.get('motion_intensity', 0)) * 0.3 +  # Less motion is better
                    existing_features.get('audio_energy', 0) * 0.4
                )
            
            elif theme == 'music':
                # Look for audio-heavy content, rhythm
                features['music_score'] = (
                    existing_features.get('audio_energy', 0) * 0.5 +
                    existing_features.get('tempo', 0) / 200.0 * 0.3 +  # Normalize tempo
                    existing_features.get('dynamic_range', 0) * 0.2
                )
            
            elif theme == 'gaming':
                # Look for high motion, bright colors, action
                features['gaming_score'] = (
                    existing_features.get('motion_intensity', 0) * 0.4 +
                    existing_features.get('saturation', 0) / 255.0 * 0.3 +
                    existing_features.get('edge_density', 0) * 0.3
                )
            
            elif theme == 'lifestyle':
                # Look for aesthetic content, balanced colors
                features['lifestyle_score'] = (
                    existing_features.get('saturation', 0) / 255.0 * 0.4 +
                    existing_features.get('brightness', 0) / 255.0 * 0.3 +
                    (1 - existing_features.get('motion_variance', 0)) * 0.3  # Smooth motion
                )
            
            elif theme == 'news':
                # Look for stable, clear content
                features['news_score'] = (
                    existing_features.get('contrast', 0) / 255.0 * 0.4 +
                    (1 - existing_features.get('motion_intensity', 0)) * 0.3 +
                    existing_features.get('audio_energy', 0) * 0.3
                )
        
        except Exception as e:
            logger.error(f"Error extracting theme features: {str(e)}")
        
        return features
    
    def _score_segments(self, segments, theme):
        """Score segments based on extracted features and theme"""
        for segment in segments:
            features = segment['features']
            
            # Base score from general quality metrics
            base_score = (
                features.get('contrast', 0) / 255.0 * 0.2 +
                features.get('audio_energy', 0) * 0.2 +
                features.get('brightness', 0) / 255.0 * 0.1 +
                features.get('saturation', 0) / 255.0 * 0.1
            )
            
            # Theme-specific score
            theme_score = features.get(f'{theme}_score', 0)
            
            # Duration bonus (prefer segments closer to target duration)
            duration_bonus = 1 - abs(segment['duration'] - self.segment_duration) / self.segment_duration
            duration_bonus = max(0, duration_bonus) * 0.1
            
            # Final score
            segment['score'] = base_score + theme_score + duration_bonus
        
        return segments
    
    def _calculate_confidence(self, features, theme):
        """Calculate confidence score for a segment"""
        try:
            # High confidence if features are strong and consistent
            feature_strength = sum([
                features.get('contrast', 0) / 255.0,
                features.get('audio_energy', 0),
                features.get('edge_density', 0)
            ]) / 3
            
            theme_strength = features.get(f'{theme}_score', 0)
            
            confidence = (feature_strength + theme_strength) / 2
            return min(1.0, max(0.0, confidence))
        
        except Exception as e:
            logger.error(f"Error calculating confidence: {str(e)}")
            return 0.5
    
    def _generate_description(self, features, theme):
        """Generate a description for the segment"""
        try:
            descriptions = []
            
            # Motion description
            motion = features.get('motion_intensity', 0)
            if motion > 0.5:
                descriptions.append("High action")
            elif motion > 0.2:
                descriptions.append("Moderate movement")
            else:
                descriptions.append("Static content")
            
            # Audio description
            audio_energy = features.get('audio_energy', 0)
            if audio_energy > 0.1:
                descriptions.append("Clear audio")
            elif audio_energy > 0.05:
                descriptions.append("Moderate audio")
            else:
                descriptions.append("Quiet")
            
            # Visual quality
            contrast = features.get('contrast', 0)
            if contrast > 50:
                descriptions.append("High contrast")
            else:
                descriptions.append("Low contrast")
            
            # Theme-specific descriptions
            if theme == 'entertainment' and features.get('entertainment_score', 0) > 0.5:
                descriptions.append("Engaging content")
            elif theme == 'educational' and features.get('educational_score', 0) > 0.5:
                descriptions.append("Clear presentation")
            elif theme == 'music' and features.get('music_score', 0) > 0.5:
                descriptions.append("Musical content")
            elif theme == 'gaming' and features.get('gaming_score', 0) > 0.5:
                descriptions.append("Action-packed")
            elif theme == 'lifestyle' and features.get('lifestyle_score', 0) > 0.5:
                descriptions.append("Aesthetic visuals")
            elif theme == 'news' and features.get('news_score', 0) > 0.5:
                descriptions.append("Professional quality")
            
            return ", ".join(descriptions[:3])  # Limit to 3 descriptions
        
        except Exception as e:
            logger.error(f"Error generating description: {str(e)}")
            return "Video segment"