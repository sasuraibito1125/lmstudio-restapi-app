import pytest
import sys
import os
import logging
from unittest.mock import patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from config import Config
import main

@pytest.fixture
def mock_config():
    """Config の値をモックする"""
    Config.LMSTUDIO_API_BASE = "http://localhost:1234/api/v1"
    Config.LMSTUDIO_API_KEY = "test_key"

def test_fetch_models_success(requests_mock):
    """モデル一覧取得の成功テスト"""
    url = "http://localhost:1234/api/v1/models"
    requests_mock.get(url, json={"models": [{"key": "model-1", "display_name": "Model 1"}, {"key": "model-2", "display_name": "Model 2"}]})
    
    with patch('main.Config.LMSTUDIO_API_BASE', "http://localhost:1234/api/v1"):
        with patch('main.Config.LMSTUDIO_API_KEY', "dummy_key"):
            models = main.fetch_models()
        
    assert len(models) == 2
    assert models[0]["key"] == "model-1"

def test_fetch_models_error(requests_mock, caplog):
    """モデル一覧取得エラーのテスト"""
    url = "http://localhost:1234/api/v1/models"
    requests_mock.get(url, status_code=500)
    
    with patch('main.Config.LMSTUDIO_API_BASE', "http://localhost:1234/api/v1"):
        with patch('main.Config.LMSTUDIO_API_KEY', "dummy_key"):
            with pytest.raises(requests.RequestException):
                main.fetch_models()
        
    assert "モデル一覧の取得に失敗しました" in caplog.text

def test_chat_completion_success(requests_mock, caplog):
    """チャット応答取得の成功テスト"""
    caplog.set_level(logging.INFO)
    url = "http://localhost:1234/api/v1/chat"
    response_json = {
        "output": [
            {
                "type": "message",
                "content": "お役に立てて嬉しいです！"
            }
        ]
    }
    requests_mock.post(url, json=response_json)
    
    with patch('main.Config.LMSTUDIO_API_BASE', "http://localhost:1234/api/v1"):
        with patch('main.Config.LMSTUDIO_API_KEY', "dummy_key"):
            main.chat_completion("テストメッセージ", "dummy-model")
    
    # ログに出力されているか確認
    assert "Assistant: お役に立てて嬉しいです！" in caplog.text

def test_load_model_success(requests_mock):
    """モデルロードの成功テスト"""
    url = "http://localhost:1234/api/v1/models/load"
    requests_mock.post(url, json={"status": "success"})
    
    with patch('main.Config.LMSTUDIO_API_BASE', "http://localhost:1234/api/v1"):
        with patch('main.Config.LMSTUDIO_API_KEY', "dummy_key"):
            main.load_model("dummy-model")

def test_load_model_error(requests_mock, caplog):
    """モデルロードのエラーのテスト"""
    url = "http://localhost:1234/api/v1/models/load"
    requests_mock.post(url, status_code=500)
    
    with patch('main.Config.LMSTUDIO_API_BASE', "http://localhost:1234/api/v1"):
        with patch('main.Config.LMSTUDIO_API_KEY', "dummy_key"):
            with pytest.raises(requests.RequestException):
                main.load_model("dummy-model")
        
    assert "モデル 'dummy-model' のロードに失敗しました" in caplog.text

@patch('main.Config.validate')
@patch('builtins.input', side_effect=['1', 'Hello world'])
def test_main_execution(mock_input, mock_validate, requests_mock, caplog):
    """main() 実行の全体テスト (対話型)"""
    caplog.set_level(logging.INFO)
    url_models = "http://mock-base/models"
    url_load = "http://mock-base/models/load"
    url_chat = "http://mock-base/chat"
    
    with patch('main.Config.LMSTUDIO_API_BASE', "http://mock-base"):
        with patch('main.Config.LMSTUDIO_API_KEY', "dummy_key"):
            requests_mock.get(url_models, json={"models": [{"key": "local-model", "display_name": "Local Model"}]})
            requests_mock.post(url_load, json={})
            requests_mock.post(url_chat, json={"output": [{"content": "Response from assistant"}]})
            
            # stdoutへのprint出力をキャプチャしなくて良いが、例外なく1番のモデルがロードされチャットされるか検証
            main.main()
        
    assert "Response from assistant" in caplog.text

