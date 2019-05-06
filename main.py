import os
import sys
import platform
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
    binary_dir = sys.argv[3]
    include_dir = sys.argv[2]
    if not os.path.exists(source_dir):
        sys.exit("Error: File '" + sys.argv[1] + "' not found")
    if not os.path.exists(binary_dir):
        sys.exit("Error: File '" + sys.argv[2] + "' not found")
    if not os.path.exists(include_dir):
        sys.exit("Error: File '" + sys.argv[3] + "' not found")

    lib_info = libobj.LibraryInfo(source_dir, include_dir, binary_dir)
    print("Library: "+lib_info.name)
    print("Source Code Path: "+lib_info.source_dir)
    print("Include Directory Path:"+lib_info.header_dir)
    print("Compiled Binary Path:"+lib_info.binary_dir)
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
            utilites.print_green("Writing harness for " + function_name + " ", "")
            try:
                fn = lib_info.passed_functions[function_name]
                fn.write_includes(lib_info.includes)
                fn.write_source_dir(lib_info.source_dir)
                fn.write_header_dir(lib_info.header_dir)
                gen.generate_src(fn)
                utilites.print_green("Done")
            except utilites.NotSupport:
                os.popen("rm cache/"+function_name+"_fuzz.c")
                utilites.print_red("Failed")
                pass
            except all:
                utilites.print_red("Failed")
                pass

    elif function_name in lib_info.passed_functions:
        utilites.print_green("Writing harness for " + function_name + " ", "")
        try:
            fn = lib_info.passed_functions[function_name]
            fn.write_includes(lib_info.includes)
            fn.write_source_dir(lib_info.source_dir)
            fn.write_header_dir(lib_info.header_dir)
            gen.generate_src(fn)
            utilites.print_green("Done")
        except utilites.NotSupport:
            os.popen("rm cache/" + function_name + "_fuzz.c")
            utilites.print_red("Failed")
            pass
        except all:
            utilites.print_red("Failed")
            pass

    if platform.system() == "Linux":
        print("Try to compile!")
        utilites.print_red("NOTE: Compile may fail for multiple reasons, Please CHECK AGAIN")
        utilites.compile_gen(include_dir, binary_dir)
        utilites.postprocess()
        utilites.print_green('Generated Harness Source Code in out/src')
        utilites.print_green('Generated Executable in out/bin')
