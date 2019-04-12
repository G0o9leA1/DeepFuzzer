import os
import sys
import utilites
import interfaceGen as gen
import list_function as libobj
import get_function_info

if __name__ == "__main__":
    # python3 main.py
    if len(sys.argv) < 3:
        sys.exit(
            "Usage: python " + 'main.py' + " <source code path>" + " <compiled binary file path>" + " <include directory path>")
    source_dir = sys.argv[1]
    binary_dir = sys.argv[2]
    include_dir = sys.argv[3]
    if not os.path.exists(source_dir):
        sys.exit("Error: File '" + sys.argv[1] + "' not found")
    if not os.path.exists(binary_dir):
        sys.exit("Error: File '" + sys.argv[2] + "' not found")
    if not os.path.exists(include_dir):
        sys.exit("Error: File '" + sys.argv[3] + "' not found")

    lib_info = libobj.LibraryInfo(source_dir, binary_dir, include_dir)
    print("Library: "+lib_info.name)
    print("Source Code Path: "+lib_info.source_dir)
    print("Compiled Binary Path:"+lib_info.binary_dir)
    print("Include Directory Path:"+include_dir)
    lib_info.function_list_gen()
    lib_info.parse_function()
    lib_info.includes_gen()
    lib_info.sum_passed()
    lib_info.build_stat()
    print("Please Type the name of one of the passed functions")
    print("If you want to generate all the fuzzable target, please press enter")
    function_name = input()
    if function_name == "":
        for function_name in lib_info.passed_functions:
            print("Writing harness for " + function_name)
            fn = lib_info.passed_functions[function_name]
            fn.write_includes(lib_info.includes)
            gen.generate_src(fn)
            print("Done for " + function_name)

    if function_name in lib_info.passed_functions:
        fn = lib_info.passed_functions[function_name]
        fn.write_includes(lib_info.includes)
        gen.generate_src(fn)