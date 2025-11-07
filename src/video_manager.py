"""
Video manager module for handling video file operations.
Manages video discovery, selection, and provides video file paths.
"""

import random
from pathlib import Path
from typing import List, Optional

from config import VIDEOS_DIR, SUPPORTED_FORMATS


class VideoManager:
    """
    Manages video files for playback.

    Discovers videos in the configured directory and provides
    random selection for playback.
    """

    def __init__(self, videos_dir: Path = VIDEOS_DIR):
        """
        Initialize the video manager.

        Args:
            videos_dir: Directory containing video files.
        """
        self.videos_dir = videos_dir
        self._available_videos: List[Path] = []
        self._load_videos()

    def _load_videos(self) -> None:
        """
        Scan the videos directory and load all supported video files.
        """
        if not self.videos_dir.exists():
            print(f"Warning: Videos directory '{self.videos_dir}' does not exist")
            return

        self._available_videos = [
            video_file
            for video_file in self.videos_dir.iterdir()
            if video_file.is_file()
            and video_file.suffix.lower() in SUPPORTED_FORMATS
        ]

        if not self._available_videos:
            print(
                f"Warning: No video files found in '{self.videos_dir}' "
                f"with formats {SUPPORTED_FORMATS}"
            )
        else:
            print(f"Loaded {len(self._available_videos)} video(s)")

    def get_random_video(self) -> Optional[Path]:
        """
        Get a random video file from the available videos.

        Returns:
            Path to a random video file, or None if no videos available.
        """
        if not self._available_videos:
            return None
        return random.choice(self._available_videos)

    def has_videos(self) -> bool:
        """
        Check if any videos are available.

        Returns:
            True if videos are available, False otherwise.
        """
        return len(self._available_videos) > 0

    def reload(self) -> None:
        """
        Reload the video list from the directory.
        Useful if videos are added or removed while the application is running.
        """
        self._load_videos()

    @property
    def video_count(self) -> int:
        """Get the number of available videos."""
        return len(self._available_videos)
