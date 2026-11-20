import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil

class PropertiesEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MC Server Properties Editor")
        self.root.geometry("800x700")
        self.root.configure(bg='#1E1E1E')
        
        # 設定値を保持する変数辞書
        self.properties_vars = {} 
        # UIマッピング定義 (key: (type, label, options/range))
        self.ui_map = {
            # --- ネットワーク設定 ---
            'server-port': ('int', 'サーバーポート', 1, 65535),
            'server-ip': ('str', 'サーバーIP (空白で全Interface)'),
            'max-players': ('int', '最大プレイヤー数', 1, 10000),
            'view-distance': ('int', '描画距離 (Chunks)', 3, 32),
            'simulation-distance': ('int', 'シミュレーション距離', 1, 32),
            'network-compression-threshold': ('int', '圧縮閾値 (-1で無効)', -1, 65535),
            'enable-status': ('bool', 'ステータス応答有効'),
            'broadcast-rcon-to-ops': ('bool', 'RCONメッセージをOPに送信'),
            
            # --- ゲームプレイ設定 ---
            'gamemode': ('enum', 'デフォルトゲームモード', ['survival', 'creative', 'adventure', 'spectator']),
            'difficulty': ('enum', '難易度', ['peaceful', 'easy', 'normal', 'hard']),
            'force-gamemode': ('bool', 'ゲームモード強制'),
            'hardcore': ('bool', 'ハードコアモード'),
            'max-world-size': ('int', '最大ワールドサイズ', 1, 29999984),
            'allow-nether': ('bool', 'ネザー有効'),
            'generate-structures': ('bool', '構造物生成'),
            'spawn-monsters': ('bool', 'モンスター湧き'),
            'spawn-animals': ('bool', '動物湧き'),
            'spawn-npcs': ('bool', '村人湧き'),
            'pvp': ('bool', 'PVP有効'),
            'allow-flight': ('bool', '飛行許可'),
            'enable-command-block': ('bool', 'コマンドブロック有効'),
            'function-permission-level': ('int', '関数権限レベル', 1, 4),
            'op-permission-level': ('int', 'OP権限レベル', 1, 4),
            'entity-broadcast-range-percentage': ('int', 'エンティティ通知範囲(%)', 0, 500),
            'player-idle-timeout': ('int', 'アイドル時キック時間(分)', 0, 10000),
            'sync-chunk-writes': ('bool', 'チャンク書き込み同期'),
            'enable-jmx-monitoring': ('bool', 'JMX監視有効'),
            'rcon.port': ('int', 'RCONポート', 1, 65535),
            'rcon.password': ('str', 'RCONパスワード'),
            'query.port': ('int', 'Queryポート', 1, 65535),
            'enable-query': ('bool', 'Query有効'),
            'use-native-transport': ('bool', 'ネイティブトランスポート使用'),
            'prevent-proxy-connections': ('bool', 'プロキシ接続防止'),
            'enforce-whitelist': ('bool', 'ホワイトリスト強制'),
            'white-list': ('bool', 'ホワイトリスト有効'),
            'online-mode': ('bool', 'オンラインモード (認証)'),
            'prevent-sample-leaks': ('bool', 'サンプル漏洩防止'),
            'hide-online-players': ('bool', 'オンラインプレイヤー非表示'),
            
            # --- ワールド設定 ---
            'level-name': ('str', 'ワールド名'),
            'level-seed': ('str', 'シード値'),
            'level-type': ('enum', 'ワールドタイプ', ['minecraft:normal', 'minecraft:flat', 'minecraft:large_biomes', 'minecraft:amplified', 'minecraft:single_biome_surface']),
            'default-player-game-type': ('enum', '新規プレイヤーGT', ['survival', 'creative', 'adventure', 'spectator']),
            'generator-settings': ('str', 'ジェネレーター設定 (JSON)'),
            'dimension-spawn-settings': ('str', 'ディメンション生成設定'),
            'require-resource-pack': ('bool', 'リソースパック必須'),
            'resource-pack': ('str', 'リソースパックURL'),
            'resource-pack-sha1': ('str', 'リソースパックSHA1'),
            'resource-pack-prompt': ('str', 'リソースパックプロンプト'),
            
            # --- その他 ---
            'motd': ('str', 'サーバー説明文 (Motd)'),
            'log-ips': ('bool', 'IPログ記録'),
            'max-tick-time': ('int', '最大ティック時間(ms)', -1, 100000),
            'debug': ('bool', 'デバッグモード'),
            'broadcast-console-to-ops': ('bool', 'コンソールメッセージをOPに送信'),
            'send-chat-previews': ('bool', 'チャットプレビュー送信'),
            'chat-preview': ('int', 'チャットプレビューモード', 0, 2),
            'enable-rcon': ('bool', 'RCON有効'),
            'initial-enabled-plugins': ('str', '初期有効プラグイン'),
            'initial-disabled-plugins': ('str', '初期無効プラグイン'),
        }

        self.unknown_props = {} # マップにない設定を保持
        self.file_path = ""
        
        self._build_ui()

    def _build_ui(self):
        # トップバー
        top_frame = tk.Frame(self.root, bg='#1E1E1E')
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        btn_open = tk.Button(top_frame, text="📂 server.propertiesを開く", command=self.open_file, bg='#333333', fg='white', relief=tk.FLAT)
        btn_open.pack(side=tk.LEFT)
        
        btn_save = tk.Button(top_frame, text="💾 保存", command=self.save_file, bg='#0078D7', fg='white', relief=tk.FLAT)
        btn_save.pack(side=tk.RIGHT)
        
        # スクロール可能なキャンバス
        canvas = tk.Canvas(self.root, bg='#1E1E1E', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg='#1E1E1E')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # マウスホイール連携
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    def open_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Properties files", "*.properties"), ("All files", "*.*")])
        if not filepath:
            return
            
        self.file_path = filepath
        self.properties_vars = {}
        self.unknown_props = {}
        
        # 既存ウィジェット削除
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        if key in self.ui_map:
                            self._create_widget(key, value)
                        else:
                            self.unknown_props[key] = value
            
            self.root.title(f"Properties Editor - {os.path.basename(filepath)}")
            messagebox.showinfo("完了", f"読み込み完了\n({len(self.properties_vars)}件の設定を検出)")
            
        except Exception as e:
            messagebox.showerror("エラー", f"読み込み失敗:\n{str(e)}")

    def _create_widget(self, key, value):
        config = self.ui_map[key]
        type_ = config[0]
        label_text = config[1]
        
        frame = tk.Frame(self.scrollable_frame, bg='#1E1E1E')
        frame.pack(fill=tk.X, padx=5, pady=2)
        
        lbl = tk.Label(frame, text=f"{label_text} ({key})", fg='white', bg='#1E1E1E', anchor='w', width=35)
        lbl.pack(side=tk.LEFT)
        
        var = None
        widget = None
        
        if type_ == 'bool':
            var = tk.BooleanVar(value=value.lower() == 'true')
            widget = tk.Checkbutton(frame, variable=var, bg='#1E1E1E', fg='white', selectcolor='#333333', activebackground='#1E1E1E')
            widget.pack(side=tk.RIGHT)
        elif type_ == 'int':
            min_val, max_val = config[2], config[3]
            var = tk.IntVar(value=int(value))
            widget = ttk.Spinbox(frame, from_=min_val, to=max_val, textvariable=var, width=10)
            widget.pack(side=tk.RIGHT)
        elif type_ == 'enum':
            options = config[2]
            var = tk.StringVar(value=value)
            widget = ttk.Combobox(frame, textvariable=var, values=options, state="readonly", width=20)
            widget.pack(side=tk.RIGHT)
        elif type_ == 'str':
            var = tk.StringVar(value=value)
            widget = tk.Entry(frame, textvariable=var, bg='#333333', fg='white', insertbackground='white', width=30)
            widget.pack(side=tk.RIGHT)
            
        if var:
            self.properties_vars[key] = var

    def save_file(self):
        if not self.file_path:
            messagebox.showwarning("警告", "ファイルが開かれていません")
            return
            
        try:
            # バックアップ作成
            backup_path = self.file_path + ".bak"
            shutil.copy2(self.file_path, backup_path)
            
            with open(self.file_path, 'w', encoding='utf-8') as f:
                # 既知の設定を書き込み
                for key, var in self.properties_vars.items():
                    if isinstance(var, tk.BooleanVar):
                        val = str(var.get()).lower()
                    elif isinstance(var, (tk.IntVar, tk.StringVar)):
                        val = str(var.get())
                    else:
                        val = str(var)
                    f.write(f"{key}={val}\n")
                
                # 未知の設定もそのまま書き戻す
                for key, val in self.unknown_props.items():
                    f.write(f"{key}={val}\n")
                    
            messagebox.showinfo("完了", "保存しました！\n(バックアップ作成済み)")
            
        except Exception as e:
            messagebox.showerror("エラー", f"保存失敗:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PropertiesEditorApp(root)
    root.mainloop()