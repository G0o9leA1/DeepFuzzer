import sys
import os
import get_function_info as info

info_file = "test/function_info.txt"

fn = info.get_function_info()


def generate_filename(function):
    exit()


def generate_comment(filename,function):
    exit()


def generate_header(filename,includes):
    exit()


def generate_debug(content):
    exit()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        # sys.exit("Usage: python " + 'get_function_info.py' + " FileName")
        fn=info.get_function_info(info_file).info_dump()
    else:
        filename = sys.argv[1]
        if not os.path.exists(filename):
            sys.exit("Error: File '" + sys.argv[1] + "' not found")
        fn=info.get_function_info(filename)