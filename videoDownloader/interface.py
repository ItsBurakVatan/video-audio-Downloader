# interface.py
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QWidget, QRadioButton, QProgressBar, QMessageBox, QButtonGroup, QFileDialog
)
from PyQt5.QtCore import Qt
from yt_dlp import YoutubeDL


class DownloaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video ve Ses İndirici")
        self.setGeometry(300, 200, 500, 300)

        # Ana widget ve düzen
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # URL Girişi
        self.url_label = QLabel("İndirme Bağlantısını Girin:")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("URL'yi buraya yapıştırın...")
        self.layout.addWidget(self.url_label)
        self.layout.addWidget(self.url_input)

        # İndirme Yolu Seçimi
        self.path_button = QPushButton("İndirme Klasörünü Seç")
        self.path_button.clicked.connect(self.select_download_path)
        self.layout.addWidget(self.path_button)

        self.download_path = os.path.join(os.path.expanduser("~"), "Downloads")
        os.makedirs(self.download_path, exist_ok=True)

        # İndirme Türü Seçimi
        self.type_label = QLabel("İndirme Türünü Seçin:")
        self.mp3_button = QRadioButton("MP3 (Ses)")
        self.mp4_button = QRadioButton("MP4 (Video)")
        self.mp4_button.setChecked(True)  # Varsayılan olarak MP4 seçili
        self.type_group = QButtonGroup()
        self.type_group.addButton(self.mp3_button)
        self.type_group.addButton(self.mp4_button)
        self.layout.addWidget(self.type_label)
        self.layout.addWidget(self.mp3_button)
        self.layout.addWidget(self.mp4_button)

        # İndirme Butonu
        self.download_button = QPushButton("İndir")
        self.download_button.clicked.connect(self.start_download)
        self.layout.addWidget(self.download_button)

        # İlerleme Çubuğu
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.layout.addWidget(self.progress_bar)

    def select_download_path(self):
        selected_path = QFileDialog.getExistingDirectory(self, "İndirme Klasörünü Seç")
        if selected_path:
            self.download_path = selected_path

    def start_download(self):
        url = self.url_input.text()
        if not url.strip():
            self.show_message("Hata", "Lütfen bir URL girin!", QMessageBox.Warning)
            return

        download_type = "mp3" if self.mp3_button.isChecked() else "mp4"
        self.download_video_or_audio(url, download_type)

    def download_video_or_audio(self, url, download_type):
        # Proje ana dizini (main.py'nin bulunduğu yer)
        project_dir = os.path.dirname(os.path.abspath(__file__))

        # ffmpeg/bin klasörünü ulaşmak için yol oluşturma
        ffmpeg_location = os.path.join(project_dir, 'ffmpeg-2025-01-15-git-4f3c9f2f03-essentials_build', 'bin')

        # options sözlüğü
        options = {
            'outtmpl': f'{self.download_path}/%(title)s.%(ext)s',
            'ffmpeg_location': ffmpeg_location,
            'progress_hooks': [self.update_progress],
        }

        if download_type == "mp3":
            options.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        elif download_type == "mp4":
            options.update({
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
            })

        try:
            with YoutubeDL(options) as ydl:
                ydl.download([url])
            self.show_message("Başarılı", "İndirme tamamlandı!", QMessageBox.Information)
        except Exception as e:
            self.show_message("Hata", f"İndirme sırasında bir hata oluştu:\n{str(e)}", QMessageBox.Critical)

    def update_progress(self, d):
        if d['status'] == 'downloading':
            percentage = d.get('_percent_str', '0.0%').strip('%')
            try:
                self.progress_bar.setValue(int(float(percentage)))
            except ValueError:
                self.progress_bar.setValue(0)  # Eğer dönüştürme başarısız olursa, ilerleme çubuğunu sıfırlayabilirsiniz.
        elif d['status'] == 'finished':
            self.progress_bar.setValue(100)

    def show_message(self, title, message, icon):
        msg_box = QMessageBox()
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()


def main():
    app = QApplication([])
    window = DownloaderApp()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
