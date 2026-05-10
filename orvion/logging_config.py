"""
Structured Logging Configuration
JSON logs for production monitoring
"""

import logging
import json
import sys
from datetime import datetime
from typing import Any, Dict
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""

    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcfromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add extra fields
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        if hasattr(record, "duration_ms"):
            log_data["duration_ms"] = record.duration_ms

        return json.dumps(log_data)


def setup_logging():
    """Setup structured logging"""
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVEL)

    # Console handler with JSON formatter
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(LOG_LEVEL)

    json_formatter = JSONFormatter()
    console_handler.setFormatter(json_formatter)

    root_logger.addHandler(console_handler)

    # File handler for errors
    error_file_handler = logging.FileHandler("logs/error.log")
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(json_formatter)
    root_logger.addHandler(error_file_handler)

    # File handler for all logs
    all_file_handler = logging.FileHandler("logs/app.log")
    all_file_handler.setLevel(LOG_LEVEL)
    all_file_handler.setFormatter(json_formatter)
    root_logger.addHandler(all_file_handler)

    return root_logger


def get_logger(name: str) -> logging.Logger:
    """Get logger instance"""
    return logging.getLogger(name)


# Initialize on import
if not os.path.exists("logs"):
    os.makedirs("logs")

setup_logging()
