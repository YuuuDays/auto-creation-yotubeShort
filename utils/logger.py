# utils/logger.py

import logging
import os

# ログレベル設定（必要に応じて変更）
LOG_LEVEL = logging.DEBUG

# ログフォーマット
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

# ログファイル出力先（存在しない場合は作成）
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# ロガーの設定関数（他のモジュールから使う用）
def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    if not logger.handlers:  # ハンドラの重複を防ぐ
        # コンソール出力
        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(ch)

        # ファイル出力
        fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
        fh.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(fh)

    return logger
