import logging
import logging.handlers
import os
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import sys

class CustomJSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
            "level": record.levelname,
            "logger": record.name,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "message": record.getMessage(),
        }
        
        # Add extra fields if they exist
        if hasattr(record, 'extra'):
            log_data.update(record.extra)
            
        # Add exception info if it exists
        if record.exc_info:
            log_data['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': self.formatException(record.exc_info)
            }
            
        return json.dumps(log_data)

class CustomTextFormatter(logging.Formatter):
    """Custom text formatter for human-readable logs"""
    def format(self, record: logging.LogRecord) -> str:
        # Format: [TIMESTAMP] LEVEL [LOGGER_NAME] [MODULE:FUNCTION:LINE] - MESSAGE
        timestamp = datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        log_level = f"{record.levelname:<8}"  # Left-aligned, 8 chars
        logger_name = f"[{record.name}]"
        location = f"[{record.module}:{record.funcName}:{record.lineno}]"
        
        # Format the main message
        message = record.getMessage()
        
        # Add exception info if it exists
        if record.exc_info:
            message += f"\nException: {self.formatException(record.exc_info)}"
            
        return f"[{timestamp}] {log_level} {logger_name} {location} - {message}"

class LoggerManager:
    """Manager class for handling multiple loggers with consistent configuration"""
    
    _instance = None
    _loggers: Dict[str, logging.Logger] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggerManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the logger manager and create log directories"""
        self.LOGS_DIR = Path(__file__).parent.parent / "logs"
        self.LOGS_DIR.mkdir(exist_ok=True)
        
        # Define log directories and create them
        self.APP_LOGS_DIR = self.LOGS_DIR / "application"
        self.ERROR_LOGS_DIR = self.LOGS_DIR / "errors"
        self.AUDIT_LOGS_DIR = self.LOGS_DIR / "audit"
        
        for directory in [self.APP_LOGS_DIR, self.ERROR_LOGS_DIR, self.AUDIT_LOGS_DIR]:
            directory.mkdir(exist_ok=True)
    
    def get_logger(
        self,
        name: str,
        log_level: int = logging.INFO,
        log_to_console: bool = True,
        log_to_file: bool = True,
        json_format: bool = False,
        log_type: str = "application"
    ) -> logging.Logger:
        """
        Get or create a logger with the specified configuration
        
        Args:
            name: Name of the logger
            log_level: Logging level (default: INFO)
            log_to_console: Whether to log to console (default: True)
            log_to_file: Whether to log to file (default: True)
            json_format: Whether to use JSON format (default: False)
            log_type: Type of log (application/errors/audit) (default: application)
            
        Returns:
            logging.Logger: Configured logger instance
        """
        if name in self._loggers:
            return self._loggers[name]
            
        logger = logging.getLogger(name)
        logger.setLevel(log_level)
        
        # Prevent adding handlers multiple times
        if logger.handlers:
            return logger
            
        # Choose the appropriate formatter
        formatter = CustomJSONFormatter() if json_format else CustomTextFormatter()
        
        # Console Handler
        if log_to_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        
        # File Handler
        if log_to_file:
            log_dir = getattr(
                self,
                {
                    "application": "APP_LOGS_DIR",
                    "errors": "ERROR_LOGS_DIR",
                    "audit": "AUDIT_LOGS_DIR"
                }.get(log_type.lower(), "APP_LOGS_DIR")  # Default to APP_LOGS_DIR
            )

            current_date = datetime.now().strftime("%Y-%m-%d")
            log_file = log_dir / f"{name}_{current_date}.log"
            
            # Create rotating file handler
            file_handler = logging.handlers.RotatingFileHandler(
                filename=log_file,
                maxBytes=10*1024*1024,  # 10MB
                backupCount=30,  # Keep 30 days of logs
                encoding='utf-8'
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            
            # Add error file handler for ERROR and above
            if log_level <= logging.ERROR:
                error_log_file = self.ERROR_LOGS_DIR / f"{name}_errors_{current_date}.log"
                error_handler = logging.handlers.RotatingFileHandler(
                    filename=error_log_file,
                    maxBytes=10*1024*1024,
                    backupCount=30,
                    encoding='utf-8'
                )
                error_handler.setLevel(logging.ERROR)
                error_handler.setFormatter(formatter)
                logger.addHandler(error_handler)
        
        self._loggers[name] = logger
        return logger

# Create a global logger manager instance
logger_manager = LoggerManager()

def get_logger(
    name: str,
    log_level: int = logging.INFO,
    log_to_console: bool = True,
    log_to_file: bool = True,
    json_format: bool = False,
    log_type: str = "application"
) -> logging.Logger:
    """
    Convenience function to get a logger with the specified configuration
    
    Args:
        name: Name of the logger
        log_level: Logging level (default: INFO)
        log_to_console: Whether to log to console (default: True)
        log_to_file: Whether to log to file (default: True)
        json_format: Whether to use JSON format (default: False)
        log_type: Type of log (application/errors/audit) (default: application)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    return logger_manager.get_logger(
        name=name,
        log_level=log_level,
        log_to_console=log_to_console,
        log_to_file=log_to_file,
        json_format=json_format,
        log_type=log_type
    )

# Example usage
if __name__ == "__main__":
    # Get different types of loggers
    app_logger = get_logger("app", log_type="application")
    error_logger = get_logger("errors", log_type="errors", log_level=logging.ERROR)
    audit_logger = get_logger("audit", log_type="audit", json_format=True)
    
    # Example log messages
    app_logger.debug("This is a debug message")
    app_logger.info("This is an info message")
    app_logger.warning("This is a warning message")
    
    try:
        1/0
    except Exception as e:
        error_logger.error("An error occurred", exc_info=True)
    
    audit_logger.info("User action performed", extra={
        "user_id": "123",
        "action": "login",
        "ip_address": "192.168.1.1"
    }) 