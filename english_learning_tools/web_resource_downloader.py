import yt_dlp
import os


def download_youtube_audio_as_wav(url: str, output_dir: str = ".") -> str:
    """
    Download audio from a YouTube video and convert it to WAV format using yt-dlp and FFmpeg.

    Parameters:
    - url (str): The YouTube video URL.
    - output_dir (str): The directory where the WAV file will be saved (default is current directory).

    Returns:
    - str: The path to the saved WAV file.
    """
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
    output_path = download_youtube_audio_as_wav(video_url, output_dir="./downloads")
    print(f"WAV file saved at: {output_path}")
