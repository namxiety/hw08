import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Whisper API 配置
    WHISPER_API_KEY = os.getenv("OPENAI_API_KEY")  # 或使用 DeepSeek 的语音接口
    
    # 大模型 API 配置（推荐 DeepSeek，便宜且效果好）
    LLM_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    LLM_BASE_URL = "https://api.deepseek.com"
    LLM_MODEL = "deepseek-chat"
    
    # 本地存储路径
    UPLOAD_DIR = "./uploads"
    OUTPUT_DIR = "./outputs"
