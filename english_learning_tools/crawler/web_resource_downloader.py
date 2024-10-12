# web_resource_downloader.py
# implement yt part currently

import yt_dlp
import os


def list_subtitles(url: str):
    with yt_dlp.YoutubeDL({'listsubtitles': True}) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        return info_dict.get('subtitles', {})


def download_youtube_transcript(url: str, output_dir: str = None) -> str:
    if output_dir is None:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_dir = os.path.join(project_root, 'downloads')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ydl_opts = {
        'writesubtitles': True,
        'subtitlesformat': 'vtt',
        'subtitleslangs': ['all'],
        'skip_download': True,
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'noplaylist': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        subtitle_file = ydl.prepare_filename(info_dict).rsplit(".", 1)[0] + ".vtt"

    return subtitle_file


def download_youtube_audio_as_wav(url: str, output_dir: str = None) -> str:
    if output_dir is None:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_dir = os.path.join(project_root, 'downloads')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],

        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        file_name = ydl.prepare_filename(info_dict).rsplit(".", 1)[0] + ".wav"  # Generate the expected WAV filename

    return file_name


if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    output_path = download_youtube_transcript(video_url, output_dir="downloads")
    print(f"file saved at: {output_path}")
