# マイクからの音声をAzure OpenAI サービスの Whisper API でほぼリアルタイムに文字起こしするサンプル コード

## 概要

このプロジェクトは、マイクからの音声をリアルタイムで録音し、Azure OpenAI Whisperモデルによってテキストに変換するPythonアプリケーションです。音声は一定の時間間隔で自動的に処理され、文字起こし結果がファイルとして保存されます。

## 特徴

- リアルタイムの音声録音
- 自動的な音声チャンク分割と保存
- Azure OpenAI Whisperモデルによる高精度な文字起こし
- 日本語対応
- 文字起こし結果のリアルタイム表示と自動保存

## 必要要件

- Python 3.8以上
- Azure OpenAIアカウントとAPI設定
- 以下のPythonパッケージ：
  ```
  python-dotenv==1.0.0
  openai==0.28.1
  PyAudio==0.2.14
  ```

## セットアップ手順

1. リポジトリのクローン：
   ```bash
   git clone https://github.com/potofo/realtime-transcription.git
   cd realtime-transcription
   ```

2. 依存パッケージのインストール：
   ```bash
   pip install -r requirements.txt
   ```

3. 環境変数の設定：
   - `.env_template`を`.env`にコピー
   - 以下の項目を設定：
     ```
     OPENAI_API_TYPE=azure
     OPENAI_API_HOST=your_endpoint_here
     OPENAI_API_KEY=your_api_key_here
     OPENAI_API_VERSION=2024-06-01
     AZURE_DEPLOYMENT_ID=whisper
     
     # 音声録音設定
     AUDIO_CHUNK_SECONDS=25  # チャンクサイズ（秒）
     ```
     ※Azure OpenAIのwhisperにはレイト制限(1分間あたりの要求制限＝3)があるため、AUDIO_CHUNK_SECONDSを21秒以下にするとAPIがエラーを応答します。
## 使用方法

1. アプリケーションの起動：
   ```bash
   python realtime_transcription.py
   ```

2. 操作方法：
   - プログラム起動後、自動的に録音が開始されます
   - 音声は設定された時間間隔（デフォルト25秒）でチャンクに分割されます
   - 各チャンクは自動的に文字起こしされ、結果が表示されます
   - 終了するには`Ctrl+C`を押してください

## ファイル構造

```
realtime-transcription/
├── realtime_transcription.py  # メインスクリプト
├── requirements.txt           # 依存パッケージリスト
├── .env_template             # 環境変数テンプレート
├── audio/                    # 録音された音声ファイルの保存先
└── transcription/           # 文字起こし結果の保存先
```

## 出力ファイル

- 音声ファイル：`audio/chunk_[タイムスタンプ]_[連番].wav`
- 文字起こし結果：`transcription/chunk_[タイムスタンプ]_[連番].txt`

## エラー処理

- 音声デバイスの接続エラー
- API通信エラー
- ファイル保存エラー

各種エラーは適切にハンドリングされ、エラーメッセージが表示されます。

## ライセンス

MIT License

## 注意事項

- 十分な音声入力デバイス（マイク）が必要です
- 安定したインターネット接続が必要です
- Azure OpenAI APIの利用料金が発生する可能性があります

## 貢献

バグ報告や機能改善の提案は、IssuesまたはPull Requestsにて受け付けています。

---