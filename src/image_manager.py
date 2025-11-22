"""
Image manager module for handling image file operations.
Manages image discovery, selection, and provides image file paths.
"""

import random
from pathlib import Path
from typing import List, Optional

from config import IMAGES_DIR, SUPPORTED_IMAGE_FORMATS


class ImageManager:
    """
    Manages image files for display.

    Discovers images in the configured directory and provides
    random selection for screensaver display.
    """

    def __init__(self, images_dir: Path = IMAGES_DIR):
        """
        Initialize the image manager.

        Args:
            images_dir: Directory containing image files.
        """
        self.images_dir = images_dir
        self._available_images: List[Path] = []
        self._load_images()

    def _load_images(self) -> None:
        """
        Scan the images directory and load all supported image files.
        """
        if not self.images_dir.exists():
            print(f"Warning: Images directory '{self.images_dir}' does not exist")
            return

        self._available_images = [
            image_file
            for image_file in self.images_dir.iterdir()
            if image_file.is_file()
            and image_file.suffix.lower() in SUPPORTED_IMAGE_FORMATS
        ]

        if not self._available_images:
            print(
                f"Warning: No image files found in '{self.images_dir}' "
                f"with formats {SUPPORTED_IMAGE_FORMATS}"
            )
        else:
            print(f"Loaded {len(self._available_images)} image(s)")

    def get_random_image(self) -> Optional[Path]:
        """
        Get a random image file from the available images.

        Returns:
            Path to a random image file, or None if no images available.
        """
        if not self._available_images:
            return None
        return random.choice(self._available_images)

    def has_images(self) -> bool:
        """
        Check if any images are available.

        Returns:
            True if images are available, False otherwise.
        """
        return len(self._available_images) > 0

    def reload(self) -> None:
        """
        Reload the image list from the directory.
        Useful if images are added or removed while the application is running.
        """
        self._load_images()

    @property
    def image_count(self) -> int:
        """Get the number of available images."""
        return len(self._available_images)
