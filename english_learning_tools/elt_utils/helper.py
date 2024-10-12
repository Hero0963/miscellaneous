import re


def vtt_to_txt(vtt_file: str, output_txt: str) -> None:
    with open(vtt_file, 'r', encoding='utf-8') as vtt, open(output_txt, 'w', encoding='utf-8') as txt:
        lines = vtt.readlines()
        subtitle_text = []

        for line in lines:
            # Ignore lines that are not part of the subtitle text
            if re.match(r'\d{2}:\d{2}:\d{2}', line) or line.strip() == '' or '-->' in line:
                continue
            subtitle_text.append(line.strip())

        txt.write("\n".join(subtitle_text))


if __name__ == "__main__":
    vtt_file = "path_to_vtt_file.vtt"
    output_txt_file = "output_file.txt"
    vtt_to_txt(vtt_file, output_txt_file)
    print(f"Converted VTT to TXT: {output_txt_file}")
