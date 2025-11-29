"""
Shared utility functions for the multi-agent system.
Includes logging, time utilities, and common helper functions.
"""
import logging
from datetime import datetime
from typing import Any, Dict, Optional
import json
from pathlib import Path


def setup_logger(name: str, level: str = "INFO") -> logging.Logger:
    """
    Set up a logger with standard formatting.
    
    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


def get_utc_timestamp() -> str:
    """
    Get current UTC timestamp in ISO format with Z suffix.
    
    Returns:
        ISO format timestamp string (e.g., "2025-10-12T22:25:58Z")
    """
    return datetime.utcnow().isoformat() + "Z"


def load_json_file(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Load JSON data from a file.
    
    Args:
        file_path: Path to JSON file
    
    Returns:
        Parsed JSON data or None if file doesn't exist or is invalid
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return None
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logging.error(f"Error loading JSON file {file_path}: {e}")
        return None


def save_json_file(file_path: str, data: Dict[str, Any], indent: int = 2) -> bool:
    """
    Save data to a JSON file.
    
    Args:
        file_path: Path to save JSON file
        data: Data dictionary to save
        indent: JSON indentation level
    
    Returns:
        True if successful, False otherwise
    """
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        return True
    except (IOError, TypeError) as e:
        logging.error(f"Error saving JSON file {file_path}: {e}")
        return False


def validate_message_structure(message: Dict[str, Any]) -> bool:
    """
    Validate that a message follows the required structure.
    
    Args:
        message: Message dictionary to validate
    
    Returns:
        True if valid, False otherwise
    """
    required_fields = ["message_id", "sender", "recipient", "type", "timestamp"]
    return all(field in message for field in required_fields)

