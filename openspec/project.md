# Project Context

## Purpose

Interactive video playback system that responds to Makey Makey touch inputs. The system displays videos from a directory on demand, triggered by physical touch interactions, creating an engaging interactive installation experience.

## Tech Stack

- **Python 3.x** in virtual environment `my-venv`
- **pygame** - Video playback, fullscreen display, and input handling
- **python-vlc** or **opencv-python** - Alternative/supplementary video handling (TBD during implementation)
- **keyboard** or **evdev** - Makey Makey input detection
- **pathlib** - File and directory management
- Standard library: `os`, `random`, `queue`, `threading`

## Project Conventions

### Code Style

- Follow PEP 8 conventions
- Use descriptive variable names: `current_video`, `video_queue`, `is_playing`
- Functions should be small and single-purpose
- Add docstrings to all public functions and classes
- Use type hints where appropriate
- Maximum line length: 88 characters (Black formatter standard)

### Architecture Patterns

- **Event-driven architecture**: Input events trigger video playback
- **State machine**: Track application states (idle/screensaver, playing, transitioning)
- **Separation of concerns**:
  - Input handling module (keyboard/Makey Makey)
  - Video playback module
  - Display/UI module
  - State management
- **Configuration over hardcoding**: Video directory path, screensaver settings as config

### Testing Strategy

**Phase 1: Spacebar Testing**

- Implement and test all video playback functionality using spacebar as trigger
- Verify video loading from `/videos/` directory
- Test state transitions and screensaver behavior
- Ensure smooth playback and transitions

**Phase 2: Makey Makey Integration**

- Replace spacebar input with Makey Makey touch detection
- Test all touch inputs map correctly to video triggers
- Verify debouncing and input reliability

**Testing Priorities**:

1. Video playback starts and completes without interruption
2. Only one video plays at a time
3. Transitions are smooth and seamless
4. Screensaver activates/deactivates correctly
5. Input detection is reliable and responsive

### Git Workflow

- Feature branches for new functionality
- Descriptive commit messages following conventional commits
- Test before committing changes
- Branch naming: `feature/description`, `fix/description`

## Domain Context

This is an interactive art installation or exhibit system where physical touch interactions (via Makey Makey) trigger video playback. The experience should feel responsive, polished, and seamless to create an engaging user experience.

**Key Concepts**:

- **Makey Makey**: A hardware device that converts physical touches/connections into keyboard inputs
- **Screensaver mode**: Attractive idle state when no interaction is occurring
- **Video triggers**: Each touch should play a complete video from start to finish
- **Queue discipline**: Inputs during playback should be handled gracefully (ignore or queue)

## Important Constraints

### Video Playback

- Only one video plays at a time
- Videos must play from start to finish without interruption
- Smooth, seamless transitions between screensaver and video playback
- No visible lag or stuttering during transitions

### Input Handling

- Must support Makey Makey input detection
- Debouncing may be required to prevent multiple triggers from single touch
- System must be responsive but not overly sensitive

### File Management

- All videos stored in `/videos/` directory in project root
- Support common video formats (mp4, avi, mov)
- System should handle videos of varying lengths and resolutions

### Display

- Fullscreen playback recommended for installation context
- Maintain aspect ratio of videos
- Black background or custom screensaver when idle

## External Dependencies

- **Makey Makey hardware**: USB HID device that simulates keyboard inputs
- **Video files**: Located in `/videos/` directory
- **Display hardware**: Monitor or projector for fullscreen playback
- **Python virtual environment**: `my-venv` must be activated for all operations
