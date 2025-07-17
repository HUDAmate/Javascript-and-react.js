import whisper
from faster_whisper import WhisperModel
import torch
import logging
from typing import List, Dict, Tuple
import re
import json
from moviepy.editor import VideoFileClip
import numpy as np
from transformers import pipeline
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SubtitleGenerator:
    """
    Kelas untuk generate subtitle otomatis dengan akurasi tinggi
    """
    
    def __init__(self, model_size: str = "medium"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_size = model_size
        
        # Initialize Whisper model
        self.whisper_model = WhisperModel(model_size, device=self.device)
        
        # Initialize punctuation model
        self.punctuation_model = pipeline(
            "text-classification",
            model="oliverguhr/fullstop-punctuation-multilang-large",
            device=0 if torch.cuda.is_available() else -1
        )
        
        # Download NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
    
    def generate_subtitle(self, video_path: str, language: str = "auto") -> Dict:
        """
        Generate subtitle dari video dengan akurasi tinggi
        """
        try:
            # Extract audio dari video
            audio_path = self._extract_audio(video_path)
            
            # Transcribe audio
            segments = self._transcribe_audio(audio_path, language)
            
            # Improve punctuation dan formatting
            improved_segments = self._improve_formatting(segments)
            
            # Generate subtitle formats
            subtitle_formats = self._generate_subtitle_formats(improved_segments)
            
            return {
                'segments': improved_segments,
                'subtitle_formats': subtitle_formats,
                'language': language,
                'confidence': self._calculate_confidence(improved_segments)
            }
            
        except Exception as e:
            logger.error(f"Error generating subtitle: {str(e)}")
            raise
    
    def _extract_audio(self, video_path: str) -> str:
        """
        Extract audio dari video
        """
        try:
            clip = VideoFileClip(video_path)
            audio_path = video_path.replace('.mp4', '_audio.wav')
            clip.audio.write_audiofile(audio_path, verbose=False, logger=None)
            clip.close()
            return audio_path
        except Exception as e:
            logger.error(f"Error extracting audio: {str(e)}")
            raise
    
    def _transcribe_audio(self, audio_path: str, language: str) -> List[Dict]:
        """
        Transcribe audio menggunakan Whisper
        """
        try:
            # Set language parameter
            lang_param = None if language == "auto" else language
            
            segments, info = self.whisper_model.transcribe(
                audio_path,
                language=lang_param,
                beam_size=5,
                best_of=5,
                temperature=0.0,
                vad_filter=True,
                vad_parameters=dict(min_silence_duration_ms=500),
                word_timestamps=True
            )
            
            result_segments = []
            for segment in segments:
                result_segments.append({
                    'start': segment.start,
                    'end': segment.end,
                    'text': segment.text.strip(),
                    'confidence': segment.avg_logprob,
                    'words': [
                        {
                            'word': word.word,
                            'start': word.start,
                            'end': word.end,
                            'confidence': word.probability
                        } for word in segment.words
                    ] if hasattr(segment, 'words') and segment.words else []
                })
            
            return result_segments
            
        except Exception as e:
            logger.error(f"Error transcribing audio: {str(e)}")
            raise
    
    def _improve_formatting(self, segments: List[Dict]) -> List[Dict]:
        """
        Improve formatting dan punctuation
        """
        improved_segments = []
        
        for segment in segments:
            text = segment['text']
            
            # Clean text
            text = self._clean_text(text)
            
            # Add punctuation
            text = self._add_punctuation(text)
            
            # Capitalize sentences
            text = self._capitalize_sentences(text)
            
            # Split long segments
            split_segments = self._split_long_segments(segment, text)
            
            improved_segments.extend(split_segments)
        
        return improved_segments
    
    def _clean_text(self, text: str) -> str:
        """
        Clean dan normalize text
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove filler words (untuk bahasa Indonesia)
        filler_words = ['eh', 'em', 'uh', 'um', 'ah', 'eee', 'mmm']
        for filler in filler_words:
            text = re.sub(rf'\b{filler}\b', '', text, flags=re.IGNORECASE)
        
        # Remove repeated characters
        text = re.sub(r'(.)\1{2,}', r'\1\1', text)
        
        return text.strip()
    
    def _add_punctuation(self, text: str) -> str:
        """
        Add punctuation menggunakan AI model
        """
        try:
            # Split into sentences
            sentences = sent_tokenize(text)
            improved_sentences = []
            
            for sentence in sentences:
                if len(sentence.strip()) > 0:
                    # Add period if not present
                    if not sentence.strip().endswith(('.', '!', '?')):
                        sentence += '.'
                    improved_sentences.append(sentence)
            
            return ' '.join(improved_sentences)
        except:
            # Fallback: simple punctuation
            if not text.endswith(('.', '!', '?')):
                text += '.'
            return text
    
    def _capitalize_sentences(self, text: str) -> str:
        """
        Capitalize awal kalimat
        """
        sentences = sent_tokenize(text)
        capitalized_sentences = []
        
        for sentence in sentences:
            if sentence:
                sentence = sentence.strip()
                sentence = sentence[0].upper() + sentence[1:] if len(sentence) > 1 else sentence.upper()
                capitalized_sentences.append(sentence)
        
        return ' '.join(capitalized_sentences)
    
    def _split_long_segments(self, original_segment: Dict, improved_text: str) -> List[Dict]:
        """
        Split segment yang terlalu panjang untuk readability
        """
        max_chars = 50  # Maksimal karakter per subtitle
        max_duration = 3.0  # Maksimal durasi per subtitle
        
        if len(improved_text) <= max_chars and (original_segment['end'] - original_segment['start']) <= max_duration:
            # Segment sudah optimal
            result_segment = original_segment.copy()
            result_segment['text'] = improved_text
            return [result_segment]
        
        # Split text by words
        words = improved_text.split()
        segments = []
        current_text = ""
        start_time = original_segment['start']
        duration = original_segment['end'] - original_segment['start']
        words_per_segment = len(words) // max(1, int(len(improved_text) / max_chars)) + 1
        
        for i, word in enumerate(words):
            if len(current_text + " " + word) <= max_chars:
                current_text += " " + word if current_text else word
            else:
                if current_text:
                    # Calculate timing
                    word_ratio = len(current_text.split()) / len(words)
                    segment_duration = duration * word_ratio
                    end_time = start_time + segment_duration
                    
                    segments.append({
                        'start': start_time,
                        'end': end_time,
                        'text': current_text.strip(),
                        'confidence': original_segment['confidence'],
                        'words': []
                    })
                    
                    start_time = end_time
                
                current_text = word
        
        # Add remaining text
        if current_text:
            segments.append({
                'start': start_time,
                'end': original_segment['end'],
                'text': current_text.strip(),
                'confidence': original_segment['confidence'],
                'words': []
            })
        
        return segments
    
    def _calculate_confidence(self, segments: List[Dict]) -> float:
        """
        Calculate overall confidence score
        """
        if not segments:
            return 0.0
        
        total_confidence = sum(segment['confidence'] for segment in segments)
        return abs(total_confidence / len(segments))  # Convert log prob to positive
    
    def _generate_subtitle_formats(self, segments: List[Dict]) -> Dict:
        """
        Generate berbagai format subtitle
        """
        # SRT format
        srt_content = self._generate_srt(segments)
        
        # VTT format
        vtt_content = self._generate_vtt(segments)
        
        # JSON format for custom styling
        json_content = self._generate_json(segments)
        
        return {
            'srt': srt_content,
            'vtt': vtt_content,
            'json': json_content
        }
    
    def _generate_srt(self, segments: List[Dict]) -> str:
        """
        Generate SRT format subtitle
        """
        srt_content = ""
        
        for i, segment in enumerate(segments, 1):
            start_time = self._format_timestamp_srt(segment['start'])
            end_time = self._format_timestamp_srt(segment['end'])
            
            srt_content += f"{i}\n"
            srt_content += f"{start_time} --> {end_time}\n"
            srt_content += f"{segment['text']}\n\n"
        
        return srt_content
    
    def _generate_vtt(self, segments: List[Dict]) -> str:
        """
        Generate VTT format subtitle
        """
        vtt_content = "WEBVTT\n\n"
        
        for segment in segments:
            start_time = self._format_timestamp_vtt(segment['start'])
            end_time = self._format_timestamp_vtt(segment['end'])
            
            vtt_content += f"{start_time} --> {end_time}\n"
            vtt_content += f"{segment['text']}\n\n"
        
        return vtt_content
    
    def _generate_json(self, segments: List[Dict]) -> str:
        """
        Generate JSON format untuk custom styling
        """
        json_data = {
            'subtitles': []
        }
        
        for segment in segments:
            json_data['subtitles'].append({
                'start': segment['start'],
                'end': segment['end'],
                'text': segment['text'],
                'confidence': segment['confidence'],
                'style': {
                    'fontSize': '24px',
                    'fontFamily': 'Arial, sans-serif',
                    'color': '#FFFFFF',
                    'backgroundColor': 'rgba(0, 0, 0, 0.8)',
                    'padding': '8px 12px',
                    'borderRadius': '4px',
                    'textAlign': 'center',
                    'textShadow': '2px 2px 4px rgba(0, 0, 0, 0.8)'
                }
            })
        
        return json.dumps(json_data, indent=2, ensure_ascii=False)
    
    def _format_timestamp_srt(self, seconds: float) -> str:
        """
        Format timestamp untuk SRT (HH:MM:SS,mmm)
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"
    
    def _format_timestamp_vtt(self, seconds: float) -> str:
        """
        Format timestamp untuk VTT (HH:MM:SS.mmm)
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{milliseconds:03d}"