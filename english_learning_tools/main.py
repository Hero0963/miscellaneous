from crawler.web_resource_downloader import download_youtube_audio_as_wav


if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    output_path = download_youtube_audio_as_wav(video_url)
    print(f"WAV file saved at: {output_path}")


