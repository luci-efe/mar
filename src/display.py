"""
Display module for rendering video playback and screensaver.
Handles pygame display initialization, video playback, and screensaver rendering.
"""

from pathlib import Path
from typing import Optional, Tuple

import cv2
import numpy as np
import pygame
from PIL import Image

from config import (
    FULLSCREEN,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    BACKGROUND_COLOR,
    SCREENSAVER_TEXT,
    SCREENSAVER_TEXT_COLOR,
    SCREENSAVER_FONT_SIZE,
)


class Display:
    """
    Manages the display, video playback, and screensaver rendering.
    """

    def __init__(
        self,
        fullscreen: bool = FULLSCREEN,
        width: int = SCREEN_WIDTH,
        height: int = SCREEN_HEIGHT,
    ):
        """
        Initialize the display.

        Args:
            fullscreen: Whether to use fullscreen mode.
            width: Screen width in pixels.
            height: Screen height in pixels.
        """
        pygame.init()

        # Initialize mixer if available (optional, for audio support)
        try:
            pygame.mixer.init()
        except (NotImplementedError, ImportError):
            print("Note: Audio mixer not available (videos will play without sound)")

        self.width = width
        self.height = height
        self.fullscreen = fullscreen

        # Set up display
        if fullscreen:
            self.screen = pygame.display.set_mode(
                (width, height), pygame.FULLSCREEN
            )
        else:
            self.screen = pygame.display.set_mode((width, height))

        pygame.display.set_caption("Interactive Video Player")

        # Video playback state using OpenCV
        self._video_capture: Optional[cv2.VideoCapture] = None
        self._is_playing = False
        self._video_finished = False

        # Font for screensaver (optional)
        try:
            self.font = pygame.font.Font(None, SCREENSAVER_FONT_SIZE)
        except (NotImplementedError, ImportError):
            print("Note: Font module not available (screensaver text will be disabled)")
            self.font = None

        # Current screensaver image
        self._current_image: Optional[pygame.Surface] = None
        self._current_image_path: Optional[Path] = None

    def clear(self, color: Tuple[int, int, int] = BACKGROUND_COLOR) -> None:
        """
        Clear the screen with the specified color.

        Args:
            color: RGB color tuple.
        """
        self.screen.fill(color)

    def load_screensaver_image(self, image_path: Optional[Path]) -> bool:
        """
        Load an image for the screensaver display.

        Args:
            image_path: Path to the image file, or None to clear the image.

        Returns:
            True if image loaded successfully, False otherwise.
        """
        if image_path is None:
            self._current_image = None
            self._current_image_path = None
            return False

        try:
            # Load the image using PIL for better format support
            pil_image = Image.open(image_path)

            # Convert to RGB mode if necessary (handles RGBA, P, L, etc.)
            if pil_image.mode != 'RGB':
                pil_image = pil_image.convert('RGB')

            # Get image dimensions
            img_width, img_height = pil_image.size

            # Calculate scaling to fit screen while maintaining aspect ratio
            scale_width = self.width / img_width
            scale_height = self.height / img_height
            scale = min(scale_width, scale_height)

            # Calculate new dimensions
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)

            # Resize the image using PIL for better quality
            pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Convert PIL image to pygame surface
            mode = pil_image.mode
            size = pil_image.size
            data = pil_image.tobytes()

            self._current_image = pygame.image.fromstring(data, size, mode)
            self._current_image_path = image_path

            print(f"Loaded screensaver image: {image_path.name}")
            return True

        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            self._current_image = None
            self._current_image_path = None
            return False

    def render_screensaver(self) -> None:
        """
        Render the screensaver display.
        Shows an image (if available) or text in the center of the screen.
        """
        self.clear()

        # Render image if available
        if self._current_image is not None:
            # Calculate position to center the image
            img_rect = self._current_image.get_rect(
                center=(self.width // 2, self.height // 2)
            )
            self.screen.blit(self._current_image, img_rect)
        else:
            # Fallback: Render text if font is available
            if self.font:
                text_surface = self.font.render(
                    SCREENSAVER_TEXT, True, SCREENSAVER_TEXT_COLOR
                )
                text_rect = text_surface.get_rect(
                    center=(self.width // 2, self.height // 2)
                )
                self.screen.blit(text_surface, text_rect)

        pygame.display.flip()

    def load_video(self, video_path: Path) -> bool:
        """
        Load a video file for playback using OpenCV.

        Args:
            video_path: Path to the video file.

        Returns:
            True if video loaded successfully, False otherwise.
        """
        try:
            print(f"Loading video: {video_path.name}")

            # Stop any currently playing video
            self.stop_video()

            # Open video with OpenCV
            self._video_capture = cv2.VideoCapture(str(video_path))

            if not self._video_capture.isOpened():
                print(f"Failed to open video: {video_path}")
                return False

            self._is_playing = True
            self._video_finished = False

            # Get video properties
            fps = self._video_capture.get(cv2.CAP_PROP_FPS)
            frame_count = int(
                self._video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
            )
            duration = frame_count / fps if fps > 0 else 0
            print(
                f"Video loaded: {video_path.name} "
                f"({frame_count} frames, {fps:.2f} fps, {duration:.2f}s)"
            )

            return True

        except Exception as e:
            print(f"Error loading video: {e}")
            return False

    def play_video(self, video_path: Path) -> bool:
        """
        Start playing a video file.

        Args:
            video_path: Path to the video file.

        Returns:
            True if video started successfully, False otherwise.
        """
        return self.load_video(video_path)

    def update_video(self) -> bool:
        """
        Update video playback for the current frame.
        Reads and displays the next frame from the video.

        Returns:
            True if video is still playing, False if finished.
        """
        if not self._is_playing or self._video_capture is None:
            return False

        # Read the next frame
        ret, frame = self._video_capture.read()

        if not ret or frame is None:
            # Video finished
            self._video_finished = True
            return False

        # Convert frame from BGR (OpenCV) to RGB (pygame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Get frame dimensions
        frame_height, frame_width = frame.shape[:2]

        # Calculate scaling to fit screen while maintaining aspect ratio
        scale_width = self.width / frame_width
        scale_height = self.height / frame_height
        scale = min(scale_width, scale_height)

        # Calculate new dimensions
        new_width = int(frame_width * scale)
        new_height = int(frame_height * scale)

        # Resize frame
        frame = cv2.resize(frame, (new_width, new_height))

        # Calculate position to center the video
        x = (self.width - new_width) // 2
        y = (self.height - new_height) // 2

        # Clear screen with black background
        self.clear()

        # Convert numpy array to pygame surface
        frame_surface = pygame.surfarray.make_surface(
            np.transpose(frame, (1, 0, 2))
        )

        # Blit to screen
        self.screen.blit(frame_surface, (x, y))
        pygame.display.flip()

        return True

    def stop_video(self) -> None:
        """Stop video playback and release resources."""
        self._is_playing = False
        self._video_finished = False
        if self._video_capture is not None:
            self._video_capture.release()
            self._video_capture = None

    def is_playing(self) -> bool:
        """Check if a video is currently playing."""
        return self._is_playing

    def close(self) -> None:
        """Clean up and close the display."""
        self.stop_video()
        pygame.quit()
