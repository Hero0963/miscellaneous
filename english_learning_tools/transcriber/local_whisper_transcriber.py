import whisper
import torch
import textwrap


def transcribe_audio(file_path: str, model_type: str = "base", device: str = None) -> str:
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    model = whisper.load_model(model_type).to(device)

    result = model.transcribe(file_path)

    return result['text']


def print_transcribed_text(text: str, width: int = 70):
    wrapped_text = textwrap.fill(text, width=width)
    print(wrapped_text)


if __name__ == "__main__":
    audio_file = input("Enter the path to the audio file: ")
    transcribed_text = transcribe_audio(audio_file, model_type="base", device="cuda")

    print("\nTranscribed text:\n")
    print_transcribed_text(transcribed_text)
