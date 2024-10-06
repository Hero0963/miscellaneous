import os
import re


def has_chinese2(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False


def has_chinese(strs):
    zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
    match = zh_pattern.search(strs)
    if match:
        return True
    return False


def main():
    input_file = "15minEng_in.txt"
    output_file = "15minEng_out.txt"

    if os.path.exists(output_file):
        os.remove(output_file)

    try:
        with open(output_file, 'w', encoding="utf-8") as file_write_obj:
            with open(input_file, encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines:
                    if not has_chinese(line):
                        file_write_obj.write(line)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
