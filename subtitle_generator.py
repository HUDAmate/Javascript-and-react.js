import whisper
import os
import librosa
import numpy as np
from moviepy.editor import VideoFileClip
import logging

logger = logging.getLogger(__name__)

class SubtitleGenerator:
    def __init__(self):
        try:
            # Load Whisper model
            self.model = whisper.load_model("base")
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading Whisper model: {str(e)}")
            self.model = None
    
    def generate_subtitles(self, video_path):
        """Generate accurate subtitles from video audio"""
        try:
            if not self.model:
                logger.error("Whisper model not available")
                return []
            
            # Extract audio from video
            audio_path = self._extract_audio(video_path)
            
            # Transcribe with Whisper
            result = self.model.transcribe(
                audio_path,
                word_timestamps=True,
                language='auto'
            )
            
            # Convert to subtitle format
            subtitles = self._process_transcription(result)
            
            # Clean up temporary audio file
            if os.path.exists(audio_path):
                os.remove(audio_path)
            
            return subtitles
        
        except Exception as e:
            logger.error(f"Error generating subtitles: {str(e)}")
            return []
    
    def _extract_audio(self, video_path):
        """Extract audio from video file"""
        try:
            audio_path = os.path.join('temp', f'audio_{int(os.path.getmtime(video_path))}.wav')
            
            with VideoFileClip(video_path) as video:
                if video.audio:
                    video.audio.write_audiofile(
                        audio_path,
                        verbose=False,
                        logger=None
                    )
                else:
                    # Create empty audio file if no audio track
                    import wave
                    with wave.open(audio_path, 'w') as wav_file:
                        wav_file.setnchannels(1)
                        wav_file.setsampwidth(2)
                        wav_file.setframerate(22050)
                        wav_file.writeframes(b'')
            
            return audio_path
        
        except Exception as e:
            logger.error(f"Error extracting audio: {str(e)}")
            raise
    
    def _process_transcription(self, result):
        """Process Whisper transcription result into subtitle format"""
        subtitles = []
        
        try:
            # If word-level timestamps are available, use them
            if 'segments' in result:
                for segment in result['segments']:
                    # Split long segments into shorter subtitle chunks
                    words = segment.get('words', [])
                    if words:
                        subtitles.extend(self._create_word_based_subtitles(words))
                    else:
                        # Fallback to segment-based subtitles
                        subtitles.append({
                            'start': segment['start'],
                            'end': segment['end'],
                            'text': segment['text'].strip()
                        })
            else:
                # Fallback: create subtitles from full text
                text = result.get('text', '')
                if text:
                    # Simple time-based splitting
                    duration = 30  # Assume 30 seconds if no timing info
                    words = text.split()
                    words_per_chunk = max(1, len(words) // 10)  # ~10 subtitle chunks
                    
                    for i in range(0, len(words), words_per_chunk):
                        chunk_words = words[i:i + words_per_chunk]
                        start_time = (i / len(words)) * duration
                        end_time = ((i + words_per_chunk) / len(words)) * duration
                        
                        subtitles.append({
                            'start': start_time,
                            'end': end_time,
                            'text': ' '.join(chunk_words)
                        })
        
        except Exception as e:
            logger.error(f"Error processing transcription: {str(e)}")
        
        return subtitles
    
    def _create_word_based_subtitles(self, words):
        """Create subtitles from word-level timestamps"""
        subtitles = []
        
        try:
            # Group words into subtitle chunks (3-7 words per subtitle)
            max_words_per_subtitle = 6
            max_duration = 3.0  # Maximum 3 seconds per subtitle
            
            current_words = []
            start_time = None
            
            for word_info in words:
                word = word_info.get('word', '').strip()
                word_start = word_info.get('start', 0)
                word_end = word_info.get('end', 0)
                
                if not word:
                    continue
                
                # Start new subtitle if this is the first word
                if start_time is None:
                    start_time = word_start
                
                current_words.append(word)
                
                # Check if we should end the current subtitle
                should_end = (
                    len(current_words) >= max_words_per_subtitle or
                    (word_end - start_time) >= max_duration or
                    word.endswith('.') or
                    word.endswith('!') or
                    word.endswith('?')
                )
                
                if should_end and current_words:
                    subtitles.append({
                        'start': start_time,
                        'end': word_end,
                        'text': ' '.join(current_words)
                    })
                    
                    current_words = []
                    start_time = None
            
            # Add remaining words as final subtitle
            if current_words and start_time is not None:
                last_word_end = words[-1].get('end', start_time + 2)
                subtitles.append({
                    'start': start_time,
                    'end': last_word_end,
                    'text': ' '.join(current_words)
                })
        
        except Exception as e:
            logger.error(f"Error creating word-based subtitles: {str(e)}")
        
        return subtitles
    
    def adjust_subtitle_timing(self, subtitles, speed_factor=1.0):
        """Adjust subtitle timing for speed changes"""
        adjusted_subtitles = []
        
        for subtitle in subtitles:
            adjusted_subtitles.append({
                'start': subtitle['start'] / speed_factor,
                'end': subtitle['end'] / speed_factor,
                'text': subtitle['text']
            })
        
        return adjusted_subtitles
    
    def format_subtitles_for_display(self, subtitles, max_chars_per_line=40):
        """Format subtitles for better display"""
        formatted_subtitles = []
        
        for subtitle in subtitles:
            text = subtitle['text']
            
            # Break long lines
            if len(text) > max_chars_per_line:
                words = text.split()
                lines = []
                current_line = []
                current_length = 0
                
                for word in words:
                    if current_length + len(word) + 1 <= max_chars_per_line:
                        current_line.append(word)
                        current_length += len(word) + 1
                    else:
                        if current_line:
                            lines.append(' '.join(current_line))
                        current_line = [word]
                        current_length = len(word)
                
                if current_line:
                    lines.append(' '.join(current_line))
                
                text = '\n'.join(lines)
            
            formatted_subtitles.append({
                'start': subtitle['start'],
                'end': subtitle['end'],
                'text': text
            })
        
        return formatted_subtitles