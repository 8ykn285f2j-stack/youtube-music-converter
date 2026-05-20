"""Main window for YouTube Music Converter GUI"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QLabel, QComboBox, QPushButton, QMessageBox, QSpinBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from src.ui.widgets import URLDropZone, DirectorySelector, ConversionProgressWidget, FormGroup, SeparatorLine
from src.ui.styles import get_stylesheet
from src.converter import YouTubeDownloader, AudioConverter, MetadataHandler
from src.analyzer import QualityAnalyzer
from src.utils import is_valid_youtube_url, is_valid_bitrate, get_downloads_dir
from src.config import settings
from pathlib import Path


class ConversionWorker(QThread):
    """Worker thread for audio conversion."""
    
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(dict)
    
    def __init__(self, url, output_format, bitrate, output_dir, embed_metadata):
        super().__init__()
        self.url = url
        self.output_format = output_format
        self.bitrate = bitrate
        self.output_dir = output_dir
        self.embed_metadata = embed_metadata
    
    def run(self):
        """Run conversion process."""
        try:
            self.status.emit("Downloading audio from YouTube...")
            downloader = YouTubeDownloader()
            download_result = downloader.download_video(self.url, self.output_dir)
            
            if not download_result['success']:
                self.finished.emit({
                    'success': False,
                    'error': download_result.get('error')
                })
                return
            
            self.progress.emit(40)
            audio_file = download_result['file_path']
            
            # Convert audio
            self.status.emit(f"Converting to {self.output_format.upper()}...")
            converter = AudioConverter()
            
            output_file = Path(audio_file).with_suffix(f'.{self.output_format}')
            
            if self.output_format == 'mp3':
                result = converter.convert_to_mp3(audio_file, str(output_file), self.bitrate)
            else:
                result = converter.convert_to_wav(audio_file, str(output_file))
            
            if not result['success']:
                self.finished.emit({
                    'success': False,
                    'error': result.get('error')
                })
                return
            
            self.progress.emit(80)
            
            # Embed metadata if enabled
            if self.embed_metadata and self.output_format == 'mp3':
                self.status.emit("Embedding metadata...")
                metadata_handler = MetadataHandler()
                metadata_handler.embed_metadata(
                    output_file,
                    {
                        'title': Path(audio_file).stem,
                    }
                )
            
            self.progress.emit(100)
            self.status.emit("Conversion complete!")
            
            self.finished.emit({
                'success': True,
                'file_path': str(output_file),
                'error': None
            })
        
        except Exception as e:
            self.finished.emit({
                'success': False,
                'error': str(e)
            })


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Music Converter")
        self.setGeometry(100, 100, 900, 700)
        self.conversion_worker = None
        self.init_ui()
        self.setStyleSheet(get_stylesheet())
    
    def init_ui(self):
        """Initialize UI."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # Tab widget
        tabs = QTabWidget()
        
        # Converter tab
        converter_tab = self.create_converter_tab()
        tabs.addTab(converter_tab, "Converter")
        
        # Analyzer tab
        analyzer_tab = self.create_analyzer_tab()
        tabs.addTab(analyzer_tab, "Analyzer")
        
        # Settings tab
        settings_tab = self.create_settings_tab()
        tabs.addTab(settings_tab, "Settings")
        
        layout.addWidget(tabs)
        central_widget.setLayout(layout)
    
    def create_converter_tab(self):
        """Create converter tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # URL input
        self.url_input = URLDropZone()
        layout.addWidget(self.url_input)
        
        layout.addWidget(SeparatorLine())
        
        # Format selection
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Output Format:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(["MP3 (320kbps)", "WAV (Lossless)"])
        format_layout.addWidget(self.format_combo)
        layout.addLayout(format_layout)
        
        # Bitrate selection (for MP3)
        bitrate_layout = QHBoxLayout()
        bitrate_layout.addWidget(QLabel("Bitrate (MP3):"))
        self.bitrate_combo = QComboBox()
        self.bitrate_combo.addItems(["320k", "256k", "192k", "128k"])
        self.bitrate_combo.setCurrentText("320k")
        bitrate_layout.addWidget(self.bitrate_combo)
        layout.addLayout(bitrate_layout)
        
        # Output directory
        layout.addWidget(QLabel("Output Directory:"))
        self.output_dir_selector = DirectorySelector(str(get_downloads_dir()))
        layout.addWidget(self.output_dir_selector)
        
        layout.addWidget(SeparatorLine())
        
        # Progress
        self.progress_widget = ConversionProgressWidget()
        layout.addWidget(self.progress_widget)
        
        layout.addWidget(SeparatorLine())
        
        # Convert button
        self.convert_button = QPushButton("Convert")
        self.convert_button.setMinimumHeight(50)
        self.convert_button.clicked.connect(self.start_conversion)
        layout.addWidget(self.convert_button)
        
        widget.setLayout(layout)
        return widget
    
    def create_analyzer_tab(self):
        """Create analyzer tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Drag audio files here to analyze:"))
        
        self.analyzer_widget = QWidget()
        analyzer_layout = QVBoxLayout()
        analyzer_layout.addWidget(QLabel("Analyzer - Coming soon"))
        self.analyzer_widget.setLayout(analyzer_layout)
        
        layout.addWidget(self.analyzer_widget)
        
        widget.setLayout(layout)
        return widget
    
    def create_settings_tab(self):
        """Create settings tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Settings"))
        
        # Embed metadata option
        metadata_layout = QHBoxLayout()
        metadata_layout.addWidget(QLabel("Embed Metadata:"))
        self.embed_metadata_checkbox = QComboBox()
        self.embed_metadata_checkbox.addItems(["Yes", "No"])
        metadata_layout.addWidget(self.embed_metadata_checkbox)
        layout.addLayout(metadata_layout)
        
        # Embed artwork option
        artwork_layout = QHBoxLayout()
        artwork_layout.addWidget(QLabel("Embed Album Artwork:"))
        self.embed_artwork_checkbox = QComboBox()
        self.embed_artwork_checkbox.addItems(["Yes", "No"])
        artwork_layout.addWidget(self.embed_artwork_checkbox)
        layout.addLayout(artwork_layout)
        
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def start_conversion(self):
        """Start conversion process."""
        url = self.url_input.get_url()
        
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a YouTube URL")
            return
        
        is_valid, url_type, video_id = is_valid_youtube_url(url)
        if not is_valid:
            QMessageBox.warning(self, "Error", "Invalid YouTube URL")
            return
        
        output_format = "mp3" if "MP3" in self.format_combo.currentText() else "wav"
        bitrate = self.bitrate_combo.currentText()
        output_dir = self.output_dir_selector.get_directory()
        embed_metadata = self.embed_metadata_checkbox.currentText() == "Yes"
        
        self.progress_widget.clear_details()
        self.progress_widget.set_progress(0)
        self.progress_widget.set_status("Starting conversion...")
        self.convert_button.setEnabled(False)
        
        self.conversion_worker = ConversionWorker(
            url, output_format, bitrate, output_dir, embed_metadata
        )
        self.conversion_worker.progress.connect(self.progress_widget.set_progress)
        self.conversion_worker.status.connect(self.progress_widget.set_status)
        self.conversion_worker.finished.connect(self.on_conversion_finished)
        self.conversion_worker.start()
    
    def on_conversion_finished(self, result):
        """Handle conversion completion."""
        self.convert_button.setEnabled(True)
        
        if result['success']:
            QMessageBox.information(
                self,
                "Success",
                f"Conversion complete!\nFile saved to: {result['file_path']}"
            )
        else:
            QMessageBox.critical(
                self,
                "Error",
                f"Conversion failed: {result['error']}"
            )
