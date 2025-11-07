# Interactive Video Playback System

An interactive video playback system that responds to touch inputs (Makey Makey) for creating engaging installation experiences. Videos play on demand triggered by physical interactions.

## Features

- **Event-Driven Video Playback**: Touch triggers play videos from start to finish
- **Automatic Screensaver**: Displays attractive idle screen after inactivity
- **Fullscreen Display**: Immersive playback with aspect ratio preservation
- **State Management**: Clean state machine handling transitions
- **Modular Architecture**: Separation of concerns for easy maintenance

## Requirements

- Python 3.x
- Virtual environment (included as `my-venv`)
- Video files in supported formats (mp4, avi, mov)
- Display hardware (monitor or projector)
- Optional: Makey Makey device (Phase 2)

## Installation

1. **Activate the virtual environment**:
   ```bash
   source my-venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Add video files**:
   - Place your video files in the `videos/` directory
   - Supported formats: `.mp4`, `.avi`, `.mov`

## Usage

### Running the Application

```bash
cd src
python main.py
```

### Controls (Phase 1 - Testing)

- **SPACE**: Trigger video playback
- **ESC or Q**: Quit application

### Application States

1. **IDLE**: Initial state, waiting for input
2. **SCREENSAVER**: Displays "Touch to play..." after 10 seconds of inactivity
3. **PLAYING**: Currently playing a video

## Configuration

Edit `src/config.py` to customize settings:

- `VIDEOS_DIR`: Directory containing videos
- `FULLSCREEN`: Enable/disable fullscreen mode
- `SCREEN_WIDTH` / `SCREEN_HEIGHT`: Display resolution
- `SCREENSAVER_TIMEOUT`: Seconds before screensaver activates
- `INPUT_TRIGGER_KEY`: Key for triggering playback (Phase 1)
- `DEBOUNCE_TIME`: Minimum time between triggers

## Project Structure

```
mar/
├── src/
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration settings
│   ├── state.py             # State machine
│   ├── video_manager.py     # Video file management
│   ├── input_handler.py     # Input detection
│   └── display.py           # Display and rendering
├── videos/                   # Video files directory
├── my-venv/                  # Python virtual environment
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Development Phases

### Phase 1: Spacebar Testing (Current)
- ✅ Video playback triggered by spacebar
- ✅ State management and transitions
- ✅ Screensaver functionality
- ✅ OpenCV-based video rendering

### Phase 2: Makey Makey Integration (Future)
- Replace spacebar with Makey Makey touch detection
- Map multiple touch inputs to different triggers
- Implement debouncing for physical inputs
- Test reliability in installation environment

## Architecture

The application follows an event-driven architecture with clear separation of concerns:

- **State Machine**: Manages application states (IDLE, SCREENSAVER, PLAYING)
- **Event Loop**: Pygame-based loop handling inputs and rendering
- **Video Management**: Discovers and randomly selects videos
- **Input Handler**: Detects and debounces input triggers
- **Display**: Renders videos and screensaver using OpenCV + Pygame

## Testing

### Testing Checklist

- [ ] Videos load correctly from `videos/` directory
- [ ] Spacebar triggers video playback
- [ ] Video plays from start to finish without interruption
- [ ] Only one video plays at a time
- [ ] Screensaver activates after timeout
- [ ] Screensaver deactivates on input
- [ ] Transitions are smooth and seamless
- [ ] Application handles no videos gracefully
- [ ] Multiple video formats work correctly

### Adding Test Videos

For testing, add sample videos to the `videos/` directory:
```bash
# Example: Download a test video
cd videos/
wget https://example.com/test-video.mp4
```

## Troubleshooting

### No Videos Found
- Ensure video files are in the `videos/` directory
- Check that videos have supported extensions (.mp4, .avi, .mov)
- Verify file permissions allow reading

### Display Issues
- Try disabling fullscreen in `config.py` (set `FULLSCREEN = False`)
- Adjust `SCREEN_WIDTH` and `SCREEN_HEIGHT` to match your display
- Check that your system supports the required resolution

### Performance Issues
- Reduce video resolution for smoother playback
- Lower the FPS setting in `config.py`
- Ensure your system has sufficient resources

### Input Not Responding
- Verify the pygame window has focus
- Check `DEBOUNCE_TIME` isn't too high
- Ensure the correct trigger key is configured

## Code Style

This project follows PEP 8 conventions:
- Descriptive variable names
- Type hints on function signatures
- Docstrings on all public functions
- Maximum line length: 88 characters

## Future Enhancements

- [ ] Audio support during video playback
- [ ] Multiple Makey Makey input mapping
- [ ] Video queue management
- [ ] Custom screensaver animations
- [ ] Video playlist configuration
- [ ] Web-based configuration interface
- [ ] Statistics and analytics

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]
