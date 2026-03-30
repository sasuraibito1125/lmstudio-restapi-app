import sys
import logging
import requests
from typing import Any, Dict, List
from config import Config

# ロガーの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def list_models() -> List[Dict[str, Any]]:
    """モデル一覧を取得する"""
    url = f"{Config.LMSTUDIO_API_BASE}/models"
    headers = {"Authorization": f"Bearer {Config.LMSTUDIO_API_KEY}"}
    
    logger.info(f"モデル一覧を取得します。URL: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        models = data.get("models", [])
        return models
    except requests.RequestException as e:
        logger.error(f"モデル一覧の取得に失敗しました: {e}")
        raise

def load_model(model_id: str) -> None:
    """指定されたモデルをLM Studioサーバーでロードする"""
    url = f"{Config.LMSTUDIO_API_BASE}/models/load"
    headers = {
        "Authorization": f"Bearer {Config.LMSTUDIO_API_KEY}",
        "Content-Type": "application/json"
    }
    # 公式ドキュメントの形式を用いたロードのペイロード
    payload = {
        "model": model_id,
        "context_length": 2048,
        "flash_attention": True,
        "echo_load_config": False
    }
    
    logger.info(f"モデル '{model_id}' のロードを開始します...")
    try:
        # ロード処理は時間がかかる可能性があるため長めのタイムアウトを設定
        response = requests.post(url, headers=headers, json=payload, timeout=300)
        response.raise_for_status()
        logger.info(f"モデル '{model_id}' のロードが完了しました。")
    except requests.RequestException as e:
        logger.error(f"モデル '{model_id}' のロードに失敗しました: {e}")
        raise

def chat_with_model(prompt: str, model_id: str) -> None:
    """メッセージを送信し応答を受け取る"""
    url = f"{Config.LMSTUDIO_API_BASE}/chat"
    headers = {
        "Authorization": f"Bearer {Config.LMSTUDIO_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model_id,
        "input": [
            {"type": "text", "content": f"system: あなたは優秀なAIアシスタントです。日本語で回答してください。\nuser: {prompt}"}
        ],
        "temperature": 0.7
    }
    
    logger.info("=== チャットの実行 ===")
    logger.info(f"User: {prompt}")
    logger.info("Assistant: 応答を待っています...")
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        
        # 応答を取り出す (LM Studio独自APIの形式)
        outputs = data.get("output", [])
        if outputs:
            message = outputs[0].get("content", "")
            logger.info(f"Assistant: {message}")
        else:
            logger.warning("Assistantからの応答が空でした。")
    except requests.RequestException as e:
        logger.error(f"チャットの実行に失敗しました: {e}")
        raise



def main() -> None:
    try:
        Config.validate()
        logger.info("環境設定の読み込み完了。")
    except Exception as e:
        logger.exception("設定エラーのため異常終了します。")
        sys.exit(1)

    try:
        # 1. モデル一覧を取得
        models = list_models()
        if not models:
            logger.info("利用可能なモデルがありません。LM Studio内のダウンロード済みモデルを確認してください。")
            sys.exit(0)

        # 2. モデル一覧を表示
        print("\n=== 利用可能なモデル ===")
        for idx, model in enumerate(models):
            key = model.get('key', 'Unknown')
            display_name = model.get('display_name', key)
            print(f"{idx+1}. {display_name} ({key})")
            
        print("========================")
        
        # 3. モデルを選択
        target_model = None
        while True:
            choice = input(f"ロードしてチャットを行うモデル番号を入力してください (1-{len(models)}) [qで終了]: ")
            if choice.lower() == 'q':
                sys.exit(0)
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(models):
                    target_model = models[idx].get('key', 'local-model')
                    break
                else:
                    print("無効な番号です。正しい範囲で指定してください。")
            except ValueError:
                print("数字または終了用の 'q' を入力してください。")
                
        # 4. ユーザーが選択したモデルをロード
        load_model(target_model)
        
        # 5. ロードしたモデルでチャットメッセージを入力
        print("\n=== チャット入力 ===")
        prompt = input("アシスタントへ送るメッセージを入力してください: ").strip()
        if not prompt:
            prompt = "こんにちは！お元気ですか？"
            
        # 6. チャットの実行
        chat_with_model(prompt, target_model)

    except SystemExit:
        pass
    except Exception as e:
        logger.exception("処理中に予期せぬエラーが発生したため、異常終了します。")
        sys.exit(1)

if __name__ == "__main__":
    main()
