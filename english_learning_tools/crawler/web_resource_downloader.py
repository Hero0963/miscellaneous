import yt_dlp
import os


def list_subtitles(url: str):
    """列出影片的所有可用字幕語言"""
    with yt_dlp.YoutubeDL({'listsubtitles': True}) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        return info_dict.get('subtitles', {})


def download_youtube_transcript(url: str, output_dir: str = None) -> str:
    """
    Download subtitles from a YouTube video using yt-dlp.

    Parameters:
    - url (str): The YouTube video URL.
    - output_dir (str): The directory where the subtitle file will be saved (default is english_learning_tools/downloads).

    Returns:
    - str: The path to the saved subtitle file.
    """
    # 確保 output_dir 指定為 english_learning_tools 根目錄下的 downloads 資料夾
    if output_dir is None:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_dir = os.path.join(project_root, 'downloads')

    # 確保目標資料夾存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 設定 yt-dlp 選項來下載字幕
    ydl_opts = {
        'writesubtitles': True,
        'subtitlesformat': 'vtt',
        'subtitleslangs': ['all'],
        'skip_download': True,
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'noplaylist': True  # 只下載單一影片，避免下載整個播放清單
    }

    # 下載字幕
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        # 字幕檔案名會是影片標題 + .vtt（或 .srt）
        subtitle_file = ydl.prepare_filename(info_dict).rsplit(".", 1)[0] + ".vtt"

    return subtitle_file


def download_youtube_audio_as_wav(url: str, output_dir: str = None) -> str:
    """
    Download audio from a YouTube video and convert it to WAV format using yt-dlp and FFmpeg.

    Parameters:
    - url (str): The YouTube video URL.
    - output_dir (str): The directory where the WAV file will be saved (default is current directory).

    Returns:
    - str: The path to the saved WAV file.
    """

    if output_dir is None:
        # 獲取當前檔案 (web_resource_downloader.py) 所在的資料夾
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # 設定 output_dir 為 english_learning_tools 底下的 downloads 資料夾
        output_dir = os.path.join(project_root, 'downloads')

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Setup yt-dlp options for extracting audio and converting to WAV
    ydl_opts = {
        'format': 'bestaudio/best',  # Download the best available audio
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),  # Output file template
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # Extract audio using FFmpeg
            'preferredcodec': 'wav',  # Convert audio to WAV format
            'preferredquality': '192',  # Audio quality (bitrate)
        }],
        # 'ffmpeg_location': 'C:/ffmpeg/bin',  # Update this if FFmpeg is not in PATH
        'noplaylist': True,  # Download only the video, not the entire playlist
    }

    # Download and convert the audio
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        file_name = ydl.prepare_filename(info_dict).rsplit(".", 1)[0] + ".wav"  # Generate the expected WAV filename

    return file_name


# Example usage
if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    output_path = download_youtube_transcript(video_url, output_dir="downloads")
    print(f"WAV file saved at: {output_path}")
