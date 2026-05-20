"""Path utilities for YouTube Music Converter"""

import os
from pathlib import Path


def get_config_dir():
    """
    Get application configuration directory.
    
    Returns:
        Path: Configuration directory path
    """
    config_dir = Path.home() / ".youtube-music-converter"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_downloads_dir():
    """
    Get default downloads directory.
    
    Returns:
        Path: Downloads directory path
    """
    # Try to use system Downloads folder
    downloads = Path.home() / "Downloads"
    if downloads.exists():
        return downloads
    
    # Fallback to current directory
    return Path.cwd()


def get_temp_dir():
    """
    Get application temporary directory.
    
    Returns:
        Path: Temporary directory path
    """
    temp_dir = get_config_dir() / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    return temp_dir


def ensure_directory(path):
    """
    Ensure directory exists, create if necessary.
    
    Args:
        path (str or Path): Directory path
        
    Returns:
        Path: Directory path
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_available_filename(directory, filename):
    """
    Get available filename, appending counter if file exists.
    
    Args:
        directory (str or Path): Directory path
        filename (str): Original filename
        
    Returns:
        Path: Available file path
    """
    directory = Path(directory)
    filepath = directory / filename
    
    if not filepath.exists():
        return filepath
    
    # Split filename and extension
    name_parts = filename.rsplit('.', 1)
    if len(name_parts) == 2:
        name, ext = name_parts
        ext = '.' + ext
    else:
        name = filename
        ext = ''
    
    # Add counter until we find available name
    counter = 1
    while True:
        new_filename = f"{name}_{counter}{ext}"
        new_filepath = directory / new_filename
        if not new_filepath.exists():
            return new_filepath
        counter += 1


def get_file_size(path):
    """
    Get file size in human-readable format.
    
    Args:
        path (str or Path): File path
        
    Returns:
        str: Human-readable file size
    """
    path = Path(path)
    if not path.exists():
        return "0 B"
    
    size = path.stat().st_size
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    
    return f"{size:.2f} TB"


def cleanup_temp_files(keep_files=None):
    """
    Clean up temporary files.
    
    Args:
        keep_files (list): List of files to keep
    """
    temp_dir = get_temp_dir()
    keep_files = keep_files or []
    
    for file in temp_dir.glob('*'):
        if file.name not in keep_files:
            try:
                if file.is_dir():
                    import shutil
                    shutil.rmtree(file)
                else:
                    file.unlink()
            except Exception as e:
                print(f"Failed to delete {file}: {e}")
