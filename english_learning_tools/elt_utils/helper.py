# elt_utils/helper.py

import re


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


if __name__ == "__main__":
    vtt_file = r"D:\it_project\github_sync\Miscellaneous\english_learning_tools\crawler\downloads\Saving water in the driest place on Earth ⏲️ 6 Minute English.en-GB.vtt"
    output_txt_file = r"D:\it_project\github_sync\Miscellaneous\english_learning_tools\crawler\downloads\ddd.txt"
    vtt_to_txt(vtt_file, output_txt_file)
    print(f"Converted VTT to TXT: {output_txt_file}")
