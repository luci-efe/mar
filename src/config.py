"""
Configuration module for the interactive video playback system.
Centralizes all configurable settings to avoid hardcoding values.
"""

from pathlib import Path
from typing import Tuple

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Video settings
VIDEOS_DIR = PROJECT_ROOT / "videos"
SUPPORTED_FORMATS = (".mp4", ".avi", ".mov")

# Display settings
FULLSCREEN = True
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60
BACKGROUND_COLOR = (0, 0, 0)  # Black

# Screensaver settings
SCREENSAVER_TIMEOUT = 10.0  # Seconds of inactivity before screensaver
SCREENSAVER_TEXT = "Touch to play..."
SCREENSAVER_TEXT_COLOR = (255, 255, 255)  # White
SCREENSAVER_FONT_SIZE = 72

# Input settings
INPUT_TRIGGER_KEY = "space"  # Phase 1: spacebar trigger
DEBOUNCE_TIME = 0.3  # Minimum seconds between input triggers

# Playback settings
QUEUE_INPUTS = False  # If True, queue inputs during playback; if False, ignore
