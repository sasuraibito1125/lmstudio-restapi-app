# restapi-app 対話型改修タスク

ご提供いただいた `/api/v1/models/load` API の仕様を元に、実装を行います。

- [x] `main.py` に `load_model(model_id: str)` 関数を追加し、POST `/models/load` の呼び出しを実装
- [x] `main.py` の `main()` に以下の対話フローを追加
  - [x] コンソールでモデルリストを提示
  - [x] `input()` によるユーザーのモデル選択受け付け
  - [x] 選択されたモデルを `load_model()` でロード
  - [x] ロード完了後、チャット入力待ち（または固定メッセージ）にして `chat_completion()` を実行
- [x] `tests/test_main.py` に `load_model()` 用のモックとテストを追加
- [x] `tests/test_main.py` の `test_main_execution` で `builtins.input` をモック化し、対話的な操作をシミュレーションする
- [x] 単体テスト (start_ut.sh) のパスを確認
