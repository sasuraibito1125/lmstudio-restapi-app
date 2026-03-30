import os
from dotenv import load_dotenv

class Config:
    LMSTUDIO_API_BASE: str = ""
    LMSTUDIO_API_KEY: str = ""

    @classmethod
    def validate(cls) -> None:
        """環境変数を読み込み、設定値の検証を行う"""
        load_dotenv()
        
        api_base = os.getenv("LMSTUDIO_API_BASE")
        if not api_base:
            raise ValueError("環境変数 LMSTUDIO_API_BASE が設定されていません。")
        cls.LMSTUDIO_API_BASE = api_base
        
        api_key = os.getenv("LMSTUDIO_API_KEY", "not_needed")
        cls.LMSTUDIO_API_KEY = api_key
