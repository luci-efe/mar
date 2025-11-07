"""
Input handler module for detecting and processing user input.
Supports keyboard input with debouncing to prevent multiple triggers.
"""

import time
from typing import Callable, Optional

import pygame

from config import INPUT_TRIGGER_KEY, DEBOUNCE_TIME


class InputHandler:
    """
    Handles input detection with debouncing.

    Phase 1: Detects spacebar presses using pygame events.
    Phase 2: Can be extended to support Makey Makey touch inputs.
    """

    def __init__(
        self,
        trigger_key: str = INPUT_TRIGGER_KEY,
        debounce_time: float = DEBOUNCE_TIME,
    ):
        """
        Initialize the input handler.

        Args:
            trigger_key: The key that triggers video playback.
            debounce_time: Minimum time between triggers in seconds.
        """
        self.trigger_key = trigger_key
        self.debounce_time = debounce_time
        self._last_trigger_time = 0.0
        self._trigger_callback: Optional[Callable[[], None]] = None

        # Map key names to pygame key constants
        self._key_map = {
            "space": pygame.K_SPACE,
            "enter": pygame.K_RETURN,
            "up": pygame.K_UP,
            "down": pygame.K_DOWN,
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT,
        }

    def set_trigger_callback(self, callback: Callable[[], None]) -> None:
        """
        Set the callback function to be called when a trigger occurs.

        Args:
            callback: Function to call when input is triggered.
        """
        self._trigger_callback = callback

    def process_events(self, events: list) -> None:
        """
        Process pygame events and check for trigger inputs.

        Args:
            events: List of pygame events to process.
        """
        current_time = time.time()

        for event in events:
            if event.type == pygame.KEYDOWN:
                # Check if this is the trigger key
                trigger_key_code = self._key_map.get(
                    self.trigger_key.lower(), pygame.K_SPACE
                )

                if event.key == trigger_key_code:
                    # Check debounce
                    time_since_last = current_time - self._last_trigger_time
                    if time_since_last >= self.debounce_time:
                        self._last_trigger_time = current_time
                        if self._trigger_callback:
                            self._trigger_callback()

    def is_debouncing(self) -> bool:
        """
        Check if we're currently in the debounce period.

        Returns:
            True if within debounce period, False otherwise.
        """
        return (
            time.time() - self._last_trigger_time < self.debounce_time
        )
