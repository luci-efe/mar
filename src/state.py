"""
State machine module for managing application states.
Tracks and transitions between different states: IDLE, PLAYING, SCREENSAVER.
"""

from enum import Enum, auto
from typing import Optional


class AppState(Enum):
    """Application states for the video playback system."""

    IDLE = auto()  # Just started or finished playing, before screensaver
    SCREENSAVER = auto()  # Displaying screensaver after timeout
    PLAYING = auto()  # Currently playing a video


class StateManager:
    """
    Manages the application state and transitions.

    The state flow is:
    IDLE -> SCREENSAVER (after timeout)
    SCREENSAVER -> PLAYING (on input)
    PLAYING -> IDLE (after video completes)
    IDLE -> PLAYING (on input before screensaver activates)
    """

    def __init__(self, initial_state: AppState = AppState.IDLE):
        """
        Initialize the state manager.

        Args:
            initial_state: The starting state for the application.
        """
        self._current_state = initial_state
        self._previous_state: Optional[AppState] = None

    @property
    def current_state(self) -> AppState:
        """Get the current application state."""
        return self._current_state

    @property
    def previous_state(self) -> Optional[AppState]:
        """Get the previous application state."""
        return self._previous_state

    def transition_to(self, new_state: AppState) -> None:
        """
        Transition to a new state.

        Args:
            new_state: The state to transition to.
        """
        if new_state != self._current_state:
            self._previous_state = self._current_state
            self._current_state = new_state

    def is_idle(self) -> bool:
        """Check if the current state is IDLE."""
        return self._current_state == AppState.IDLE

    def is_screensaver(self) -> bool:
        """Check if the current state is SCREENSAVER."""
        return self._current_state == AppState.SCREENSAVER

    def is_playing(self) -> bool:
        """Check if the current state is PLAYING."""
        return self._current_state == AppState.PLAYING

    def can_play_video(self) -> bool:
        """
        Check if a video can be played in the current state.

        Videos can only be played from IDLE or SCREENSAVER states,
        not while already playing.
        """
        return self._current_state in (AppState.IDLE, AppState.SCREENSAVER)
