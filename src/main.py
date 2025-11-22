"""
Main application entry point for the interactive video playback system.
Orchestrates the event loop, state management, and component interactions.
"""

import sys
import time
from pathlib import Path

import pygame

from config import FPS, SCREENSAVER_TIMEOUT
from state import AppState, StateManager
from video_manager import VideoManager
from image_manager import ImageManager
from input_handler import InputHandler
from display import Display


class VideoPlaybackApp:
    """
    Main application class that orchestrates all components.
    """

    def __init__(self):
        """Initialize the application and all its components."""
        self.running = False
        self.clock = pygame.time.Clock()

        # Initialize components
        self.state_manager = StateManager(AppState.IDLE)
        self.video_manager = VideoManager()
        self.image_manager = ImageManager()
        self.input_handler = InputHandler()
        self.display = Display()

        # Timing
        self.last_activity_time = time.time()

        # Set up input callback
        self.input_handler.set_trigger_callback(self._on_input_trigger)

    def _on_input_trigger(self) -> None:
        """
        Callback function called when input is triggered.
        Handles video playback initiation.
        """
        if self.state_manager.can_play_video():
            self._start_video_playback()

    def _start_video_playback(self) -> None:
        """Start playing a random video."""
        video_path = self.video_manager.get_random_video()

        if video_path is None:
            print("No videos available to play")
            return

        print(f"Starting playback: {video_path.name}")

        # Transition to PLAYING state
        self.state_manager.transition_to(AppState.PLAYING)

        # Start video playback
        if self.display.play_video(video_path):
            self.last_activity_time = time.time()

    def _check_screensaver(self) -> None:
        """
        Check if screensaver should be activated.
        Activates after SCREENSAVER_TIMEOUT seconds of inactivity.
        """
        if self.state_manager.is_idle():
            time_since_activity = time.time() - self.last_activity_time
            if time_since_activity >= SCREENSAVER_TIMEOUT:
                self.state_manager.transition_to(AppState.SCREENSAVER)
                print("Screensaver activated")

                # Load a random image for the screensaver
                if self.image_manager.has_images():
                    image_path = self.image_manager.get_random_image()
                    if image_path:
                        self.display.load_screensaver_image(image_path)

    def _update_video_playback(self) -> None:
        """Update video playback and handle completion."""
        if not self.state_manager.is_playing():
            return

        # Check if video is still playing
        video_playing = self.display.update_video()

        if not video_playing:
            # Video finished
            print("Video playback completed")
            self.display.stop_video()
            self.state_manager.transition_to(AppState.IDLE)
            self.last_activity_time = time.time()

            # Load a new random image for the idle state
            if self.image_manager.has_images():
                image_path = self.image_manager.get_random_image()
                if image_path:
                    self.display.load_screensaver_image(image_path)

    def _render(self) -> None:
        """Render the current state to the display."""
        if self.state_manager.is_screensaver():
            self.display.render_screensaver()
        elif self.state_manager.is_idle():
            # Show a random image when idle (if available)
            self.display.render_screensaver()
        # Video rendering is handled in _update_video_playback

    def run(self) -> None:
        """Main application loop."""
        if not self.video_manager.has_videos():
            print("Warning: No videos found. Add videos to the 'videos/' directory.")
            print("The application will continue running but cannot play videos.")

        if not self.image_manager.has_images():
            print("Warning: No images found. Add images to the 'images/' directory.")
            print("The application will show text when idle instead of images.")
        else:
            # Load initial image for idle state
            image_path = self.image_manager.get_random_image()
            if image_path:
                self.display.load_screensaver_image(image_path)

        self.running = True
        print("Application started. Press SPACE to trigger video playback.")
        print("Press ESC or Q to quit.")

        while self.running:
            # Process events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_q):
                        self.running = False

            # Process input
            self.input_handler.process_events(events)

            # Update state
            if self.state_manager.is_playing():
                self._update_video_playback()
            else:
                self._check_screensaver()

            # Render
            self._render()

            # Maintain frame rate
            self.clock.tick(FPS)

        # Cleanup
        self._cleanup()

    def _cleanup(self) -> None:
        """Clean up resources before exit."""
        print("Shutting down...")
        self.display.close()


def main():
    """Entry point for the application."""
    try:
        app = VideoPlaybackApp()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
    finally:
        sys.exit(0)


if __name__ == "__main__":
    main()
