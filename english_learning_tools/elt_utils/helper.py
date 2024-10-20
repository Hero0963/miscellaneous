# elt_utils/helper.py

import os
import re
import logging
from typing import Callable
from ..transcriber.local_whisper_transcriber import transcribe_audio as chosen_transcriber


def transcribe_and_save(audio_file: str, transcription_file: str, transcriber_func: Callable[[str], str]) -> None:
    logging.debug(f"Transcribing audio from: {audio_file}")
    transcription = transcriber_func(audio_file)

    with open(transcription_file, 'w', encoding='utf-8') as f:
        f.write(transcription)

    logging.debug(f"Transcription saved to: {transcription_file}")


def vtt_to_txt(vtt_file: str, output_txt: str) -> None:
    with open(vtt_file, 'r', encoding='utf-8') as vtt, open(output_txt, 'w', encoding='utf-8') as txt:
        lines = vtt.readlines()
        subtitle_text = []
        start_processing = False

        for line in lines:
            if not start_processing:
                if re.match(r'\d{2}:\d{2}:\d{2}', line):
                    start_processing = True

            if start_processing and not re.match(r'\d{2}:\d{2}:\d{2}',
                                                 line) and '-->' not in line.strip() and line.strip() != '':
                subtitle_text.append(line.strip())

        txt.write("\n".join(subtitle_text))


def _simple_test_vtt_to_txt():
    vtt_file = r"D:\it_project\github_sync\Miscellaneous\english_learning_tools\crawler\downloads\Saving water in the driest place on Earth ⏲️ 6 Minute English.en-GB.vtt"
    output_txt_file = r"D:\it_project\github_sync\Miscellaneous\english_learning_tools\crawler\downloads\ddd.txt"
    vtt_to_txt(vtt_file, output_txt_file)
    print(f"Converted VTT to TXT: {output_txt_file}")


def _simple_test_transcribe_and_save():
    audio_file = recorded_audio_path = r"D:\onedrive\Documents\錄音\2024_10_13_the_future_of_food.wav"
    output_name = r"D:\it_project\github_sync\Miscellaneous\english_learning_tools\validation_data\34567.txt"
    transcriber_func = chosen_transcriber
    transcribe_and_save(audio_file, output_name, transcriber_func)


if __name__ == "__main__":
    _simple_test_transcribe_and_save()
