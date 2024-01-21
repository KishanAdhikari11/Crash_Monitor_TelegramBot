import time
import logging
import re
import random
import requests
from src.utils import send_telegram_message


class TelegramUpdateHandler:
    def __init__(self):
        self.command_data = {
            'command': None,
            'number': None
        }

    def handle_command(self, update):
        """Handle incoming command messages"""
        try:
            if 'message' in update:
                message_text = update['message'].get('text', '')
                
                match = re.match(r'^/(under|above|equal)\s+([\d.]+)$', message_text.lower())
                if match:
                    command, number_str = match.groups()
                    number = float(number_str)
                    
                    self.command_data['command'] = command
                    self.command_data['number'] = number
                    
                    self._send_telegram_message(
                        f"✅ Alert set!\n"
                        f"Will notify when crash is {command} {number}x"
                    )
                    logging.info(f"Command set: {command} {number}")
                    
                elif message_text == "/cancel":
                    self.command_data['command'] = None
                    self.command_data['number'] = None
                    self._send_telegram_message("❌ Alerts cancelled")
                    
        except Exception as e:
            logging.error(f"Error handling command: {str(e)}")

    def _send_telegram_message(self, message):
        """Send message to Telegram channel"""
        from utils import send_telegram_message
        return send_telegram_message(message)

    def get_updates(self, offset=None):
        """Get updates from Telegram"""
        from config.config import TELEGRAM_API_KEY
        url = f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/getUpdates"
        params = {"timeout": 100}
        if offset:
            params["offset"] = offset
        
        try:
            response = requests.get(url, params=params)
            return response.json()
        except Exception as e:
            logging.error(f"Error getting updates: {str(e)}")
            return {"ok": False}

    def poll_updates(self):
        """Poll for updates from Telegram"""
        offset = None
        while True:
            try:
                updates = self.get_updates(offset)
                if updates.get('ok'):
                    for update in updates['result']:
                        self.handle_command(update)
                        offset = update['update_id'] + 1
                time.sleep(random.uniform(1, 2))  # Random delay between polls
            except Exception as e:
                logging.error(f"Error in polling: {str(e)}")
                time.sleep(random.uniform(3, 6))  # Random delay on error