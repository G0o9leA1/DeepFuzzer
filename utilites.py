import os
import time
import structfinder
import list_function as info


class NotSupport(BaseException):
    """
    self defined exception
    """
    pass


def get_regular_types(filename):
    """
    get regular types from file

    :param filename: regular_type file name
    :return: regular types dictionary
    """
    types = set()
    infile = open(filename, "rt")
    for line in infile.readlines():
        types.add(line.split("\n")[0])
        types.add("const "+line.split("\n")[0])
    #print(types)
    return types


def function_checker(function, debug=False):
    """
    check function is compatible to deepfuzzer or not
    :param function: function need to be checked
    :param debug: enable debug print
    :return: if function is not compatible return error, else return a formalized function
    """
    # function.info_dump()
    # pointer_counter = 0
    regular_para_nonepointer = []
    regular_para_pointer = []
    struct_para = []
    for para in function.inputs:
        var_type = para.var_type
        if para.var_type.rfind(' ') !=-1:
            var_type = para.var_type[para.var_type.rfind(' ')+1:]

        if not is_regular_type(var_type):
            # return "Error"
            if debug:
                print("Self Defined Structs Detected: " + para.var_type + " " + para.var_name)
            if para.pointer_num >= 2:
                if debug:
                    print("Function Not Yet Supported\n")
            struct_info = dict()
            if not struct_checker(para, function, struct_info):
                return "Error"
            para.write_struct_info(struct_info)
            struct_para.append(para)

        else:
            if debug:
                print("Regular Type Detected: " + para.var_type + " " + para.var_name)
            if para.pointer_num > 1:
                if debug:
                    print("Function Not Yet Supported\n")
            if para.pointer_num == 0:
                regular_para_nonepointer.append(para)
            if para.pointer_num >= 1:
                regular_para_pointer.append(para)
    return [regular_para_nonepointer, regular_para_pointer, struct_para]


def struct_checker(para, function, struct_info):
    """
    check self-defined structure is compatible with deepfuzzer or not
    :param para: argument is self-defined structure
    :param function: function contain the self-defined structure
    :param struct_info: a dict contains the info of the struct
    :return: struct_info: a dict contains the info of the struct
    """
    # para.input_dump()
    struct = structfinder.build(para.var_name, para.var_type, function.source_dir, function.header_dir)
    struct_info[para.var_type] = []
    # struct.print_components()
    if not struct.components:
        return False
    else:
        for component in struct.components:
            if component[3] != 0:
                component[1] = component[1][:component[1].find('[')]
            struct_para = info.FnInput("")
            struct_para.set_input(component)
            struct_info[para.var_type].append(struct_para)
            # recursively check until all the para in struct is regular type
            # print(struct_para.var_type)
            if struct_para.pointer_num == 0 and not is_regular_type(struct_para.var_type):
                # not compatible if struct contain it self eg. linked list
                struct.print_components()
                if struct_para.var_type in struct_info:
                    return False
                    # return False
                struct_checker(struct_para, function, struct_info)
    # for key in struct_info:
    #     for fn in struct_info[key]:
    #         fn.input_dump()
    return struct_info


def is_regular_type(var_type):
    """
    check a type is regular or not
    :param var_type: para type
    :return: True of False
    """
    regular_type = get_regular_types("utilities/types.txt")
    return var_type in regular_type


def compile_gen(include, linker, compiler='afl-gcc'):
    """
    Try to compile
    :param compiler: CC
    :param include: -I
    :param linker: -L
    :return: no return
    """
    alib = linker[linker.rfind('/')+1:]
    linker = '-L ' + linker[:linker.rfind('/')] + ' -l' + alib.replace('lib', '', 1).replace('.a','',1)
    c_files = os.popen("find cache -name '*.c'").read().split("\n")
    for i in range(0, len(c_files)):
        c_files[i] = c_files[i][c_files[i].find('cache/')+6:]
    infile = open('utilities/compile_flag.txt','r')
    extra_linker_flag = ' '
    for line in infile:
        if line[0:2] == 'CC=':
            compiler = line[3:]
        if line[0:11] == 'LinkerFlag=':
            extra_linker_flag += line[11:-1]
    linker = linker + extra_linker_flag
    for c_file in c_files:
        if c_file == "":
            continue
        print_green(
            compiler + " cache/" + c_file + " -I " + include + " " + linker + " -static -o cache/" + c_file[:-2])
        os.popen(
            compiler + " -w cache/" + c_file + " -I " + include + " " + linker + " -static -o cache/" + c_file[:-2])
        time.sleep(.1)


def print_green(string, end="\n"):
    """
    print log in green
    :param string: string
    :param end: end
    :return:
    """
    print('\033[1;32m '+string+' \033[0m', end=end)


def print_red(string, end="\n"):
    """
    print log in red
    :param string: string
    :param end: end
    :return:
    """
    print('\033[1;31m '+string+' \033[0m', end=end)


if __name__ == "__main__":
    # compile_gen("afl-gcc", "../sela/include/", "-lsela -L ../sela/ -lm")
    print_red("a")