"""Audio converter using FFmpeg for YouTube Music Converter"""

import subprocess
from pathlib import Path
from src.utils import app_logger


class AudioConverter:
    """Converts audio files to MP3 and WAV formats using FFmpeg."""
    
    def __init__(self):
        """Initialize audio converter."""
        self.logger = app_logger
    
    def check_ffmpeg(self):
        """
        Check if FFmpeg is installed and accessible.
        
        Returns:
            bool: True if FFmpeg is available
        """
        try:
            subprocess.run(['ffmpeg', '-version'], 
                         capture_output=True, 
                         check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.logger.error("FFmpeg not found. Please install it")
            return False
    
    def convert_to_mp3(self, input_file, output_file, bitrate='320k'):
        """
        Convert audio to MP3 at specified bitrate.
        
        Args:
            input_file (str): Input audio file path
            output_file (str): Output MP3 file path
            bitrate (str): MP3 bitrate (default: 320k)
            
        Returns:
            dict: Conversion result with 'success', 'file_path', and 'error' keys
        """
        if not self.check_ffmpeg():
            return {
                'success': False,
                'file_path': None,
                'error': 'FFmpeg is not installed'
            }
        
        input_file = Path(input_file)
        output_file = Path(output_file)
        
        if not input_file.exists():
            error_msg = f"Input file not found: {input_file}"
            self.logger.error(error_msg)
            return {
                'success': False,
                'file_path': None,
                'error': error_msg
            }
        
        try:
            self.logger.info(f"Converting to MP3 ({bitrate}): {input_file} -> {output_file}")
            
            # FFmpeg command for MP3 conversion
            # -acodec libmp3lame: Use MP3 codec
            # -ab: Audio bitrate
            # -q:a: Audio quality (0-9, 0 is best)
            command = [
                'ffmpeg',
                '-i', str(input_file),
                '-acodec', 'libmp3lame',
                '-ab', bitrate,
                '-q:a', '0',  # Best quality for given bitrate
                '-y',  # Overwrite output file
                str(output_file)
            ]
            
            result = subprocess.run(command,
                                  capture_output=True,
                                  text=True,
                                  timeout=3600)
            
            if result.returncode != 0:
                error_msg = result.stderr or "Unknown error during conversion"
                self.logger.error(f"MP3 conversion failed: {error_msg}")
                return {
                    'success': False,
                    'file_path': None,
                    'error': error_msg
                }
            
            if output_file.exists():
                self.logger.info(f"Successfully converted to MP3: {output_file}")
                return {
                    'success': True,
                    'file_path': str(output_file),
                    'error': None
                }
            else:
                return {
                    'success': False,
                    'file_path': None,
                    'error': 'Output file was not created'
                }
        
        except subprocess.TimeoutExpired:
            self.logger.error("Conversion timeout")
            return {
                'success': False,
                'file_path': None,
                'error': 'Conversion timeout'
            }
        except Exception as e:
            self.logger.error(f"Conversion error: {str(e)}")
            return {
                'success': False,
                'file_path': None,
                'error': str(e)
            }
    
    def convert_to_wav(self, input_file, output_file):
        """
        Convert audio to lossless WAV format.
        
        Args:
            input_file (str): Input audio file path
            output_file (str): Output WAV file path
            
        Returns:
            dict: Conversion result with 'success', 'file_path', and 'error' keys
        """
        if not self.check_ffmpeg():
            return {
                'success': False,
                'file_path': None,
                'error': 'FFmpeg is not installed'
            }
        
        input_file = Path(input_file)
        output_file = Path(output_file)
        
        if not input_file.exists():
            error_msg = f"Input file not found: {input_file}"
            self.logger.error(error_msg)
            return {
                'success': False,
                'file_path': None,
                'error': error_msg
            }
        
        try:
            self.logger.info(f"Converting to WAV: {input_file} -> {output_file}")
            
            # FFmpeg command for WAV conversion (lossless)
            command = [
                'ffmpeg',
                '-i', str(input_file),
                '-acodec', 'pcm_s16le',  # 16-bit PCM
                '-ar', '44100',  # 44.1kHz sample rate
                '-y',  # Overwrite output file
                str(output_file)
            ]
            
            result = subprocess.run(command,
                                  capture_output=True,
                                  text=True,
                                  timeout=3600)
            
            if result.returncode != 0:
                error_msg = result.stderr or "Unknown error during conversion"
                self.logger.error(f"WAV conversion failed: {error_msg}")
                return {
                    'success': False,
                    'file_path': None,
                    'error': error_msg
                }
            
            if output_file.exists():
                self.logger.info(f"Successfully converted to WAV: {output_file}")
                return {
                    'success': True,
                    'file_path': str(output_file),
                    'error': None
                }
            else:
                return {
                    'success': False,
                    'file_path': None,
                    'error': 'Output file was not created'
                }
        
        except subprocess.TimeoutExpired:
            self.logger.error("Conversion timeout")
            return {
                'success': False,
                'file_path': None,
                'error': 'Conversion timeout'
            }
        except Exception as e:
            self.logger.error(f"Conversion error: {str(e)}")
            return {
                'success': False,
                'file_path': None,
                'error': str(e)
            }
    
    def get_audio_info(self, audio_file):
        """
        Get audio file information using FFprobe.
        
        Args:
            audio_file (str): Audio file path
            
        Returns:
            dict: Audio information (duration, bitrate, codec, etc.)
        """
        audio_file = Path(audio_file)
        if not audio_file.exists():
            return None
        
        try:
            command = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                str(audio_file)
            ]
            
            result = subprocess.run(command,
                                  capture_output=True,
                                  text=True,
                                  timeout=10)
            
            if result.returncode == 0:
                import json
                data = json.loads(result.stdout)
                
                # Extract relevant audio information
                format_info = data.get('format', {})
                stream_info = data.get('streams', [{}])[0]
                
                return {
                    'duration': float(format_info.get('duration', 0)),
                    'bitrate': int(format_info.get('bit_rate', 0)),
                    'codec': stream_info.get('codec_name'),
                    'sample_rate': stream_info.get('sample_rate'),
                    'channels': stream_info.get('channels'),
                    'codec_bitrate': stream_info.get('bit_rate'),
                }
        except Exception as e:
            self.logger.error(f"Error getting audio info: {str(e)}")
        
        return None
