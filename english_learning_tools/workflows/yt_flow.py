"""
yt_flow.py

This module defines the YouTubeWorkflow class, which handles downloading content from YouTube
and executing related transcription evaluations. The workflow supports both audio and subtitle (VTT) downloads.
"""

import os
import time
import logging
from abc import ABC

from .workflow_base import WorkflowBase
from .workflow_param import YTFlowParams
from ..crawler.web_resource_downloader import (
    download_youtube_transcript as get_transcript,
    download_youtube_audio_as_wav as get_audio
)

from ..transcriber.local_whisper_transcriber import transcribe_audio as chosen_transcriber
from ..elt_utils.helper import transcribe_and_save
from ..elt_utils.helper import vtt_to_txt

from ..evaluation.text_evaluation import evaluate_transcription_naive


class YTFlow(WorkflowBase, ABC):
    def __init__(self, params: YTFlowParams):
        super().__init__()
        self.params = params
        self.source_files = []
        self.evaluation_pairs = []

        if not hasattr(self.params, 'yt_url') or not hasattr(self.params, 'output_folder') or not hasattr(self.params,
                                                                                                          'fetch_content'):
            raise ValueError("Missing necessary parameters in YTFlowParams")

    def download_source(self) -> 'YTFlow':
        logging.debug(f"Fetching content from YouTube")
        download_map = {
            "audio": get_audio,
            "vtt": get_transcript
        }
        for content in self.params.fetch_content:
            download_func = download_map.get(content)
            if download_func:
                source_file = download_func(self.params.yt_url, self.params.output_folder)
                if source_file:
                    self.source_files.append(source_file)

        logging.debug(f"Downloaded source files: {self.source_files}")

        return self

    def generate_transcription_pair(self) -> 'YTFlow':
        time_stamp = time.strftime("%Y%m%d_%H%M%S")
        output_base = self.params.output_folder

        if self.params.use_content == "audio":
            audio_file = next((f for f in self.source_files if f.endswith('.wav')), None)

            if not audio_file:
                logging.warning("No audio file (.wav) found in source_files.")
                return self

            logging.debug(f"Transcribing audio from: {audio_file}")
            transcription_file = os.path.join(output_base, f"source_audio_{time_stamp}.txt")
            transcribe_and_save(audio_file, transcription_file, chosen_transcriber)
            self.evaluation_pairs.append(transcription_file)

        if self.params.use_content == "vtt":
            vtt_file = next((f for f in self.source_files if f.endswith('.vtt')), None)

            if not vtt_file:
                logging.warning("No VTT file (.vtt) found in source_files.")
                return self

            logging.debug(f"Processing VTT file: {vtt_file}")
            transcription_file = os.path.join(output_base, f"source_vtt_txt_file_{time_stamp}.txt")
            vtt_to_txt(vtt_file, transcription_file)
            self.evaluation_pairs.append(transcription_file)
            logging.info(f"VTT transcription saved to: {transcription_file}")

        audio_file = self.params.recorded_audio_path
        if not os.path.exists(audio_file):
            logging.warning(f"Recorded audio file not found: {audio_file}")
            return self

        logging.debug(f"Transcribing recorded audio from: {audio_file}")
        transcription_file = os.path.join(output_base, f"record_audio_{time_stamp}.txt")
        transcribe_and_save(audio_file, transcription_file, chosen_transcriber)
        self.evaluation_pairs.append(transcription_file)

        return self

    def evaluate(self) -> 'YTFlow':
        logging.debug("Starting evaluation...")

        source_file = next((f for f in self.evaluation_pairs if 'source' in f and f.endswith('.txt')), None)
        if not source_file:
            logging.warning("No source file found for evaluation.")
            return self

        transcribed_file = next((f for f in self.evaluation_pairs if 'record' in f and f.endswith('.txt')), None)
        if not transcribed_file:
            logging.warning("No transcribed file found for evaluation.")
            return self

        accuracy_rate, redundancy_rate = evaluate_transcription_naive(source_file, transcribed_file)

        logging.info(f'Accuracy Rate: {accuracy_rate * 100:.2f}%')
        logging.info(f'Redundancy Rate: {redundancy_rate:.2f}%')

        return self

    def execute(self) -> 'YTFlow':
        return self

    def run(self) -> 'YTFlow':
        return self.download_source().generate_transcription_pair().evaluate()


def _simple_example():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    output_folder = os.path.join(os.getcwd(), "english_learning_tools", "downloads")

    os.makedirs(output_folder, exist_ok=True)

    params = YTFlowParams(
        yt_url=r"https://www.youtube.com/watch?v=Y3vHuw97AiA",
        recorded_audio_path=r"D:\onedrive\Documents\錄音\2024_10_13_the_future_of_food.wav",
        output_folder=output_folder,
        fetch_content=["audio", "vtt"],
        use_content="audio",
    )

    workflow = YTFlow(params)

    workflow.run()


if __name__ == "__main__":
    _simple_example()
