"""
custom01_flow.py

audio_file + source_txt

"""

import os
import time
import logging
from abc import ABC

from .workflow_base import WorkflowBase
from ..transcriber.local_whisper_transcriber import transcribe_audio as chosen_transcriber
from ..elt_utils.helper import transcribe_and_save
from ..evaluation.text_evaluation import evaluate_transcription_naive, evaluate_transcription_word_level


class Custom01Flow(WorkflowBase, ABC):
    def __init__(self, audio_file_path: str, source_txt_file: str):
        super().__init__()

        self.audio_file_path = audio_file_path
        self.source_txt_file = source_txt_file
        self.transcription_file = None

    def generate_transcription_pair(self) -> 'Custom01Flow':
        time_stamp = time.strftime("%Y%m%d_%H%M%S")
        output_base = "D:\it_project\github_sync\Miscellaneous\english_learning_tools\processed_data"
        transcription_file = os.path.join(output_base, f"result_{time_stamp}.txt")

        transcribe_and_save(self.audio_file_path, transcription_file, chosen_transcriber)

        self.transcription_file = transcription_file

        return self

    def evaluate1(self) -> 'Custom01Flow':
        logging.debug("Starting evaluation...")

        accuracy_rate, redundancy_rate = evaluate_transcription_naive(self.source_txt_file, self.transcription_file)

        logging.info(f'Accuracy Rate: {accuracy_rate * 100:.2f}%')
        logging.info(f'Redundancy Rate: {redundancy_rate:.2f}%')

        return self

    def evaluate2(self) -> 'Custom01Flow':
        logging.debug("Starting evaluation Word-level Levenshtein")
        distance = evaluate_transcription_word_level(self.source_txt_file, self.transcription_file)
        logging.info(f'distance: {distance}')

        return self

    def execute(self) -> 'Custom01Flow':
        return self

    def run(self) -> 'Custom01Flow':
        return self.generate_transcription_pair().evaluate1().evaluate2()


def _simple_example():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    audio_file_path = r"D:\it_project\github_sync\Miscellaneous\english_learning_tools\validation_data\testing_sample.wav"
    source_txt_file = r"D:\it_project\github_sync\Miscellaneous\english_learning_tools\validation_data\testing_sample.txt"
    workflow = Custom01Flow(audio_file_path, source_txt_file)

    workflow.run()


if __name__ == "__main__":
    _simple_example()
