import os

# Telegram Bot Configuration
TELEGRAM_API_KEY = os.getenv("API_KEY")
TELEGRAM_CHANNEL_ID = os.getenv("CHANNEL_ID")

# User Agents and Viewport Configurations
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
]

VIEWPORT_RESOLUTIONS = [
    {'width': 1920, 'height': 1080},  # Full HD
    {'width': 1366, 'height': 768},   # Common laptop
    {'width': 1536, 'height': 864},   # Common laptop HiDPI
    {'width': 1440, 'height': 900},   # MacBook
    {'width': 1280, 'height': 720},   # HD
    {'width': 1600, 'height': 900},   # HD+
    {'width': 1680, 'height': 1050},  # WSXGA+
    {'width': 1024, 'height': 768},   # XGA
]


LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s'
}