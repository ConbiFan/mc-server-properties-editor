# MC Server Properties Editor

A lightweight, privacy-focused GUI tool to safely edit Minecraft `server.properties` files.

![Demo](demo.gif) <!-- 動作GIFがあればここに貼る -->

## 🚀 Features

- **Safe Editing**: GUI-based editor prevents syntax errors in `server.properties`.
- **Auto Backup**: Automatically creates a `.bak` backup before saving changes.
- **Validation**: Input validation for integers (port, max-players, etc.) and enums (gamemode, difficulty).
- **Unknown Props Preserved**: Settings not in the UI map are kept intact on save.
- **Dark Theme**: Native dark UI matching modern IDE aesthetics.
- **Privacy First**: No internet connection required. All processing is done locally on your PC.
- **Open Source**: Written in Python with tkinter. Verify the code yourself for safety.
- **No KYC/Account**: Purchase the standalone executable without providing personal information.

## 🛒 Download

| Version | Description | Link |
| :--- | :--- | :--- |
| **Standalone (exe)** | No Python installation required. Ready to use. | [Buy on Sell.app](https://conbifan.sell.app/product/mc-server-properties-editor) |
| **Source Code** | For developers who want to inspect or modify the code. | Free (This Repository) |

> 💰 **Accepted Payments**: Cryptocurrency only (USDT, XMR, BTC, etc.) via [NowPayments](https://nowpayments.io/donation/conbifan).

## 💻 How to Run from Source

If you have Python installed, you can run this tool for free.

### Requirements
- Python 3.10+
- `tkinter` (Usually included with Python on Windows/macOS)
- No external dependencies required!

### Installation
1. Clone this repository:
    ```bash
    git clone https://github.com/ConbiFan/mc-server-properties-editor.git
    cd mc-server-properties-editor
    ```
2. Run the application:
    ```bash
    python src\PropertiesEditor.py
    ```

## 📝 Supported Properties

| Property | Type | Description |
| :--- | :--- | :--- |
| `server-port` | int (1-65535) | サーバーポート |
| `max-players` | int (1-10000) | 最大プレイヤー数 |
| `view-distance` | int (3-32) | 描画距離 (Chunks) |
| `simulation-distance` | int (1-32) | シミュレーション距離 |
| `gamemode` | enum | デフォルトゲームモード |
| `difficulty` | enum | 難易度 |
| `level-name` | str | ワールド名 |
| `level-seed` | str | シード値 |
| `motd` | str | サーバー説明文 |
| `online-mode` | bool | オンラインモード (認証) |
| `white-list` | bool | ホワイトリスト有効 |
| `enforce-whitelist` | bool | ホワイトリスト強制 |
| `pvp` | bool | PVP有効 |
| `allow-flight` | bool | 飛行許可 |
| `enable-command-block` | bool | コマンドブロック有効 |
| `hardcore` | bool | ハードコアモード |
| `spawn-monsters` | bool | モンスター湧き |
| `spawn-animals` | bool | 動物湧き |
| `rcon.port` | int (1-65535) | RCONポート |
| `enable-rcon` | bool | RCON有効 |

*Full list includes 60+ properties across network, gameplay, world, and misc categories.*

## 🛡️ Security & Trust

- **Open Source**: The entire source code is available in this repository. You can check for any malicious behavior.
- **Local Processing**: This tool does not send any data to external servers. Your server configuration remains private.
- **Backup Safety**: A `.bak` file is automatically created before every save operation.
- **Anonymous Purchase**: Buy the executable version on Sell.app without revealing your identity.

## 🤝 Support My Work

I am an independent developer. If you find this tool useful, please consider supporting me via Cryptocurrency.

- 🛒 **Shop**: [https://conbifan.sell.app](https://conbifan.sell.app)
- 💰 **Donate**: [https://nowpayments.io/donation/conbifan](https://nowpayments.io/donation/conbifan)

## 📜 License

MIT License. Feel free to use, modify, and distribute.
