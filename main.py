import threading
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.insert(0, project_root)

from src.telegram_bot import TelegramUpdateHandler
from src.crash_monitor import CrashGameMonitor
from src.utils import setup_logging

def main():
    setup_logging()

    telegram_handler = TelegramUpdateHandler()

    # Initialize crash game monitor
    crash_monitor = CrashGameMonitor(telegram_handler)

    # Create threads for Telegram updates and crash monitoring
    telegram_thread = threading.Thread(target=telegram_handler.poll_updates, daemon=True)
    crash_monitor_thread = threading.Thread(target=crash_monitor.start, daemon=True)

    # Start threads
    telegram_thread.start()
    crash_monitor_thread.start()

    # Wait for threads to complete (which they won't in this case)
    telegram_thread.join()
    crash_monitor_thread.join()

if __name__ == "__main__":
    main()