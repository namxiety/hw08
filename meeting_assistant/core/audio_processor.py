import os
import uuid
from pydub import AudioSegment

class AudioProcessor:
    """音频预处理：格式统一、采样率转换、分段"""
    
    SUPPORTED_FORMATS = ['.mp3', '.wav', '.m4a', '.flac']
    TARGET_SR = 16000  # Whisper 推荐采样率
    
    @staticmethod
    def preprocess(file_path: str) -> str:
        """将音频统一转换为 16kHz 单声道 WAV"""
        audio = AudioSegment.from_file(file_path)
        audio = audio.set_frame_rate(16000).set_channels(1)
        
        output_path = f"./uploads/{uuid.uuid4()}.wav"
        audio.export(output_path, format="wav")
        return output_path
    
    @staticmethod
    def split_audio(file_path: str, max_duration: int = 600) -> list:
        """将长音频分段（Whisper API 有 25MB 限制）"""
        audio = AudioSegment.from_wav(file_path)
        duration_ms = len(audio)
        chunk_size_ms = max_duration * 1000
        
        chunks = []
        for i in range(0, duration_ms, chunk_size_ms):
            chunk = audio[i:i+chunk_size_ms]
            chunk_path = f"./uploads/chunk_{i//chunk_size_ms}.wav"
            chunk.export(chunk_path, format="wav")
            chunks.append(chunk_path)
        return chunks
