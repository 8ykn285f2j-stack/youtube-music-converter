"""CLI entry point for YouTube Music Converter"""

import argparse
from pathlib import Path
from src.converter import YouTubeDownloader, AudioConverter, MetadataHandler
from src.analyzer import QualityAnalyzer
from src.utils import is_valid_youtube_url, app_logger, get_downloads_dir


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='YouTube Music Converter - Convert YouTube videos to MP3 or WAV'
    )
    
    parser.add_argument(
        '-u', '--url',
        help='YouTube video or playlist URL'
    )
    parser.add_argument(
        '-f', '--format',
        choices=['mp3', 'wav'],
        default='mp3',
        help='Output format (default: mp3)'
    )
    parser.add_argument(
        '-b', '--bitrate',
        default='320k',
        help='MP3 bitrate (default: 320k)'
    )
    parser.add_argument(
        '-o', '--output',
        default=str(get_downloads_dir()),
        help='Output directory'
    )
    parser.add_argument(
        '--analyze',
        help='Analyze audio file instead of converting'
    )
    parser.add_argument(
        '--keep-temp',
        action='store_true',
        help='Keep temporary files'
    )
    parser.add_argument(
        '--no-metadata',
        action='store_true',
        help='Skip metadata embedding'
    )
    
    args = parser.parse_args()
    
    # Analysis mode
    if args.analyze:
        analyze_file(args.analyze)
        return
    
    # Conversion mode
    if not args.url:
        parser.print_help()
        return
    
    convert_url(args)


def convert_url(args):
    """Convert a YouTube URL."""
    is_valid, url_type, video_id = is_valid_youtube_url(args.url)
    
    if not is_valid:
        print(f"❌ Invalid YouTube URL: {args.url}")
        return
    
    print(f"📥 Downloading: {args.url}")
    
    downloader = YouTubeDownloader()
    result = downloader.download_video(args.url, args.output)
    
    if not result['success']:
        print(f"❌ Download failed: {result['error']}")
        return
    
    audio_file = result['file_path']
    print(f"✅ Downloaded to: {audio_file}")
    
    # Convert
    print(f"🔄 Converting to {args.format.upper()}...")
    converter = AudioConverter()
    
    output_file = Path(audio_file).with_suffix(f'.{args.format}')
    
    if args.format == 'mp3':
        result = converter.convert_to_mp3(audio_file, str(output_file), args.bitrate)
    else:
        result = converter.convert_to_wav(audio_file, str(output_file))
    
    if not result['success']:
        print(f"❌ Conversion failed: {result['error']}")
        return
    
    print(f"✅ Converted to: {output_file}")
    
    # Embed metadata
    if not args.no_metadata and args.format == 'mp3':
        print("📝 Embedding metadata...")
        metadata_handler = MetadataHandler()
        metadata_handler.embed_metadata(
            str(output_file),
            {'title': Path(audio_file).stem}
        )
    
    print(f"🎵 Done! Saved to: {output_file}")


def analyze_file(file_path):
    """Analyze audio file quality."""
    if not Path(file_path).exists():
        print(f"❌ File not found: {file_path}")
        return
    
    print(f"🔍 Analyzing: {file_path}")
    
    analyzer = QualityAnalyzer()
    result = analyzer.analyze_file(file_path)
    
    if not result['success']:
        print(f"❌ Analysis failed: {result['error']}")
        return
    
    data = result['data']
    
    print("\n" + "="*60)
    print("📊 QUALITY ANALYSIS REPORT")
    print("="*60)
    print(f"File: {data['filename']}")
    print(f"Size: {data['file_size_mb']} MB")
    print(f"Duration: {data['duration_formatted']}")
    print(f"Codec: {data['codec']}")
    print(f"Sample Rate: {data['sample_rate']} Hz")
    print(f"Channels: {data['channels']}")
    print(f"\nClaimed Bitrate: {data['claimed_bitrate_kbps']} kbps")
    print(f"Calculated Bitrate: {data['calculated_bitrate_kbps']} kbps")
    print(f"Difference: {data['bitrate_difference']} kbps")
    print(f"\nQuality: {data['quality_assessment']}")
    
    if data['is_fake_320kbps']:
        print(f"⚠️  FAKE 320kbps DETECTED!")
    else:
        print(f"✅ No fake bitrate detected")
    
    if data['warnings']:
        print(f"\n⚠️  Warnings:")
        for warning in data['warnings']:
            print(f"   {warning}")
    
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
