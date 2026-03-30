import pytest
import os
import sys

# プロジェクトルートをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from unittest.mock import patch

def test_validate_success():
    """環境変数から正しく設定が読み込まれるかテスト"""
    mock_env = {
        "LMSTUDIO_API_BASE": "http://localhost:1234/api/v1",
        "LMSTUDIO_API_KEY": "dummy_key"
    }
    
    with patch.dict(os.environ, mock_env, clear=True):
        # dotenvを呼ばせないためにモック化
        with patch('config.load_dotenv'):
            Config.validate()
    
    assert Config.LMSTUDIO_API_BASE == "http://localhost:1234/api/v1"
    assert Config.LMSTUDIO_API_KEY == "dummy_key"

def test_validate_missing_api_base():
    """必須のLMSTUDIO_API_BASEが存在しない場合にValueErrorとなるかテスト"""
    mock_env = {
        "LMSTUDIO_API_KEY": "dummy_key"
    }
    
    with patch.dict(os.environ, mock_env, clear=True):
        with patch('config.load_dotenv'):
            with pytest.raises(ValueError, match="環境変数 LMSTUDIO_API_BASE が設定されていません。"):
                Config.validate()

def test_validate_default_api_key():
    """API_KEYが省略された場合のデフォルト値のテスト"""
    mock_env = {
        "LMSTUDIO_API_BASE": "http://localhost:1234/api/v1",
    }
    
    with patch.dict(os.environ, mock_env, clear=True):
        with patch('config.load_dotenv'):
            Config.validate()
            
    assert Config.LMSTUDIO_API_BASE == "http://localhost:1234/api/v1"
    assert Config.LMSTUDIO_API_KEY == "not_needed"
