"""URL and input validators for YouTube Music Converter"""

import re
from urllib.parse import urlparse, parse_qs


def is_valid_youtube_url(url):
    """
    Validate if URL is a valid YouTube video or playlist URL.
    
    Args:
        url (str): URL to validate
        
    Returns:
        tuple: (is_valid, url_type, video_id/playlist_id or None)
    """
    if not url or not isinstance(url, str):
        return False, None, None
    
    url = url.strip()
    
    # YouTube video URL patterns
    video_patterns = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',
        r'(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]{11})',
        r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]{11})',
    ]
    
    # YouTube playlist URL pattern
    playlist_pattern = r'(?:https?://)?(?:www\.)?youtube\.com/playlist\?list=([a-zA-Z0-9_-]+)'
    
    # Check video URLs
    for pattern in video_patterns:
        match = re.search(pattern, url)
        if match:
            return True, "video", match.group(1)
    
    # Check playlist URL
    match = re.search(playlist_pattern, url)
    if match:
        return True, "playlist", match.group(1)
    
    return False, None, None


def extract_youtube_id(url):
    """
    Extract YouTube video or playlist ID from URL.
    
    Args:
        url (str): YouTube URL
        
    Returns:
        str: Video/playlist ID or None if invalid
    """
    is_valid, url_type, youtube_id = is_valid_youtube_url(url)
    return youtube_id if is_valid else None


def is_valid_bitrate(bitrate):
    """
    Validate bitrate string format (e.g., '320k', '128k').
    
    Args:
        bitrate (str): Bitrate string
        
    Returns:
        bool: True if valid format
    """
    if not isinstance(bitrate, str):
        return False
    
    match = re.match(r'^(\d+)k?$', bitrate.lower())
    if match:
        value = int(match.group(1))
        return 32 <= value <= 320  # Valid MP3 bitrate range
    
    return False


def parse_bitrate(bitrate):
    """
    Parse bitrate string to integer value in kbps.
    
    Args:
        bitrate (str): Bitrate string (e.g., '320k', '320')
        
    Returns:
        int: Bitrate in kbps or None if invalid
    """
    if not is_valid_bitrate(bitrate):
        return None
    
    match = re.match(r'^(\d+)k?$', bitrate.lower())
    return int(match.group(1)) if match else None


def is_valid_output_format(format_str):
    """
    Validate output format.
    
    Args:
        format_str (str): Format string (mp3, wav)
        
    Returns:
        bool: True if valid format
    """
    valid_formats = ['mp3', 'wav']
    return isinstance(format_str, str) and format_str.lower() in valid_formats


def sanitize_filename(filename):
    """
    Sanitize filename to remove invalid characters.
    
    Args:
        filename (str): Filename to sanitize
        
    Returns:
        str: Sanitized filename
    """
    # Remove invalid filename characters
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars, '', filename)
    
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip('. ')
    
    # Replace multiple spaces with single space
    sanitized = re.sub(r'\s+', ' ', sanitized)
    
    # Limit length
    max_length = 200
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length].rsplit(' ', 1)[0]
    
    return sanitized or 'download'
