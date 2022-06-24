def is_Chinese_char(chr) -> bool:
    if '\u4e00' <= chr <= '\u9fa5':
        return True

    return False


def check_nonduplicate(file):
    counter_dict = {}

    flag = True

    with open(file, encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            for chr in line:
                if not is_Chinese_char(chr):
                    continue

                if chr not in counter_dict:
                    counter_dict[chr] = 1
                else:
                    print("char repeat", chr)
                    flag = False
    if flag:
        print("nonduplicate")


def main():
    input_file = "千字文.txt"
    check_nonduplicate(input_file)


if __name__ == "__main__":
    main()
