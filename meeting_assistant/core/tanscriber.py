import os
import openai
from typing import List, Dict

class Transcriber:
    """使用 Whisper API 进行语音转文字"""
    
    def __init__(self, api_key: str):
        openai.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key)
    
    def transcribe(self, audio_path: str, language: str = "zh") -> Dict:
        """转写单段音频，返回带时间戳的文本"""
        with open(audio_path, "rb") as f:
            response = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                response_format="verbose_json",
                language=language,
                timestamp_granularities=["segment"]
            )
        return response
    
    def transcribe_long(self, audio_path: str) -> str:
        """处理长音频：分段转写后合并"""
        from core.audio_processor import AudioProcessor
        
        # 先检查文件大小，若小于 25MB 直接转写
        if os.path.getsize(audio_path) < 25 * 1024 * 1024:
            result = self.transcribe(audio_path)
            return result.text
        
        # 分段处理
        chunks = AudioProcessor.split_audio(audio_path)
        full_text = ""
        for chunk_path in chunks:
            result = self.transcribe(chunk_path)
            full_text += result.text + "\n"
            os.remove(chunk_path)
        return full_text
