# YouTube Music Converter

A professional-grade desktop application for converting YouTube Music videos and playlists to high-quality audio formats (MP3 @ 320kbps, WAV) while preserving metadata and album artwork.

## Features

✨ **Core Features**
- 🎵 Convert YouTube videos and playlists to MP3 (320kbps) or WAV (lossless)
- 🎨 Automatic metadata and album artwork embedding
- 📋 Batch playlist support with progress tracking
- 🖱️ Drag-and-drop URL input
- 📊 Quality analysis tool (detect fake 320kbps files)
- 💾 Persistent user settings

🔧 **Technical Features**
- Cross-platform (Windows, macOS, Linux)
- Modern PyQt6 GUI with dark theme
- Non-blocking background processing
- Comprehensive error handling and logging
- CLI interface for automation

## Requirements

### System Requirements
- Python 3.10+
- FFmpeg (required for audio conversion)

### Installation

#### 1. Install FFmpeg

**Windows (using Chocolatey):**
```bash
choco install ffmpeg
```

**macOS (using Homebrew):**
```bash
brew install ffmpeg
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt-get install ffmpeg
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install ffmpeg
```

#### 2. Clone Repository
```bash
git clone https://github.com/8ykn285f2j-stack/youtube-music-converter.git
cd youtube-music-converter
```

#### 3. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 4. Install Python Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### GUI Application

Run the graphical interface:
```bash
python -m src.main
```

**Features:**
1. **Converter Tab**
   - Paste or drag YouTube URL
   - Select output format (MP3 320kbps or WAV)
   - Choose output directory
   - Click "Convert" to start

2. **Playlist Tab**
   - Paste playlist URL
   - View tracks before conversion
   - Convert entire playlist in batch

3. **Analyzer Tab**
   - Drag audio files to analyze
   - Check bitrate and quality
   - Detect fake 320kbps files
   - View detailed audio metrics

### Command Line Interface

```bash
# Single video to MP3
python -m src.cli --url "https://www.youtube.com/watch?v=..." --format mp3 --bitrate 320k

# Single video to WAV
python -m src.cli --url "https://www.youtube.com/watch?v=..." --format wav

# Playlist conversion
python -m src.cli --url "https://www.youtube.com/playlist?list=..." --format mp3 --output ./music

# Analyze audio file
python -m src.cli --analyze "./path/to/audio.mp3"
```

**CLI Options:**
```
--url, -u          YouTube video/playlist URL
--format, -f       Output format: mp3, wav (default: mp3)
--bitrate, -b      Bitrate for MP3 (default: 320k)
--output, -o       Output directory (default: ./downloads)
--analyze          Analyze audio file instead of converting
--keep-temp        Keep temporary files after conversion
--no-metadata      Skip metadata/artwork embedding
```

## Project Structure

```
youtube-music-converter/
├── src/
│   ├── converter/
│   │   ├── youtube_downloader.py     # yt-dlp wrapper
│   │   ├── audio_converter.py        # FFmpeg wrapper
│   │   └── metadata_handler.py       # ID3 tag & artwork
│   ├── ui/
│   │   ├── main_window.py            # Main GUI window
│   │   ├── widgets.py                # Custom UI widgets
│   │   └── styles.py                 # Theme & styling
│   ├── analyzer/
│   │   └── quality_analyzer.py       # Audio quality analysis
│   ├── utils/
│   │   ├── validators.py             # URL validation
│   │   ├── path_utils.py             # Path utilities
│   │   └── logger.py                 # Logging setup
│   ├── config/
│   │   └── settings.py               # Configuration management
│   ├── main.py                       # GUI entry point
│   └── cli.py                        # CLI entry point
├── tests/
│   ├── test_converter.py
│   ├── test_analyzer.py
│   └── test_validators.py
├── requirements.txt
├── setup.py
└── README.md
```

## Configuration

Settings are stored in `~/.youtube-music-converter/config.json`:

```json
{
  "output_directory": "./downloads",
  "default_format": "mp3",
  "default_bitrate": "320k",
  "embed_artwork": true,
  "embed_metadata": true,
  "quality_threshold": 320,
  "theme": "dark"
}
```

## Quality Assurance

### Preserving Audio Quality

1. **Downloads Best Format** - yt-dlp selects the highest quality audio available
2. **Minimal Re-encoding** - WAV uses lossless conversion, MP3 uses high bitrate (320kbps)
3. **Metadata Preservation** - ID3v2 tags maintain artist, album, date information
4. **Artwork Embedding** - Thumbnail artwork automatically embedded in files

### Quality Analysis

The analyzer tool checks for:
- **Actual Bitrate** - Detects files that claim 320kbps but aren't
- **Audio Duration** - Validates conversion completed fully
- **Format Verification** - Confirms proper MP3/WAV encoding
- **Metadata Presence** - Checks for complete ID3 tags

## Troubleshooting

### FFmpeg Not Found
```bash
# Verify FFmpeg is installed
ffmpeg -version

# On Windows, add FFmpeg to PATH or install via Chocolatey
choco install ffmpeg
```

### Age-Restricted Videos
Some YouTube videos require authentication. yt-dlp will handle this automatically if you're logged in.

### Memory Issues with Large Playlists
Process playlists in smaller batches (100+ videos may require more system memory).

### No Audio Downloaded
- Check if video is available in your region
- Some videos may be audio-only streams (no video component)
- Try downloading with `--keep-temp` to inspect intermediate files

## Development

### Running Tests
```bash
pytest tests/
```

### Building Standalone Executable

**Windows:**
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon.ico src/main.py
```

**macOS:**
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon.icns src/main.py
```

## Legal Notice

⚠️ **Important:** This tool is designed for:
- Personal use with content you have rights to
- Educational purposes
- Legal fair use scenarios

Ensure you have the right to download content from YouTube. Respect copyright laws and YouTube's Terms of Service in your jurisdiction.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - See LICENSE file for details

## Support

For issues, feature requests, or questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review troubleshooting section above

## Changelog

### v0.1.0 (Initial Release)
- GUI application with drag-and-drop support
- MP3 (320kbps) and WAV conversion
- Playlist support
- Metadata and artwork embedding
- Quality analysis tool
- CLI interface
