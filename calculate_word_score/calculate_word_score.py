"""
ref= https://www.slideshare.net/charlesfong/attitude-100-presentation
This program can help us convert a word to its score, and check Internet rumor.

"""


def calculate_word_score(word: str) -> int:
    score = 0
    for char in word:
        c = ord(char)
        add = 0
        if ord('a') <= c <= ord('z'):
            add = c - ord('a') + 1
        elif ord('A') <= c <= ord('Z'):
            add = c - ord('A') + 1

        # print(char, add)

        score += add

    return score


def main():
    words = ["Attitude", "knowledge", "Workhard", "love", "luck", "money", "leadership",
             "Pneumonoultramicroscopicsilicovolcanoconiosis", "ZZZ"]

    for word in words:
        score = calculate_word_score(word)
        print("{0}, score= {1}".format(word, score))


if __name__ == "__main__":
    main()
