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


def read_regular_type(var_type, var_name, file_name):
    infile = open(file_name, 'at')
    # int32_t num_elements;
    string = var_type+" "+var_name+";"
    # fread(&num_elements, sizeof(int32_t), 1, infile);
    string = string + "fread(&" + var_name + ", sizeof(" + var_type + "),1,infile);"
    print(string)
    infile.write(string)
    infile.close()
    size = "sizeof(" + var_type + ")"
    return size


def read_array_length(para, file_name):
    infile = open(file_name, 'at')
    # int pointer_size = 1;
    string = "int " + "pointer_size_" + para.var_name + "=" + str(para.pointer_num) + ";"
    for i in range(para.pointer_num):
        string = string + "uint16_t d" + str(i + 1) + "_" + para.var_name + ";\n"
        # fread( & d1_data, sizeof(uint16_t), 1, infile);
        string = string + "fread(&d" + str(i + 1) + "_" + para.var_name + ",sizeof(uint16_t),1,infile);\n\n"
    print(string)
    infile.write(string)
    infile.close()

    # sizeof(uint16_t) * pointer_size
    size = "sizeof(uint16_t) * " + "pointer_size_" + para.var_name
    return size


def new_wrapper(filename,formalized_fn):
    infile = open(filename, "at")
    string = "int main(int argc, char **argv){"
    string += 'FILE *infile = fopen(argv[1],"rb");\n\n'
    infile.write(string)
    string = "fseek(infile,0,SEEK_END);"
    string += "int fileSize = (int)ftell(infile);"
    string += "rewind(infile);\n\n"
    infile.write(string)
    [regular_para_nonepointer, regular_para_pointer, struct_para] = formalized_fn
    string = ""
    if len(struct_para) == 0:
        if regular_para_pointer is not None:
            for para in regular_para_pointer:
                read_array_length(para, filename)
        for para in regular_para_nonepointer:
            read_regular_type(para.var_name,para.var_type,filename)





def input_wrapper(filename,formalized_fn):
    infile = open(filename, "at")
    string = "int main(int argc, char **argv){"
    string += 'FILE *infile = fopen(argv[1],"rb");\n\n'
    infile.write(string)
    string = "fseek(infile,0,SEEK_END);"
    string += "int fileSize = (int)ftell(infile);"
    string += "rewind(infile);\n\n"
    infile.write(string)
    [regular_para_nonepointer, regular_para_pointer, struct_para] = formalized_fn
    string = ""
    if len(struct_para) == 0:
        if regular_para_pointer is None:
            infile.write("int pointer_size = 1;")
        else:
            pointer_size = 0
            for para in regular_para_pointer:
                pointer_size += para.pointer_num
            infile.write("int pointer_size =" + str(pointer_size) + ";")

        # if (fileSize < sizeof(uint16_t) * pointer_size) {
        # return 0;
        # }

        infile.write("if(fileSize < sizeof(uint16_t)*pointer_size){fclose(infile);return 0;}\n\n")

        for para in regular_para_pointer:
            for i in range(para.pointer_num):
                string = string + "uint16_t d" + str(i+1) + "_" + para.var_name + ";\n"
                # fread( & d1_data, sizeof(uint16_t), 1, infile);
                string = string + "fread(&d" + str(i+1) + "_" + para.var_name + ",sizeof(uint16_t),1,infile);\n\n"
        infile.write(string)
        # int minSize = sizeof(uint16_t) * pointer_size + sizeof(int) * d1_data + sizeof(int32_t);
        string = "int minSize = sizeof(uint16_t)*pointer_size"

        for para in regular_para_pointer:
            string = string + "+sizeof(" + para.var_type + ")"
            for i in range(para.pointer_num):
                string = string + "*d" + str(i+1) + "_" + para.var_name

        for para in regular_para_nonepointer:
            string = string + "+sizeof(" + para.var_type + ")"

        string = string + ";\n"
        infile.write(string)
        string = "if( minSize>fileSize ) {fclose(infile);return 0;}\n\n"
        infile.write(string)

        # int reference_data[d1_data];
        # for (int i = 0; i < d1_data; ++i) {
        #     int tmp_data;
        # fread( & tmp_data, sizeof(int), 1, infile);
        # reference_data[i] = tmp_data;
        # }
        # const int16_t * data = reference_data;

        for para in regular_para_pointer:
            string = ""

            # int reference_data[d1_data];
            if para.var_type.find("const") == 0:
                string = string + para.var_type[6:]
            else:
                string = string + para.var_type
            string = string + " reference_" + para.var_name + "["
            for i in range(para.pointer_num):
                string = string + "d" + str(i + 1) + "_" + para.var_name + "*"
            string = string[:-1] + "];"

            # for (int i = 0; i < d1_data; ++i) {
            string = string + "for(long int i=0;i<"
            for i in range(para.pointer_num):
                string = string + "d" + str(i + 1) + "_" + para.var_name + "*"
            string = string[:-1] + ";++i){"
            #     int tmp_data;
            if para.var_type.find("const") == 0:
                string = string + para.var_type[6:]
            else:
                string = string + para.var_type
            string = string + " tmp" + "_" + para.var_name + ";"

            # fread( & tmp_data, sizeof(int), 1, infile);
            string = string + "fread(&" + "tmp" + "_" + para.var_name + ",sizeof(" + para.var_type + "),1,infile);"

            # reference_data[i] = tmp_data;
            string = string + " reference_" + para.var_name + "[i] = " + "tmp" + "_" + para.var_name + ";}"

            # const int16_t * data = reference_data;
            string = string + para.var_type + " "
            for i in range(para.pointer_num):
                string = string + "*"
            string = string + para.var_name + "= reference_" + para.var_name + ";\n\n"
            infile.write(string)

        for para in regular_para_nonepointer:
            string = ""
            string = string + para.var_type + " " + para.var_name + ";"
            # fread(&num_elements, sizeof(int32_t), 1, infile);
            string = string + "fread(&" + para.var_name + ",sizeof(" + para.var_type + "),1,infile);\n\n"
            infile.write(string)
    for para in regular_para_nonepointer:
        para.input_dump()
    for para in regular_para_pointer:
        para.input_dump()
    infile.write("fclose(infile);\n\n")


def define_var():
    exit()


def allocate_mem(para, buffer_name, buffer_type, buffer_count, filename):
    infile = open(filename, "at")
    string = ""
    string = string + buffer_type + " * " + buffer_name + "="
    string = string + "(" + buffer_type + "*)" + "malloc(" + " sizeof(" + buffer_type + ")*" + str(
        buffer_count) + ");\n"
    # fread(buffer,sizeof(int16_t),1,infile);
    infile.write(string)
    string = ""
    string = string + "fread(" + buffer_name + ",sizeof(" + buffer_type + "), " + str(buffer_count) + " , infile); "
    infile.write(string)
    string = ""
    string = string + para.var_type + " " + para.var_name + "=" + "*df_buffer_" + para.var_name + ";"
    string = string + "free(" + buffer_name + ");\n\n"
    infile.write(string)
    infile.close()

# def read_data()


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
    # input_wrapper(filename, formalized_fn)
    new_wrapper(filename, formalized_fn)
    generate_fuzz(filename, function)
    formatter(filename)


def formatter(filename):
    os.system(
        'clang-format -style="{BasedOnStyle: Chromium, IndentWidth: 4}" ' + filename + " > " + filename + ".format")
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