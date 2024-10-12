"""
yt_flow.py

This module defines the YouTubeWorkflow class, which handles downloading content from YouTube
and executing related transcription evaluations. The workflow supports both audio and subtitle (VTT) downloads.
"""

import logging
from abc import ABC

from .workflow_base import WorkflowBase
from .workflow_param import YTFlowParams
from ..crawler.web_resource_downloader import (
    download_youtube_transcript as get_transcript,
    download_youtube_audio_as_wav as get_audio
)
from ..evaluation.text_evaluation import evaluate_transcription_naive
from ..elt_utils.helper import vtt_to_txt


class YTFlow(WorkflowBase, ABC):
    def __init__(self, params: YTFlowParams):
        super().__init__()
        self.params = params
        self.source_files = []

    def download_source(self):
        logging.debug(f"Fetching content from YouTube: {self.params.fetch_content}")
        for content in self.params.fetch_content:
            source_file = None
            if content == "audio":
                source_file = get_audio(self.params.yt_url, self.params.output_folder)
            elif content == "vtt":
                source_file = get_transcript(self.params.yt_url, self.params.output_folder)

            if source_file:
                self.source_files.append(source_file)

        logging.debug(f"Downloaded source files: {self.source_files}")

    def transcribe_audio(self):
        if self.params.use_content == "audio":
            logging.info(f"Transcribing audio from: {self.params.audio_path}")
            transcribed_file = self.transcribe_audio(self.params.audio_path)  # 假設有轉錄邏輯
            return transcribed_file
        elif self.params.use_content == "vtt":
            logging.info("Using VTT file as source text")
            vtt_file = self.source_files[self.params.fetch_content.index("vtt")]
            transcribed_file = vtt_file.replace('.vtt', '.txt')
            vtt_to_txt(vtt_file, transcribed_file)
            return transcribed_file
        return None

    def evaluate(self, transcribed_file: str):
        logging.debug("Starting evaluation...")
        accuracy_rate, redundancy_rate = evaluate_transcription_naive(self.source_files[0], transcribed_file)
        logging.debug(f'Accuracy Rate: {accuracy_rate * 100:.2f}%')
        logging.debug(f'Redundancy Rate: {redundancy_rate:.2f}%')

    def run(self):
        self.download_source()
        transcribed_file = self.transcribe_audio()
        self.evaluate(transcribed_file)


def _simple_example():
    pass


if __name__ == "__main__":
    _simple_example()
