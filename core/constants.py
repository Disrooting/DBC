"""
=========================================================
 Discord Desktop Client V2
 constants.py

 Global application constants.

 This file should NEVER import any project modules.
 Only standard library modules may be imported here.
=========================================================
"""

from pathlib import Path

# =========================================================
# APP INFO
# =========================================================

APP_NAME = "Discord Desktop Client"

APP_VERSION = "2.0.0"

APP_AUTHOR = "Shadow Project"

# =========================================================
# PATHS
# =========================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

ASSETS_DIR = ROOT_DIR / "assets"

LOGS_DIR = ROOT_DIR / "logs"

CONFIG_FILE = ROOT_DIR / "bot_config.json"

CACHE_DIR = ROOT_DIR / "cache"

AVATAR_CACHE = CACHE_DIR / "avatars"

IMAGE_CACHE = CACHE_DIR / "images"

TEMP_DIR = CACHE_DIR / "temp"

# Create directories automatically

for folder in (
    LOGS_DIR,
    CACHE_DIR,
    AVATAR_CACHE,
    IMAGE_CACHE,
    TEMP_DIR,
):
    folder.mkdir(parents=True, exist_ok=True)

# =========================================================
# WINDOW
# =========================================================

WINDOW_WIDTH = 1450

WINDOW_HEIGHT = 850

WINDOW_MIN_WIDTH = 1200

WINDOW_MIN_HEIGHT = 650

# =========================================================
# REFRESH RATES
# =========================================================

UI_REFRESH = 20

STATUS_REFRESH = 500

MEMBER_REFRESH = 1000

CACHE_SAVE_INTERVAL = 60

# =========================================================
# CACHE
# =========================================================

MESSAGE_CACHE_LIMIT = 500

IMAGE_CACHE_LIMIT = 250

MAX_HISTORY_LOAD = 100

# =========================================================
# UPLOADS
# =========================================================

MAX_UPLOAD_SIZE = 8 * 1024 * 1024

SUPPORTED_IMAGE_TYPES = (
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".bmp",
    ".webp",
)

# =========================================================
# COLORS
# =========================================================

COLOR_BACKGROUND = "#313338"

COLOR_PANEL = "#2B2D31"

COLOR_PANEL_DARK = "#1E1F22"

COLOR_INPUT = "#383A40"

COLOR_BLURPLE = "#5865F2"

COLOR_GREEN = "#23A55A"

COLOR_RED = "#ED4245"

COLOR_ORANGE = "#FAA61A"

COLOR_TEXT = "#DBDEE1"

COLOR_SUBTEXT = "#949BA4"

COLOR_OFFLINE = "#5C6169"

# =========================================================
# MEMBER STATUS COLORS
# =========================================================

STATUS_COLORS = {

    "online": "#23A55A",

    "idle": "#FAA61A",

    "dnd": "#ED4245",

    "offline": "#5C6169",

    "invisible": "#5C6169",

}

# =========================================================
# FONTS
# =========================================================

FONT_TITLE = ("Segoe UI", 18, "bold")

FONT_HEADER = ("Segoe UI", 14, "bold")

FONT_NORMAL = ("Segoe UI", 13)

FONT_SMALL = ("Segoe UI", 11)

FONT_CONSOLE = ("Consolas", 12)

# =========================================================
# ICONS
# =========================================================

ICON_CONNECT = "🟢"

ICON_DISCONNECT = "🔴"

ICON_UPLOAD = "📤"

ICON_DOWNLOAD = "📥"

ICON_FOLDER = "📁"

ICON_CHANNEL = "#"

ICON_MEMBER = "👤"

ICON_BOT = "🤖"

ICON_WARNING = "⚠"

ICON_ERROR = "❌"

ICON_SUCCESS = "✅"

ICON_LOADING = "🔄"

# =========================================================
# NETWORK
# =========================================================

CONNECTION_TIMEOUT = 30

REQUEST_TIMEOUT = 15

RECONNECT_DELAY = 5

MAX_RECONNECT_ATTEMPTS = 999999

# =========================================================
# IMAGE SETTINGS
# =========================================================

IMAGE_PREVIEW_SIZE = 220

AVATAR_SIZE = 64

# =========================================================
# SEARCH
# =========================================================

SEARCH_HISTORY_LIMIT = 50

# =========================================================
# LOGGING
# =========================================================

LOG_FILE_NAME = "client.log"

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(name)s | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# =========================================================
# THEME
# =========================================================

DEFAULT_THEME = "dark"

AVAILABLE_THEMES = (
    "dark",
    "light",
)

# =========================================================
# DEFAULT CONFIG
# =========================================================

DEFAULT_CONFIG = {

    "token": "",

    "theme": DEFAULT_THEME,

    "remember_token": True,

    "show_notifications": True,

    "play_sound": True,

    "auto_reconnect": True,

    "load_history": True,

    "history_limit": MAX_HISTORY_LOAD,

    "cache_messages": True,

}