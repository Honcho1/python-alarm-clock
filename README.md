# Python Alarm Clock

A feature-rich, terminal-based alarm clock application built with Python. This program offers customizable alarm tones, flexible snooze options, and comprehensive alarm management capabilities.

## Features

- **Multiple Alarm Support**: Set and manage multiple alarms simultaneously
- **Custom Alarm Tones**: Choose from built-in tones or upload your own audio files
- **Flexible Snooze Options**: Customizable snooze duration (5, 10, 15 minutes, or custom)
- **Smart Validation**: Input validation for time format and file paths
- **Background Monitoring**: Non-blocking alarm monitoring using threading
- **Alarm Management**: Enable/disable alarms without deletion
- **User-Friendly Interface**: Clean text-based menu system with status indicators
- **Error Handling**: Robust error handling with graceful fallbacks
- **Help Documentation**: Built-in help system for user guidance

## Installation

1. Clone this repository: git clone https://github.com/Honcho1/python-alarm-clock.git
```cd python-alarm-clock```
2. Install required dependencies:
```pip install playsound```
Note: If `playsound` is not available, the program will run with simulated audio output.

## Usage

1. Run the program:
```python alarm_clock.py```
2. Follow the menu options to:
   - Set new alarms with custom times and tones
   - View all configured alarms
   - Manage existing alarms (enable/disable/delete)
   - Access help documentation

## Supported Audio Formats

- WAV (.wav)
- MP3 (.mp3)
- OGG (.ogg)
- M4A (.m4a)

## Key Components

### AlarmClock Class
The main class that handles all alarm functionality including:
- Alarm creation and validation
- Tone selection and playback
- Snooze management
- Background monitoring
- User interface

### Time Validation
Ensures proper 24-hour format (HH:MM) input with comprehensive error checking.

### Threading System
Uses Python threading for non-blocking alarm monitoring while maintaining responsive user interface.

## Configuration Options

- **Alarm Time**: 24-hour format (HH:MM)
- **Alarm Tones**: Default options or custom audio files
- **Snooze Duration**: 5, 10, 15 minutes, or custom (1-60 minutes)
- **Alarm Labels**: Custom descriptions for easy identification

## Error Handling

The program includes comprehensive error handling for:
- Invalid time formats
- Missing audio files
- Corrupted audio playback
- File path validation
- Keyboard interrupts
- Threading exceptions

## Requirements

- Python 3.6+
- playsound library (optional - program works without it)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is open source and available under the MIT License.

## Future Enhancements

- GUI interface using tkinter or PyQt
- Recurring alarm options (daily, weekly)
- Volume control for alarm tones
- Integration with system notifications
- Web-based interface
- Mobile app companion

## Author

Daniel Nwadinkpa

## Acknowledgments

- Built with Python's threading and datetime libraries
- Audio playback powered by playsound library
- Inspired by the need for a customizable, terminal-based alarm system