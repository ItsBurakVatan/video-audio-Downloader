import os
from yt_dlp import YoutubeDL

def download_video_or_audio(url, download_type):
    """
    Video veya ses indirme fonksiyonu.
    :param url: İndirme bağlantısı
    :param download_type: "mp3" veya "mp4"
    """
    # Kullanıcı profilindeki "Downloads" klasörünü bul
    default_output_path = os.path.join(os.path.expanduser("~"), "Downloads")
    os.makedirs(default_output_path, exist_ok=True)  # Çıktı klasörünü oluştur

    # Proje ana dizini (main.py'nin bulunduğu yer)
    project_dir = os.path.dirname(os.path.abspath(__file__))

    # ffmpeg/bin klasörüne ulaşmak için yol oluşturma
    ffmpeg_location = os.path.join(project_dir, 'ffmpeg-2025-01-15-git-4f3c9f2f03-essentials_build', 'bin')

    options = {
        'outtmpl': f'{default_output_path}/%(title)s.%(ext)s',
        'ffmpeg_location': ffmpeg_location
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
            'merge_output_format': 'mp4',  # Sadece MP4 için geçerli
            'keepvideo': True,  # Orijinal dosyaları sakla (isteğe bağlı)
        })
    with YoutubeDL(options) as ydl:
        ydl.download([url])

def main():
    url = input("Video bağlantısını girin: ")
    print("İndirme türünü seçin:")
    print("1. MP3 (ses)")
    print("2. MP4 (video)")
    choice = input("Seçiminiz (1 veya 2): ")

    if choice == "1":
        download_video_or_audio(url, "mp3")
        print("Ses dosyası başarıyla indirildi!")
    elif choice == "2":
        download_video_or_audio(url, "mp4")
        print("Video dosyası başarıyla indirildi!")
    else:
        print("Geçersiz seçim. Programdan çıkılıyor.")

if __name__ == "__main__":
    main()