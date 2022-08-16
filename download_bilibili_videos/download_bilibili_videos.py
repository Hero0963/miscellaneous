""""
This program will download videos by You-Get package:
https://github.com/soimort/you-get
usage: save the url to url_list.txt, split each url by line, run this
program, it will download the videos by using command line
"""

# coding:utf-8
import os


def download_files():
    cmd_prefix = "you-get "
    file_name = "url_list.txt"

    with open(file_name, encoding="utf-8") as f:
        url = f.readline()
        while url:
            command = cmd_prefix + url
            os.system(command)
            url = f.readline()


def main():
    download_files()


if __name__ == "__main__":
    main()
