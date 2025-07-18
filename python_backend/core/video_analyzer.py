import cv2
import numpy as np
import librosa
from moviepy.editor import VideoFileClip
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer
import torch
import logging
from typing import List, Tuple, Dict
import json
from scipy import signal
from scipy.stats import zscore
import face_recognition
from ultralytics import YOLO
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoAnalyzer:
    """
    Enhanced AI-powered video analyzer untuk menentukan segmen terbaik dari video panjang
    dengan algoritma machine learning yang canggih
    """
    
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.target_duration = 60  # Target durasi short video dalam detik
        self.min_duration = 15     # Durasi minimum short video
        self.max_duration = 90     # Durasi maksimum short video
        
        # Initialize YOLO for object detection
        try:
            self.yolo_model = YOLO('yolov8n.pt')  # Lightweight model
        except:
            logger.warning("YOLO model tidak tersedia, menggunakan analisis basic")
            self.yolo_model = None
            
        # Weights untuk berbagai aspek analisis
        self.weights = {
            'visual_appeal': 0.25,    # Kualitas visual dan komposisi
            'motion_activity': 0.20,  # Aktivitas dan gerakan
            'audio_quality': 0.15,    # Kualitas audio dan speech
            'face_presence': 0.15,    # Kehadiran wajah manusia
            'object_interest': 0.10,  # Objek menarik dalam frame
            'scene_diversity': 0.10,  # Keragaman scene
            'technical_quality': 0.05 # Kualitas teknis (focus, exposure)
        }
    
    def analyze_video(self, video_path: str, target_segments: int = 3) -> Dict:
        """
        Menganalisis video dengan AI dan mengembalikan segmen terbaik
        
        Args:
            video_path: Path ke video input
            target_segments: Jumlah segmen terbaik yang diinginkan
        
        Returns:
            Dict dengan informasi analisis dan segmen terbaik
        """
        try:
            logger.info(f"Memulai analisis AI untuk video: {video_path}")
            clip = VideoFileClip(video_path)
            duration = clip.duration
            fps = clip.fps
            
            # Analisis multi-aspek dengan AI
            visual_scores = self._analyze_visual_content_enhanced(video_path, fps)
            audio_scores = self._analyze_audio_content_enhanced(clip)
            motion_scores = self._analyze_motion_enhanced(video_path, fps)
            face_scores = self._analyze_face_presence(video_path, fps)
            object_scores = self._analyze_object_interest(video_path, fps)
            scene_scores = self._analyze_scene_diversity(video_path, fps)
            technical_scores = self._analyze_technical_quality(video_path, fps)
            
            # Gabungkan semua skor dengan weighted average
            combined_scores = self._combine_scores_enhanced(
                visual_scores, audio_scores, motion_scores, 
                face_scores, object_scores, scene_scores, technical_scores
            )
            
            # Smoothing untuk menghindari transisi yang terlalu cepat
            combined_scores = self._smooth_scores(combined_scores)
            
            # Tentukan segmen terbaik dengan algoritma advanced
            best_segments = self._find_best_segments_enhanced(
                combined_scores, duration, target_segments
            )
            
            # Analisis tema dan mood untuk efek yang sesuai
            theme_analysis = self._analyze_video_theme(visual_scores, audio_scores)
            
            clip.close()
            
            result = {
                'video_info': {
                    'duration': duration,
                    'fps': fps,
                    'resolution': (clip.w, clip.h)
                },
                'analysis_scores': {
                    'visual': visual_scores,
                    'audio': audio_scores,
                    'motion': motion_scores,
                    'faces': face_scores,
                    'objects': object_scores,
                    'scenes': scene_scores,
                    'technical': technical_scores,
                    'combined': combined_scores
                },
                'best_segments': best_segments,
                'theme_analysis': theme_analysis,
                'processing_metadata': {
                    'timestamp': str(datetime.now()),
                    'analyzer_version': '2.0',
                    'ai_features_used': ['YOLO', 'FaceRecognition', 'AudioAnalysis', 'MotionDetection']
                }
            }
            
            logger.info(f"Analisis selesai. Ditemukan {len(best_segments)} segmen berkualitas tinggi")
            return result
            
        except Exception as e:
            logger.error(f"Error dalam analisis video: {str(e)}")
            raise

    def _analyze_visual_content_enhanced(self, video_path: str, fps: float) -> List[float]:
        """
        Analisis konten visual dengan AI yang lebih canggih
        """
        cap = cv2.VideoCapture(video_path)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        visual_scores = []
        
        # Sample frames untuk analisis (setiap detik)
        sample_interval = max(1, int(fps))
        
        for frame_idx in range(0, frame_count, sample_interval):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            
            if not ret:
                break
                
            # Analisis kualitas visual
            score = 0.0
            
            # 1. Analisis kontras dan ketajaman
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            contrast = gray.std()
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            score += min(contrast / 100.0, 1.0) * 0.3
            score += min(laplacian_var / 1000.0, 1.0) * 0.3
            
            # 2. Analisis komposisi (rule of thirds)
            h, w = gray.shape
            roi_points = [
                (w//3, h//3), (2*w//3, h//3),
                (w//3, 2*h//3), (2*w//3, 2*h//3)
            ]
            composition_score = 0
            for x, y in roi_points:
                if gray[y, x] > gray.mean():
                    composition_score += 0.25
            score += composition_score * 0.2
            
            # 3. Analisis distribusi warna
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            hist = cv2.calcHist([hsv], [0, 1], None, [50, 60], [0, 180, 0, 256])
            color_diversity = cv2.calcHist([hsv], [1], None, [256], [0, 256]).std()
            score += min(color_diversity / 50.0, 1.0) * 0.2
            
            visual_scores.append(score)
        
        cap.release()
        return visual_scores

    def _analyze_audio_content_enhanced(self, clip: VideoFileClip) -> List[float]:
        """
        Analisis konten audio dengan deteksi speech dan musik
        """
        if not clip.audio:
            return [0.0] * int(clip.duration)
            
        # Extract audio
        audio = clip.audio
        y, sr = librosa.load(audio.filename, sr=22050)
        
        # Analisis per detik
        hop_length = sr  # 1 detik
        audio_scores = []
        
        for i in range(0, len(y), hop_length):
            segment = y[i:i+hop_length]
            if len(segment) < hop_length:
                break
                
            score = 0.0
            
            # 1. Analisis volume dan dinamika
            rms = librosa.feature.rms(y=segment)[0]
            score += min(np.mean(rms) * 10, 1.0) * 0.3
            
            # 2. Deteksi speech
            spectral_centroids = librosa.feature.spectral_centroid(y=segment, sr=sr)[0]
            if np.mean(spectral_centroids) > 1000:  # Kemungkinan speech
                score += 0.4
            
            # 3. Analisis ritme dan beat
            tempo, beats = librosa.beat.beat_track(y=segment, sr=sr)
            if len(beats) > 0:
                score += min(len(beats) / 10.0, 1.0) * 0.3
            
            audio_scores.append(score)
            
        return audio_scores

    def _analyze_motion_enhanced(self, video_path: str, fps: float) -> List[float]:
        """
        Analisis gerakan dengan optical flow dan scene change detection
        """
        cap = cv2.VideoCapture(video_path)
        motion_scores = []
        prev_frame = None
        
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        sample_interval = max(1, int(fps / 5))  # Sample 5 kali per detik
        
        for frame_idx in range(0, frame_count, sample_interval):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            
            if not ret:
                break
                
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            if prev_frame is not None:
                # Optical flow
                flow = cv2.calcOpticalFlowPyrLK(
                    prev_frame, gray, None, None
                )
                
                # Motion magnitude
                motion_magnitude = np.mean(np.abs(flow[0] - flow[1])) if flow[0] is not None else 0
                
                # Scene change detection
                hist_prev = cv2.calcHist([prev_frame], [0], None, [256], [0, 256])
                hist_curr = cv2.calcHist([gray], [0], None, [256], [0, 256])
                scene_change = cv2.compareHist(hist_prev, hist_curr, cv2.HISTCMP_CORREL)
                
                # Combine scores
                motion_score = min(motion_magnitude / 50.0, 1.0) * 0.7
                scene_score = (1.0 - scene_change) * 0.3
                
                motion_scores.append(motion_score + scene_score)
            else:
                motion_scores.append(0.0)
                
            prev_frame = gray.copy()
        
        cap.release()
        
        # Interpolate ke detik
        target_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps)
        if len(motion_scores) != target_length:
            motion_scores = np.interp(
                np.linspace(0, len(motion_scores)-1, target_length),
                np.arange(len(motion_scores)),
                motion_scores
            ).tolist()
        
        return motion_scores

    def _analyze_face_presence(self, video_path: str, fps: float) -> List[float]:
        """
        Deteksi kehadiran dan kualitas wajah dalam video
        """
        cap = cv2.VideoCapture(video_path)
        face_scores = []
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Sample setiap 1 detik
        for frame_idx in range(0, frame_count, int(fps)):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            
            if not ret:
                break
                
            try:
                # Convert BGR to RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Find faces
                face_locations = face_recognition.face_locations(rgb_frame)
                
                if face_locations:
                    # Score berdasarkan jumlah dan ukuran wajah
                    total_face_area = 0
                    for (top, right, bottom, left) in face_locations:
                        face_area = (bottom - top) * (right - left)
                        total_face_area += face_area
                    
                    # Normalize berdasarkan ukuran frame
                    frame_area = frame.shape[0] * frame.shape[1]
                    face_ratio = total_face_area / frame_area
                    
                    # Optimal face ratio: 0.05 - 0.3
                    if 0.05 <= face_ratio <= 0.3:
                        score = 1.0
                    elif face_ratio < 0.05:
                        score = face_ratio / 0.05
                    else:
                        score = max(0.3, 1.0 - (face_ratio - 0.3) / 0.2)
                    
                    face_scores.append(score)
                else:
                    face_scores.append(0.0)
                    
            except Exception as e:
                logger.warning(f"Error dalam face detection: {e}")
                face_scores.append(0.0)
        
        cap.release()
        return face_scores

    def _analyze_object_interest(self, video_path: str, fps: float) -> List[float]:
        """
        Analisis objek menarik menggunakan YOLO
        """
        if not self.yolo_model:
            return [0.5] * int(cv2.VideoCapture(video_path).get(cv2.CAP_PROP_FRAME_COUNT) / fps)
        
        cap = cv2.VideoCapture(video_path)
        object_scores = []
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Objek yang dianggap menarik (skor lebih tinggi)
        interesting_objects = {
            'person': 1.0, 'car': 0.8, 'motorcycle': 0.8, 'bicycle': 0.7,
            'dog': 0.9, 'cat': 0.9, 'bird': 0.7, 'horse': 0.8,
            'sports ball': 0.6, 'cell phone': 0.5, 'laptop': 0.5
        }
        
        for frame_idx in range(0, frame_count, int(fps)):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            
            if not ret:
                break
                
            try:
                results = self.yolo_model(frame, verbose=False)
                
                score = 0.0
                for result in results:
                    if result.boxes is not None:
                        for box in result.boxes:
                            class_name = self.yolo_model.names[int(box.cls)]
                            confidence = float(box.conf)
                            
                            if class_name in interesting_objects:
                                score += interesting_objects[class_name] * confidence
                
                object_scores.append(min(score, 1.0))
                
            except Exception as e:
                logger.warning(f"Error dalam object detection: {e}")
                object_scores.append(0.0)
        
        cap.release()
        return object_scores

    def _analyze_scene_diversity(self, video_path: str, fps: float) -> List[float]:
        """
        Analisis keragaman scene untuk menghindari segment yang monoton
        """
        cap = cv2.VideoCapture(video_path)
        scene_scores = []
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        prev_histograms = []
        window_size = 5  # Bandingkan dengan 5 frame sebelumnya
        
        for frame_idx in range(0, frame_count, int(fps)):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            
            if not ret:
                break
                
            # Calculate histogram
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            hist = cv2.calcHist([hsv], [0, 1, 2], None, [50, 60, 60], [0, 180, 0, 256, 0, 256])
            hist = cv2.normalize(hist, hist).flatten()
            
            if len(prev_histograms) >= window_size:
                # Calculate diversity score
                similarities = []
                for prev_hist in prev_histograms[-window_size:]:
                    similarity = cv2.compareHist(hist, prev_hist, cv2.HISTCMP_CORREL)
                    similarities.append(similarity)
                
                # Diversity = 1 - average similarity
                diversity = 1.0 - np.mean(similarities)
                scene_scores.append(max(0.0, diversity))
                
                prev_histograms.append(hist)
                if len(prev_histograms) > window_size * 2:
                    prev_histograms.pop(0)
            else:
                scene_scores.append(0.5)  # Default score
                prev_histograms.append(hist)
        
        cap.release()
        return scene_scores

    def _analyze_technical_quality(self, video_path: str, fps: float) -> List[float]:
        """
        Analisis kualitas teknis (focus, exposure, stabilitas)
        """
        cap = cv2.VideoCapture(video_path)
        technical_scores = []
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        for frame_idx in range(0, frame_count, int(fps)):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            
            if not ret:
                break
                
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # 1. Focus quality (Laplacian variance)
            focus_score = cv2.Laplacian(gray, cv2.CV_64F).var()
            focus_score = min(focus_score / 1000.0, 1.0)
            
            # 2. Exposure quality (histogram analysis)
            hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
            
            # Check for over/under exposure
            total_pixels = gray.shape[0] * gray.shape[1]
            overexposed = np.sum(hist[240:]) / total_pixels
            underexposed = np.sum(hist[:15]) / total_pixels
            
            exposure_score = 1.0 - max(overexposed, underexposed) * 2
            exposure_score = max(0.0, exposure_score)
            
            # Combine scores
            technical_score = (focus_score * 0.6 + exposure_score * 0.4)
            technical_scores.append(technical_score)
        
        cap.release()
        return technical_scores

    def _combine_scores_enhanced(self, visual_scores, audio_scores, motion_scores, 
                                face_scores, object_scores, scene_scores, technical_scores):
        """
        Menggabungkan semua skor dengan weighted average
        """
        # Ensure all scores have the same length
        min_length = min(len(visual_scores), len(audio_scores), len(motion_scores),
                        len(face_scores), len(object_scores), len(scene_scores), len(technical_scores))
        
        combined_scores = []
        
        for i in range(min_length):
            score = (
                visual_scores[i] * self.weights['visual_appeal'] +
                motion_scores[i] * self.weights['motion_activity'] +
                audio_scores[i] * self.weights['audio_quality'] +
                face_scores[i] * self.weights['face_presence'] +
                object_scores[i] * self.weights['object_interest'] +
                scene_scores[i] * self.weights['scene_diversity'] +
                technical_scores[i] * self.weights['technical_quality']
            )
            combined_scores.append(score)
        
        return combined_scores

    def _smooth_scores(self, scores: List[float], window_size: int = 5) -> List[float]:
        """
        Smoothing skor untuk menghindari fluktuasi yang terlalu cepat
        """
        if len(scores) < window_size:
            return scores
            
        smoothed = []
        for i in range(len(scores)):
            start = max(0, i - window_size // 2)
            end = min(len(scores), i + window_size // 2 + 1)
            smoothed.append(np.mean(scores[start:end]))
        
        return smoothed

    def _find_best_segments_enhanced(self, scores: List[float], duration: float, 
                                   target_segments: int = 3) -> List[Dict]:
        """
        Mencari segmen terbaik dengan algoritma yang lebih canggih
        """
        if not scores:
            return []
        
        # Convert to numpy for easier processing
        scores_array = np.array(scores)
        
        # Find peaks (local maxima)
        peaks, properties = signal.find_peaks(
            scores_array, 
            height=np.percentile(scores_array, 70),  # Only consider top 30%
            distance=self.min_duration,  # Minimum distance between peaks
            width=5  # Minimum width of peaks
        )
        
        if len(peaks) == 0:
            # Fallback: use highest scoring segments
            peaks = np.argsort(scores_array)[-target_segments:]
        
        # Extract segments around peaks
        segments = []
        for peak in peaks:
            # Determine segment boundaries
            start_time = max(0, peak - self.target_duration // 2)
            end_time = min(duration, peak + self.target_duration // 2)
            
            # Adjust if too short
            if end_time - start_time < self.min_duration:
                if start_time == 0:
                    end_time = min(duration, start_time + self.min_duration)
                else:
                    start_time = max(0, end_time - self.min_duration)
            
            segment_score = np.mean(scores_array[int(start_time):int(end_time)])
            
            segments.append({
                'start_time': start_time,
                'end_time': end_time,
                'duration': end_time - start_time,
                'score': segment_score,
                'peak_time': peak,
                'quality_metrics': {
                    'peak_score': scores_array[peak],
                    'consistency': 1.0 - np.std(scores_array[int(start_time):int(end_time)]),
                    'improvement_potential': segment_score / np.mean(scores_array)
                }
            })
        
        # Sort by score and return top segments
        segments.sort(key=lambda x: x['score'], reverse=True)
        return segments[:target_segments]

    def _analyze_video_theme(self, visual_scores: List[float], audio_scores: List[float]) -> Dict:
        """
        Analisis tema video untuk menentukan efek yang sesuai
        """
        avg_visual = np.mean(visual_scores)
        avg_audio = np.mean(audio_scores)
        
        # Determine theme based on scores
        if avg_visual > 0.7 and avg_audio > 0.6:
            theme = 'energetic'
            confidence = 0.9
        elif avg_visual < 0.4 and avg_audio < 0.4:
            theme = 'calm'
            confidence = 0.8
        elif avg_audio > 0.6:
            theme = 'entertainment'
            confidence = 0.7
        else:
            theme = 'educational'
            confidence = 0.6
        
        return {
            'primary_theme': theme,
            'confidence': confidence,
            'visual_intensity': avg_visual,
            'audio_intensity': avg_audio,
            'recommended_effects': self._get_theme_effects(theme)
        }

    def _get_theme_effects(self, theme: str) -> Dict:
        """
        Mendapatkan efek yang direkomendasikan berdasarkan tema
        """
        effect_map = {
            'energetic': {
                'transitions': ['quick_zoom', 'fast_cut', 'shake'],
                'colors': ['high_saturation', 'vibrant', 'warm'],
                'text_style': 'bold_animated',
                'pace': 'fast'
            },
            'calm': {
                'transitions': ['fade', 'slow_zoom', 'gentle_pan'],
                'colors': ['soft', 'pastel', 'cool'],
                'text_style': 'elegant_fade',
                'pace': 'slow'
            },
            'entertainment': {
                'transitions': ['creative_cut', 'bounce', 'slide'],
                'colors': ['balanced', 'bright', 'mixed'],
                'text_style': 'playful',
                'pace': 'medium'
            },
            'educational': {
                'transitions': ['clean_cut', 'smooth_fade', 'highlight'],
                'colors': ['professional', 'clear', 'neutral'],
                'text_style': 'clear_readable',
                'pace': 'medium'
            }
        }
        
        return effect_map.get(theme, effect_map['educational'])