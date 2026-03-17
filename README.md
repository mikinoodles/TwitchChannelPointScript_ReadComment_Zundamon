# ずんだもん Twitch チャネポ読み上げ

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

Twitch の **チャンネルポイント（チャネポ）交換をトリガーに、VOICEVOX の「ずんだもん」でメッセージを読み上げるツール**です。

視聴者がチャネポを使用してメッセージ付き報酬を交換すると、そのメッセージが **ずんだもんの音声で読み上げられます。**

配信者向けに設計されており、
**exe版を利用すれば Python のインストールは不要です。**

---

# デモ

```
視聴者
   ↓
チャネポ交換
   ↓
Twitch EventSub
   ↓
TTS Queue
   ↓
VOICEVOX
   ↓
ずんだもん音声再生
```

---

# 目次

- 機能
- インストール
- セットアップ
- 設定ファイル
- NGワード設定
- VOICEVOX設定
- OBS音声出力
- トラブルシューティング
- 開発者向け情報

---

# 主な機能

- Twitch EventSub WebSocket 対応
- チャンネルポイント交換で読み上げ
- VOICEVOX によるずんだもん音声合成
- 読み上げキュー処理
- NGワードフィルター
- exe版配布（Python不要）

---

# インストール

最新版は **GitHub Releases** からダウンロードしてください。

```
https://github.com/mikinoodles/TwitchChannelPointScript_ReadComment_Zundamon/releases
```

zip を解凍し、以下を実行します。

```
ZundamonTTSRewardBot.exe
```

---

# セットアップ

初回起動前に設定ファイルを作成します。

```
settings/config.template.json
```

をコピーして

```
settings/config.json
```

を作成してください。

---

# 設定ファイル

例：

```json
{
  "voicevox_settings": {
    "voicevox_path": "{VOICEVOX.exeの絶対パス}",
    "zundamon_id": 3,
    "voicevox_url": "http://127.0.0.1:50021"
  },
  "twitch_settings": {
    "client_id": "{YOUR_CLIENT_ID}",
    "user_access_token": "{YOUR_USER_ACCESS_TOKEN}",
    "broadcaster_user_id": "{YOUR_BROADCASTER_ID}",
    "reward_id": "{TWITCH_REWARD_ID}"
  },
  "delete_wavs_on_program_complete": true
}
```

---

# Twitch 設定

## Client ID

Twitch Developer Consoleで作成します。

https://dev.twitch.tv/console/apps

---

## User Access Token

以下のようなツールで取得できます。

https://twitchtokengenerator.com/

必要スコープ：

```
channel:read:redemptions
```

---

## Broadcaster User ID

以下の API で取得できます。

```
https://api.twitch.tv/helix/users?login=YOUR_TWITCH_NAME
```

---

## Reward ID

Channel Point Reward の ID です。

Twitch API で取得できます。

```
GET https://api.twitch.tv/helix/channel_points/custom_rewards
```

---

# NGワード設定

```
settings/ng_word_list.txt
```

1行につき1ワードで記述します。

例：

```
NGWORD1
NGWORD2
NGWORD3
```

NGワードを含むメッセージは読み上げされません。

---

# VOICEVOX 設定

VOICEVOX をインストールしてください。

公式サイト：

https://voicevox.hiroshiba.jp/

インストール後、`config.json` の

```
voicevox_path
```

に VOICEVOX のパスを指定します。

例：

```
C:/VOICEVOX.exe
```

---

# OBS 音声出力（おすすめ）

配信で使う場合は以下の方法がおすすめです。

### 方法1（簡単）

OBSの

```
Application Audio Capture
```

で `ZundamonTTSRewardBot.exe` をキャプチャ

### 方法2（安定）

仮想オーディオケーブル使用

例：

- VB-Cable
- VoiceMeeter

---

# ディレクトリ構成

```
(Root directory)
│
├─ main.py
├─ ZundamonTTSRewardBot.spec
│
├─ scripts/
│  ├─ config.py
│  ├─ audio_utils.py
│  ├─ file_utils.py
│  ├─ zundamon.py
│  └─ twitch_web_socket.py
│
├─ settings/
│  ├─ config.template.json
│  └─ ng_word_list.txt
│
├─ resources/
└─ _generated/
```

---

# 動作要件

### exe版

- Windows 10 / 11
- VOICEVOX
  - **VOICEVOXの規約に同意した上でご利用ください。**

### Python版

- Python 3.10+
- 必要なライブラリ

---

# exe ビルド（開発者向け）

PyInstaller を使用します。

```
pip install pyinstaller
```

ビルド：

```
pyinstaller --clean ZundamonTTSRewardBot.spec
```

生成場所：

```
dist/ZundamonTTSRewardBot/
```

---

# トラブルシューティング

## 読み上げが動かない

確認項目：

- VOICEVOX が起動できるか
- config.json が正しいか
- Twitch Token が有効か

---

## EventSub が接続できない

以下を確認してください。

- インターネット接続
- Twitch API Token
- client_id

---

# ライセンス

MIT License

---

# 作者

**カップ麺**

Twitch配信向けのツールとして開発しています。

- GitHub: https://github.com/mikinoodles
- Twitch: https://www.twitch.tv/mikinoodles
- X: https://x.com/TonkotsuCupMen

バグ報告・改善提案などは **Issue / Pull Request** からお気軽にどうぞ。
