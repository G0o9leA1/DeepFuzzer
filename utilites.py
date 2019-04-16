import os
import time
import sys


class NotSupport(BaseException):
    pass


def get_regular_types(filename):
    """
    get regular types from file

    :param filename:
    :return:
    """
    types = set()
    infile = open(filename,"rt")
    for line in infile.readlines():
        types.add(line.split("\n")[0])
        types.add("const "+line.split("\n")[0])
    #print(types)
    return types


def function_checker(function, debug=False):

    pointer_counter = 0
    regular_para_nonepointer = []
    regular_para_pointer = []
    struct_para = []
    for para in function.inputs:
        if not is_regular_type(para.var_type):
            # return "Error"
            if debug:
                print("Self Defined Structs Detected: " + para.var_type + " " + para.var_name)
            if para.pointer_num >= 2:
                if debug:
                    print("Function Not Yet Supported\n")
                return "Error"
            struct_para.append(para)

        else:
            if debug:
                print("Regular Type Detected: " + para.var_type + " " + para.var_name)
            if para.pointer_num > 1:
                if debug:
                    print("Function Not Yet Supported\n")
                return "Error"
            if para.pointer_num == 0:
                regular_para_nonepointer.append(para)
            if para.pointer_num == 1:
                regular_para_pointer.append(para)
    return [regular_para_nonepointer, regular_para_pointer, struct_para]


def is_regular_type(var_type):
    regular_type = get_regular_types("utilties/types.txt")
    return var_type in regular_type


def compile_gen(compiler,include,linker):
    c_files = os.popen("find cache -name '*.c'").read().split("\n")
    for i in range(0, len(c_files)):
        c_files[i] = c_files[i][c_files[i].find('cache/')+6:]
    for c_file in c_files:
        if c_file == "":
            continue
        print_green(compiler + " cache/" + c_file + " -I " + include + " " + linker + " -static -o cache/" + c_file[:-2])
        os.popen(
            compiler + " -w cache/" + c_file + " -I " + include + " " + linker + " -static -o cache/" + c_file[:-2])
        time.sleep(.1)


def print_green(string, end="\n"):
    print('\033[1;32m '+string+' \033[0m', end=end)


def print_red(string, end="\n"):
    print('\033[1;31m '+string+' \033[0m', end=end)


if __name__ == "__main__":
    # compile_gen("afl-gcc", "../sela/include/", "-lsela -L ../sela/ -lm")
    print_red("a")