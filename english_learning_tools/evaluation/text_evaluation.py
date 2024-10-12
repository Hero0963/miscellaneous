# text_evaluation.py

import re
import collections
import logging


def replace_punctuation_with_spaces(text: str) -> str:
    return re.sub(r'[^\w\s]', ' ', text)


def prepare_text_for_comparison(file_path: str) -> list[str]:
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read().lower()
    cleaned_text = replace_punctuation_with_spaces(text)
    return cleaned_text.split()


def evaluate_transcription_naive(source_file: str, transcribed_file: str) -> tuple[float, float]:
    cleaned_src_text = prepare_text_for_comparison(source_file)
    cleaned_trc_text = prepare_text_for_comparison(transcribed_file)

    source_word_count = collections.Counter(cleaned_src_text)
    transcribed_word_count = collections.Counter(cleaned_trc_text)

    logging.debug(f"source_word_count={source_word_count}")
    logging.debug("")
    logging.debug(f"transcribed_word_count={transcribed_word_count}")

    matched_words = 0
    total_unique_words = 0
    for word in source_word_count:
        total_unique_words += 1
        if word in transcribed_word_count:
            matched_words += 1

    accuracy_rate = matched_words / total_unique_words if total_unique_words else 1.0
    logging.debug(
        f"matched_words={matched_words}, total_unique_words={total_unique_words}, accuracy_rate={accuracy_rate}")

    source_total_word = sum(source_word_count.values())
    transcribed_total_word = sum(transcribed_word_count.values())
    redundancy_rate = ((
                               transcribed_total_word - matched_words) / source_total_word) * 100.0 if transcribed_total_word else 0.0
    logging.debug(
        f"source_total_word={source_total_word}, transcribed_total_word={transcribed_total_word}, redundancy_rate={redundancy_rate}")

    return accuracy_rate, redundancy_rate


def _simple_example():
    logging_level = 'debug'.upper()
    logging.basicConfig(level=getattr(logging, logging_level))
    source_file = r"D:\it_project\github_sync\Miscellaneous\english_learning_tools\crawler\downloads\sss.txt"
    transcribed_file = r"D:\it_project\github_sync\Miscellaneous\english_learning_tools\crawler\downloads\ttt.txt"

    accuracy_rate, redundancy_rate = evaluate_transcription_naive(source_file, transcribed_file)
    logging.debug(f'Accuracy Rate: {accuracy_rate * 100:.2f}%')
    logging.debug(f'Redundancy Rate: {redundancy_rate:.2f}%')


if __name__ == '__main__':
    _simple_example()
