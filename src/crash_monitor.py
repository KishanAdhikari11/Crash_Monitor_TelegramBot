import time
import logging
import random
from playwright.sync_api import sync_playwright

from config.config import USER_AGENTS
from src.utils import get_random_viewport, check_alert_conditions, CSVLogger

class CrashGameMonitor:
    def __init__(self, telegram_handler):
        self.telegram_handler = telegram_handler
        self.last_game_id = None
        self.csv_logger = CSVLogger()  
    def get_crash_data(self, page):
        """Get crash game data and check conditions"""
        try:
            query = """
            query CrashGameListHistory($limit: Int, $offset: Int) {
              crashGameList(limit: $limit, offset: $offset) {
                id
                startTime
                crashpoint
                hash {
                  id
                  hash
                  __typename
                }
                __typename
              }
            }
            """
            
            payload = {
                "query": query,
                "operationName": "CrashGameListHistory",
                "variables": {
                    "limit": 1,
                    "offset": 0
                }
            }
            
            response = page.evaluate("""
                async (payload) => {
                    const response = await fetch('https://stake.games/_api/graphql', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(payload)
                    });
                    return await response.json();
                }
            """, payload)
            
            latest_game = response['data']['crashGameList'][0]
            current_game_id = latest_game['id']
            
            if current_game_id != self.last_game_id:
                multiplier = float(latest_game['crashpoint'])
                logging.info(f"New crash point: {multiplier}x")
                check_alert_conditions(multiplier, self.telegram_handler.command_data)
                self.csv_logger.log_crash_data(current_game_id,multiplier)
                self.last_game_id = current_game_id
                
        except Exception as e:
            logging.error(f"Error getting crash data: {str(e)}")


 
    def run_monitoring(self):
        """Run continuous monitoring"""
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(
                    headless=True,
                    args=[
                        '--no-sandbox',
                        '--disable-setuid-sandbox',
                        '--disable-dev-shm-usage',
                        '--disable-accelerated-2d-canvas',
                        '--disable-gpu'
                    ]
                )
                
                context = browser.new_context(
                    viewport=get_random_viewport(),
                    user_agent=random.choice(USER_AGENTS),
                    device_scale_factor=random.choice([1, 1.25, 1.5, 2]),
                    bypass_csp=True,
                    ignore_https_errors=True,
                    locale='en-US',
                    timezone_id='America/New_York'  
                )
                
                try:
                    page = context.new_page()
                    
                    page.goto(
                        'https://stake.games/casino/games/crash',
                        wait_until='networkidle',
                        timeout=60000
                    )
                    
                    page.wait_for_timeout(random.randint(2000, 4000))
                    
                    while True:
                        try:
                            self.get_crash_data(page)
                            time.sleep(random.uniform(3, 5))
                        except Exception as data_error:
                            logging.error(f"Error getting crash data: {str(data_error)}")
                            time.sleep(random.uniform(5, 10))
                            
                except Exception as page_error:
                    logging.error(f"Page error: {str(page_error)}")
                finally:
                    page.close()
                        
            except Exception as browser_error:
                logging.error(f"Browser error: {str(browser_error)}")
            finally:
                context.close()
                browser.close()

    def start(self):
        """Wrapper method to continuously run monitoring"""
        while True:
            try:
                self.run_monitoring()
            except Exception as e:
                logging.error(f"Error in crash monitoring: {str(e)}")
                time.sleep(random.uniform(10, 20))