import os
import sys

import interfaceGen as gen
import list_function
import get_function_info

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python " + 'get_function_info.py' + " FileName")
    filename = sys.argv[1]
    if not os.path.exists(filename):
        sys.exit("Error: File '" + sys.argv[1] + "' not found")
    list_function.main(filename)
    fn = get_function_info.get_info("cache/function_info.txt")
    gen.function_checker(fn)