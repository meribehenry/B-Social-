import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(app_name):
    # 1. Create the logger
    logger = logging.getLogger(app_name)
   
    # We set the base level to INFO so it ignores spammy DEBUG messages
    logger.setLevel(logging.INFO)

    # 2. Define the Format (The "Security Camera Timestamp")
    # Example output: 2026-08-07 21:30:43,123 - [ERROR] - Failed to connect to Brevo API
    formatter = logging.Formatter(
        '%(asctime)s - [%(levelname)s] - %(message)s'
    )

    # 3. PRODUCTION SETUP: Write to a file
    # We use RotatingFileHandler. If the log file reaches 5 Megabytes,
    # it creates a new file (up to 3 backups) so it doesn't fill up the server's hard drive!
    if os.environ.get("FLASK_CONFIG") == "production":
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler(
            'logs/app_activity.log', maxBytes=5000000, backupCount=3
        )
        file_handler.setFormatter(formatter)
        # Only write WARNING, ERROR, and CRITICAL to the file to save space
        file_handler.setLevel(logging.WARNING)
    
        logger.addHandler(file_handler)

    # 4. DEVELOPMENT SETUP: Print to the console (Terminal)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


