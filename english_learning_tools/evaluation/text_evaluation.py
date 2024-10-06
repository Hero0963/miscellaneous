import collections


def evaluate_transcription_naive(source_file: str, transcribed_file: str) -> tuple[float, float]:
    with open(source_file, 'r', encoding='utf-8') as f:
        source_text = f.read().lower().split()

    with open(transcribed_file, 'r', encoding='utf-8') as f:
        transcribed_text = f.read().lower().split()

    source_word_count = collections.Counter(source_text)
    transcribed_word_count = collections.Counter(transcribed_text)

    matched_words = 0
    total_unique_words = 0
    for word in source_word_count:
        total_unique_words += 1
        if word in transcribed_word_count:
            matched_words += 1

    accuracy = matched_words / total_unique_words if total_unique_words else 1.0

    source_total_word = sum(source_word_count.values())
    transcribed_total_word = sum(transcribed_word_count.values())
    redundancy_rate = (source_total_word / transcribed_total_word) * 100.0 if transcribed_total_word else 0.0

    return accuracy, redundancy_rate
