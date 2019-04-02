import sys
import os
import subprocess
import datetime
import get_function_info as info

info_file = "test/function_info.txt"



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


def function_checker(function):
    """
    Check selected function whether contained a self defined struct

    :param function:
    :return:
    """
    types = get_regular_types("utilties/types.txt")
    pointer_counter = 0
    regular_para_nonepointer = []
    regular_para_pointer = []
    struct_para = []
    for para in function.inputs:
        if not is_regular_type(types, para.var_type):
            print("Self Defined Structs Detected: " + para.var_type + " " + para.var_name + "\n")
            if para.pointer_num>=2:
                print("Function Not Yet Supported\n")
                break
            struct_para.append(para)
        else:
            #para.pointer_num != 0:
            print("Regular Type Detected: " + para.var_type + " " + para.var_name + "\n")
            if para.pointer_num != 0:
                pointer_counter += 1
                regular_para_pointer.append(para)
                if pointer_counter >= 2:
                    print("Function Not Yet Supported\n")
                    break
            else:
                regular_para_nonepointer.append(para)
    return [regular_para_nonepointer, regular_para_pointer, struct_para]


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
    """
    Generate header

    :param filename:
    :param function:
    :return:
    """
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
    string = "fseek(infile,0,SEEK_END);\n"
    string += "int fileSize = (int)ftell(infile);\n"
    string += "rewind(infile);"
    infile.write(string)
    [regular_para_nonepointer, regular_para_pointer, struct_para] = formalized_fn
    string = "int minSize ="
    if len(struct_para) == 0:
        for para in regular_para_nonepointer:
            string = string + " sizeof(" + para.var_type + ") +"
        for para in regular_para_pointer:
            string = string + " sizeof(" + para.var_type + ") +"
        if string[-1] == "+":
            string = string[:-2] + ";\n"
        infile.write(string)
        string = "if( minSize>fileSize ) {fclose(infile);return 0;}"
        infile.write(string)
        for para in regular_para_nonepointer:
            string = ""
            string = string + para.var_type + " * df_buffer_" + para.var_name + "="
            string = string + "(" + para.var_type + "*)" + "malloc("+" sizeof(" + para.var_type +")"+");\n"
            # fread(buffer,sizeof(int16_t),1,infile);
            infile.write(string)
            string = ""
            string = string + "fread(" + "df_buffer_" + para.var_name + ",sizeof(" + para.var_type + "), 1 , infile); "
            infile.write(string)
            string = ""
            string = string + para.var_type + " " + para.var_name + "=" + "*df_buffer_" + para.var_name + ";"
            string = string + "free(" + "df_buffer_" + para.var_name + ");"
            infile.write(string)
    infile.close()
    for para in regular_para_nonepointer:
        para.input_dump()
    for para in regular_para_pointer:
        para.input_dump()


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
    infile.write("return 0;\n}\n")
    infile.close()


def generate_src(function):
    filename = generate_filename(function)
    if os.path.exists(filename):
        os.remove(filename)
    formalized_fn = function_checker(function)
    generate_comment(filename, function)
    generate_header(filename, function)
    input_wrapper(filename, formalized_fn)
    generate_fuzz(filename, function)
    formatter(filename)


def formatter(filename):
    os.system('clang-format -style="{BasedOnStyle: llvm, IndentWidth: 4}" ' + filename + " > " + filename + ".format")
    os.system("mv "+filename + ".format " + filename)


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