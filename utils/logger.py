import logging
import sys
from datetime import datetime
import os

class Logger:
    _instance = None
    
    @staticmethod
    def get_logger():
        if Logger._instance is None:
            # Create logs directory if it doesn't exist
            if not os.path.exists('logs'):
                os.makedirs('logs')
                
            # Configure logging
            logger = logging.getLogger('TruthAISwarm')
            logger.setLevel(logging.DEBUG)
            
            # Create formatters
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            
            # File handler for all logs
            file_handler = logging.FileHandler(
                f'logs/app_{datetime.now().strftime("%Y%m%d")}.log'
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            
            # Stream handler for console
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setLevel(logging.INFO)
            stream_handler.setFormatter(formatter)
            
            # Add handlers
            logger.addHandler(file_handler)
            logger.addHandler(stream_handler)
            
            Logger._instance = logger
            
        return Logger._instance 