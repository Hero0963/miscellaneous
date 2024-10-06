import whisper
import torch
import textwrap


def transcribe_audio(file_path: str, model_type: str = "base", device: str = None) -> str:
    """
    Transcribe the given audio file using the specified Whisper model.

    Parameters:
    - file_path (str): Path to the audio file to be transcribed.
    - model_type (str): Type of Whisper model to use (default is 'base'). Options include 'tiny', 'base', 'small', 'medium', 'large'.
    - device (str): Device to use for computation ('cpu' or 'cuda'). If not specified, automatically chooses based on availability.

    Returns:
    - str: The transcribed text.
    """
    # 確認使用的設備
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    # Load the Whisper model on the specified device
    model = whisper.load_model(model_type).to(device)

    # Transcribe the audio
    result = model.transcribe(file_path)

    # Return the transcription text
    return result['text']


def print_transcribed_text(text: str, width: int = 70):
    """
    Print the transcribed text with automatic line wrapping.

    Parameters:
    - text (str): The transcribed text to print.
    - width (int): The maximum line width before wrapping (default is 70 characters).
    """
    wrapped_text = textwrap.fill(text, width=width)
    print(wrapped_text)


if __name__ == "__main__":
    # Input audio file
    audio_file = input("Enter the path to the audio file: ")

    # Transcribe using Whisper with device choice (can specify 'cpu' or 'cuda')
    transcribed_text = transcribe_audio(audio_file, model_type="base", device="cuda")

    # Output the transcribed text with line wrapping
    print("\nTranscribed text:\n")
    print_transcribed_text(transcribed_text)
