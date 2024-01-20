import csv
import os
import random
import logging
import math
import requests
from datetime import datetime
from config.config import USER_AGENTS, VIEWPORT_RESOLUTIONS, TELEGRAM_API_KEY, TELEGRAM_CHANNEL_ID

class CSVLogger:
    def __init__(self, filename='crash_game_data.csv'):
        self.filename = filename
        self._ensure_csv_exists()

    def _ensure_csv_exists(self):
        """Create CSV file with headers if it doesn't exist"""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([
                    'Timestamp', 
                    'Game ID', 
                    'Multiplier'
                ])

    def log_crash_data(self, game_id, multiplier):
        """Log crash game data to CSV"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Write to CSV
        with open(self.filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                timestamp, 
                game_id, 
                f"{multiplier:.2f}x"
            ])

def setup_logging():
    """Configure logging settings"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def get_random_viewport():
    """Generate a slightly randomized viewport size based on common resolutions"""
    base_viewport = random.choice(VIEWPORT_RESOLUTIONS)
    width = base_viewport['width'] + random.randint(-10, 10)
    height = base_viewport['height'] + random.randint(-10, 10)
    return {'width': width, 'height': height}

def send_telegram_message(message):
    """Send message to Telegram channel"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHANNEL_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            logging.info("Message sent successfully")
            return True
    except Exception as e:
        logging.error(f"Error sending message: {str(e)}")
    return False

def check_alert_conditions(multiplier, command_data):
    """Check if crash multiplier meets alert conditions"""
    command = command_data['command']
    number = command_data['number']
    
    if command and number is not None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_multiplier = f"{math.floor(multiplier * 100) / 100:.2f}"
        
        alert_triggered = False
        
        if command == "under" and multiplier < number:
            alert_triggered = True
        elif command == "above" and multiplier > number:
            alert_triggered = True
        elif command == "equal" and abs(multiplier - number) < 0.0000001:  
            alert_triggered = True
            
        if alert_triggered:
            alert_message = (
                f"📊 <b>MULTIPLIER {formatted_multiplier}x</b>\n\n"
                f"⏰ Time: {timestamp}\n\n"
                f"🎯 Condition met: {command} {number}x"
            )
            send_telegram_message(alert_message)