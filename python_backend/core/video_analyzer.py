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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoAnalyzer:
    """
    Kelas untuk menganalisis video dan menentukan segmen terbaik untuk short video
    """
    
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.target_duration = 60  # Target durasi short video dalam detik
        self.min_duration = 15     # Durasi minimum short video
        self.max_duration = 90     # Durasi maksimum short video
    
    def analyze_video(self, video_path: str) -> Dict:
        """
        Menganalisis video dan mengembalikan informasi detail
        """
        try:
            clip = VideoFileClip(video_path)
            duration = clip.duration
            fps = clip.fps
            
            # Analisis visual
            visual_scores = self._analyze_visual_content(video_path)
            
            # Analisis audio
            audio_scores = self._analyze_audio_content(clip)
            
            # Analisis movement/action
            movement_scores = self._analyze_movement(video_path)
            
            # Gabungkan semua skor
            combined_scores = self._combine_scores(visual_scores, audio_scores, movement_scores)
            
            # Tentukan segmen terbaik
            best_segments = self._find_best_segments(combined_scores, duration)
            
            clip.close()
            
            return {
                'duration': duration,
                'fps': fps,
                'visual_scores': visual_scores,
                'audio_scores': audio_scores,
                'movement_scores': movement_scores,
                'combined_scores': combined_scores,
                'best_segments': best_segments
            }
            
        except Exception as e:
            logger.error(f"Error analyzing video: {str(e)}")
            raise
    
    def _analyze_visual_content(self, video_path: str) -> List[float]:
        """
        Menganalisis konten visual untuk menentukan frame yang menarik
        """
        cap = cv2.VideoCapture(video_path)
        visual_scores = []
        
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        # Sampling setiap detik
        sample_interval = int(fps)
        
        for i in range(0, frame_count, sample_interval):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            
            if not ret:
                break
            
            # Hitung skor berdasarkan berbagai faktor
            score = self._calculate_visual_score(frame)
            visual_scores.append(score)
        
        cap.release()
        return visual_scores
    
    def _calculate_visual_score(self, frame) -> float:
        """
        Menghitung skor visual berdasarkan berbagai faktor
        """
        # Konversi ke grayscale untuk analisis
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 1. Variance (kontras)
        variance = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # 2. Edge density
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges) / (edges.shape[0] * edges.shape[1])
        
        # 3. Color diversity
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv], [0, 1], None, [50, 60], [0, 180, 0, 256])
        color_diversity = np.count_nonzero(hist) / hist.size
        
        # 4. Face detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        face_score = len(faces) * 0.3  # Boost untuk frame dengan wajah
        
        # Gabungkan skor
        total_score = (variance * 0.3 + edge_density * 1000 * 0.3 + 
                      color_diversity * 0.2 + face_score * 0.2)
        
        return total_score
    
    def _analyze_audio_content(self, clip: VideoFileClip) -> List[float]:
        """
        Menganalisis konten audio untuk menentukan bagian dengan audio menarik
        """
        if clip.audio is None:
            return [0.0] * int(clip.duration)
        
        # Extract audio
        audio_array = clip.audio.to_soundarray(fps=22050)
        if len(audio_array.shape) > 1:
            audio_array = np.mean(audio_array, axis=1)
        
        # Analisis per detik
        sample_rate = 22050
        window_size = sample_rate  # 1 detik
        audio_scores = []
        
        for i in range(0, len(audio_array), window_size):
            window = audio_array[i:i + window_size]
            if len(window) < window_size:
                break
            
            # 1. Volume (RMS)
            rms = np.sqrt(np.mean(window ** 2))
            
            # 2. Spectral centroid
            spectral_centroids = librosa.feature.spectral_centroid(y=window, sr=sample_rate)[0]
            spectral_centroid = np.mean(spectral_centroids)
            
            # 3. Zero crossing rate
            zcr = librosa.feature.zero_crossing_rate(window)[0]
            zcr_mean = np.mean(zcr)
            
            # 4. Spectral rolloff
            spectral_rolloff = librosa.feature.spectral_rolloff(y=window, sr=sample_rate)[0]
            rolloff_mean = np.mean(spectral_rolloff)
            
            # Gabungkan skor
            audio_score = (rms * 0.4 + spectral_centroid/1000 * 0.2 + 
                          zcr_mean * 0.2 + rolloff_mean/1000 * 0.2)
            audio_scores.append(audio_score)
        
        return audio_scores
    
    def _analyze_movement(self, video_path: str) -> List[float]:
        """
        Menganalisis pergerakan dalam video
        """
        cap = cv2.VideoCapture(video_path)
        movement_scores = []
        
        ret, prev_frame = cap.read()
        if not ret:
            cap.release()
            return []
        
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Optical flow
            flow = cv2.calcOpticalFlowPyrLK(prev_gray, gray, None, None)
            
            # Motion magnitude
            diff = cv2.absdiff(prev_gray, gray)
            motion_score = np.mean(diff)
            
            # Simpan skor per detik
            if frame_count % int(fps) == 0:
                movement_scores.append(motion_score)
            
            prev_gray = gray
            frame_count += 1
        
        cap.release()
        return movement_scores
    
    def _combine_scores(self, visual_scores: List[float], audio_scores: List[float], 
                       movement_scores: List[float]) -> List[float]:
        """
        Menggabungkan semua skor untuk mendapatkan skor final
        """
        # Normalisasi panjang list
        min_length = min(len(visual_scores), len(audio_scores), len(movement_scores))
        
        visual_scores = visual_scores[:min_length]
        audio_scores = audio_scores[:min_length]
        movement_scores = movement_scores[:min_length]
        
        # Normalisasi skor
        visual_scores = self._normalize_scores(visual_scores)
        audio_scores = self._normalize_scores(audio_scores)
        movement_scores = self._normalize_scores(movement_scores)
        
        # Gabungkan dengan bobot
        combined_scores = []
        for i in range(min_length):
            combined_score = (visual_scores[i] * 0.4 + 
                            audio_scores[i] * 0.3 + 
                            movement_scores[i] * 0.3)
            combined_scores.append(combined_score)
        
        return combined_scores
    
    def _normalize_scores(self, scores: List[float]) -> List[float]:
        """
        Normalisasi skor ke rentang 0-1
        """
        if not scores:
            return []
        
        min_score = min(scores)
        max_score = max(scores)
        
        if max_score == min_score:
            return [0.5] * len(scores)
        
        return [(score - min_score) / (max_score - min_score) for score in scores]
    
    def _find_best_segments(self, combined_scores: List[float], 
                          video_duration: float) -> List[Dict]:
        """
        Mencari segmen terbaik berdasarkan skor gabungan
        """
        if not combined_scores:
            return []
        
        # Sliding window untuk mencari segmen terbaik
        segments = []
        
        for duration in [15, 30, 60, 90]:  # Berbagai durasi target
            if duration > video_duration:
                continue
            
            best_score = 0
            best_start = 0
            
            # Sliding window
            for start in range(len(combined_scores) - duration + 1):
                segment_scores = combined_scores[start:start + duration]
                avg_score = np.mean(segment_scores)
                
                if avg_score > best_score:
                    best_score = avg_score
                    best_start = start
            
            segments.append({
                'start_time': best_start,
                'end_time': best_start + duration,
                'duration': duration,
                'score': best_score,
                'confidence': min(best_score, 1.0)
            })
        
        # Sort berdasarkan skor
        segments.sort(key=lambda x: x['score'], reverse=True)
        
        return segments[:5]  # Return top 5 segments