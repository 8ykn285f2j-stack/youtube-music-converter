"""Logging configuration for YouTube Music Converter"""

import logging
import os
from pathlib import Path
from datetime import datetime


def setup_logger(name=None, level=logging.INFO):
    """
    Configure logging for the application.
    
    Args:
        name: Logger name (default: root logger)
        level: Logging level (default: INFO)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create logs directory if it doesn't exist
    log_dir = Path.home() / ".youtube-music-converter" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Create formatters and handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    
    # File handler
    log_file = log_dir / f"converter_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # Add handlers to logger
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return logger


# Create application logger
app_logger = setup_logger("youtube-music-converter")
