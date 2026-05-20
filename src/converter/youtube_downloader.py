"""YouTube downloader using yt-dlp for YouTube Music Converter"""

import os
import subprocess
from pathlib import Path
from src.utils import app_logger, get_temp_dir, sanitize_filename


class YouTubeDownloader:
    """Downloads audio from YouTube using yt-dlp."""
    
    def __init__(self):
        """Initialize YouTube downloader."""
        self.logger = app_logger
        self.temp_dir = get_temp_dir()
    
    def check_yt_dlp(self):
        """
        Check if yt-dlp is installed and accessible.
        
        Returns:
            bool: True if yt-dlp is available
        """
        try:
            subprocess.run(['yt-dlp', '--version'], 
                         capture_output=True, 
                         check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.logger.error("yt-dlp not found. Please install it: pip install yt-dlp")
            return False
    
    def download_video(self, url, output_path=None, progress_callback=None):
        """
        Download audio from YouTube video.
        
        Args:
            url (str): YouTube video URL
            output_path (str): Output directory path
            progress_callback (callable): Callback function for progress updates
            
        Returns:
            dict: Download info with 'success', 'file_path', 'info', and 'error' keys
        """
        if not self.check_yt_dlp():
            return {
                'success': False,
                'file_path': None,
                'info': None,
                'error': 'yt-dlp is not installed'
            }
        
        output_path = output_path or self.temp_dir
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)
        
        try:
            self.logger.info(f"Downloading audio from: {url}")
            
            # yt-dlp command with best audio format
            output_template = output_path / '%(title)s.%(ext)s'
            
            command = [
                'yt-dlp',
                '-f', 'bestaudio/best',  # Best available audio
                '-x',  # Extract audio
                '--audio-format', 'wav',  # Download as WAV to minimize quality loss
                '--audio-quality', '0',  # Best quality (FLAC equivalent)
                '--progress',
                '--newline',
                '-o', str(output_template),
                url
            ]
            
            # Run yt-dlp
            result = subprocess.run(command, 
                                  capture_output=True,
                                  text=True,
                                  timeout=3600)  # 1 hour timeout
            
            if result.returncode != 0:
                error_msg = result.stderr or "Unknown error during download"
                self.logger.error(f"Download failed: {error_msg}")
                return {
                    'success': False,
                    'file_path': None,
                    'info': None,
                    'error': error_msg
                }
            
            # Find downloaded file
            audio_files = list(output_path.glob('*.wav'))
            if audio_files:
                audio_file = audio_files[0]
                self.logger.info(f"Successfully downloaded: {audio_file}")
                
                return {
                    'success': True,
                    'file_path': str(audio_file),
                    'info': {
                        'url': url,
                        'filename': audio_file.name,
                        'size': audio_file.stat().st_size,
                    },
                    'error': None
                }
            else:
                return {
                    'success': False,
                    'file_path': None,
                    'info': None,
                    'error': 'No audio file was downloaded'
                }
        
        except subprocess.TimeoutExpired:
            self.logger.error("Download timeout")
            return {
                'success': False,
                'file_path': None,
                'info': None,
                'error': 'Download timeout (exceeded 1 hour)'
            }
        except Exception as e:
            self.logger.error(f"Download error: {str(e)}")
            return {
                'success': False,
                'file_path': None,
                'info': None,
                'error': str(e)
            }
    
    def get_video_info(self, url):
        """
        Get information about YouTube video without downloading.
        
        Args:
            url (str): YouTube video URL
            
        Returns:
            dict: Video information (title, duration, uploader, etc.)
        """
        if not self.check_yt_dlp():
            return None
        
        try:
            command = [
                'yt-dlp',
                '--dump-json',
                '--no-warnings',
                url
            ]
            
            result = subprocess.run(command,
                                  capture_output=True,
                                  text=True,
                                  timeout=30)
            
            if result.returncode == 0:
                import json
                info = json.loads(result.stdout)
                return {
                    'title': info.get('title'),
                    'duration': info.get('duration'),
                    'uploader': info.get('uploader'),
                    'thumbnail': info.get('thumbnail'),
                    'upload_date': info.get('upload_date'),
                }
        except Exception as e:
            self.logger.error(f"Error getting video info: {str(e)}")
        
        return None
    
    def get_playlist_info(self, url):
        """
        Get information about YouTube playlist.
        
        Args:
            url (str): YouTube playlist URL
            
        Returns:
            list: List of video information dictionaries
        """
        if not self.check_yt_dlp():
            return []
        
        try:
            command = [
                'yt-dlp',
                '--dump-json',
                '--flat-playlist',
                '--no-warnings',
                url
            ]
            
            result = subprocess.run(command,
                                  capture_output=True,
                                  text=True,
                                  timeout=60)
            
            if result.returncode == 0:
                import json
                videos = []
                for line in result.stdout.strip().split('\n'):
                    if line:
                        info = json.loads(line)
                        if info.get('_type') == 'url':
                            videos.append({
                                'id': info.get('id'),
                                'title': info.get('title'),
                                'url': info.get('url'),
                            })
                return videos
        except Exception as e:
            self.logger.error(f"Error getting playlist info: {str(e)}")
        
        return []
