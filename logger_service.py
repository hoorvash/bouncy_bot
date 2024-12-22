import logging
import os
from datetime import datetime
from pathlib import Path

class LoggerService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggerService, cls).__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance
    
    def _initialize_logger(self):
        """Initialize the logger with file and console handlers"""
        self.logger = logging.getLogger('BouncyBot')
        self.logger.setLevel(logging.INFO)
        
        # Create logs directory if it doesn't exist
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Create file handler with current date
        current_date = datetime.now().strftime('%Y-%m-%d')
        file_handler = logging.FileHandler(
            f"logs/bouncy_bot_{current_date}.log",
            encoding='utf-8'
        )
        file_handler.setLevel(logging.INFO)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message: str):
        """Log info level message"""
        self.logger.info(message)
    
    def error(self, message: str, exc_info=None):
        """Log error level message with optional exception info"""
        self.logger.error(message, exc_info=exc_info)
    
    def warning(self, message: str):
        """Log warning level message"""
        self.logger.warning(message) 