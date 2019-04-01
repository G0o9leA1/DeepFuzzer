import sys
import os
import datetime
import get_function_info as info

info_file = "test/function_info.txt"

fn = info.get_info()


def get_regular_types(filename):
    types=set()
    infile = open(filename,"rt")
    for line in infile.readlines():
        types.add(line.split("\n")[0])
        types.add("const "+line.split("\n")[0])
    #print(types)
    return types


def function_checker(function):
    types = get_regular_types("utilties/types.txt")
    pointer_counter = 0
    regular_para = []
    struct_para = []
    for para in function.inputs:
        if not is_regular_type(types, para.var_type):
            print("Self Defined Structs Detected: " + para.var_type + " " + para.var_name + "\n")
            struct_para.append(para)
        else:
            #para.pointer_num != 0:
            print("Regular Type Detected: " + para.var_type + " " + para.var_name + "\n")
            if para.pointer_num != 0:
                pointer_counter += 1
                if pointer_counter >= 2:
                    print("Function Not Yet Supported\n")
                    break
            regular_para.append(para)
    return [regular_para, struct_para]


def is_regular_type(regular_type, var_type):
    return var_type in regular_type


def generate_filename(function):
    return "cache/" + function.fn_name + "_fuzz.c"


def generate_comment(filename, function):
    infile = open(filename, "at")
    string = "/*\n* Generate by Deepfuzzer\n"
    infile.write(string)
    string = "* Target Function: " +function.fn_name + "\n"
    infile.write(string)
    now = datetime.datetime.now()
    string = "* Time: " + str(now)+"\n*/\n\n"
    infile.write(string)
    infile.close()


def generate_header(filename, function):
    infile = open(filename, "at")
    string = ""
    for include in function.includes:
        string += include+"\n"
    string += "\n"+"#include <inttypes.h>\n"+"#include <stdlib.h>\n"
    infile.write(string+"\n")
    infile.close()


def generate_debug(content):
    exit()


def input_wrapper(filename,formalized_fn):
    infile = open(filename, "at")
    string = "int main(int argc, char **argv)\n{\n"
    string += 'FILE *infile = fopen(argv[1],"rb");\n'
    infile.write(string)

    infile.close()

def define_var():
    exit()


def allocate_mem():
    exit()


def generate_fuzz(filename,function):
    infile = open(filename, "at")
    string = ""
    for para in function.inputs:
        string += para.var_name+","
    if string[-1] == ",":
        string = string[:-1]
    string = function.fn_name + "(" + string + ");\n"
    infile.write(string)
    infile.write("return 0;\n}")
    infile.close()


def generate_src(function):
    filename = generate_filename(function)
    formalized_fn = function_checker(function)
    generate_comment(filename, function)
    generate_header(filename, function)
    input_wrapper(filename, formalized_fn)
    generate_fuzz(filename, function)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        # sys.exit("Usage: python " + 'get_function_info.py' + " FileName")
        fn = info.get_info("test/function_info.txt")
        generate_src(fn)
        # fn=info.get_function_info(info_file)
        # filename=generate_filename(fn)
        # generate_header(filename,fn)
        # input_wrapper(filename)
        # generate_fuzz(filename,fn)
    else:
        filename = sys.argv[1]
        if not os.path.exists(filename):
            sys.exit("Error: File '" + sys.argv[1] + "' not found")
        fn=info.get_info(filename)