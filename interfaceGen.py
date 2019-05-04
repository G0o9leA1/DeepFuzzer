import sys
import os
import subprocess
import list_function as info
import utilites
import structfinder

info_file = "test/function_info.txt"


def generate_filename(function):
    """
    generate interface name
    :param function: FnInfo Object
    :return: file name like "xxx_fuzz.c"
    """
    return "cache/" + function.fn_name + "_fuzz.c"


def generate_comment(file_name, function):
    """
    generate some useful comment
    :param file_name: file writen to
    :param function: FnInfo Object
    :return:
    """
    infile = open(file_name, "at")
    string = "/*\n* Generate by Deepfuzzer\n"
    infile.write(string)
    string = "* Target Function: " + function.prototype + "\n"
    infile.write(string)
    now = os.popen("date").read().split('\n')[0]
    string = "* Time: " + now+"\n*/\n\n"
    infile.write(string)
    infile.close()


def generate_header(file_name, function):
    """
    generate #include<header>
    :param file_name: file writen to
    :param function: FnInfo Object
    :return:
    """
    infile = open(file_name, "at")
    string = ""
    for include in function.includes:
        string += include+"\n"
    infile.write(string)
    infile.write("\n")
    if "#include <inttypes.h>" not in function.includes:
        infile.write("#include <inttypes.h>\n")
    if "#include <stdlib.h>" not in function.includes:
        infile.write("#include <stdlib.h>\n")
    infile.write("\n")
    infile.close()


def generate_debug(file_name, content):
    """
    generate some debug info
    :param file_name: file written to
    :param content: debug message
    :return:
    """
    exit()


def read_regular_type(para, file_name, min_size):
    """
    generate source code for a regular type
    eg. int32_t num_elements;
        fread(&num_elements, sizeof(int32_t), 1, infile);
    :param para: variable
    :param file_name: file written to
    :param min_size: cumulative size
    :return: cumulative size and size to read this data
    """
    min_size = min_size + "+sizeof(" + para.var_type + ")"
    check_file_size(min_size, file_name)
    infile = open(file_name, 'at')
    # int32_t num_elements;
    string = para.var_type+" "+para.var_name+";"
    # fread(&num_elements, sizeof(int32_t), 1, infile);
    string = string + "fread(&" + para.var_name + ", sizeof(" + para.var_type + "),1,infile);\n\n"
    infile.write(string)
    infile.close()
    return min_size


def read_array_length(para, file_name, min_size):
    """
    generate source code for a array length
    :param para: variable
    :param file_name: file written to
    :param min_size: cumulative size
    :return: cumulative size and size to read this data
    """

    # int pointer_size_data = 1;
    string = "int " + "pointer_size_" + para.var_name + "=" + str(para.pointer_num) + ";"
    infile = open(file_name, 'at')
    infile.write(string)
    infile.close()

    # min_size = min_size + sizeof(uint16_t) * pointer_size_data = 1
    min_size = min_size + "+sizeof(uint16_t) * " + "pointer_size_" + para.var_name
    check_file_size(min_size, file_name)
    infile = open(file_name, 'at')
    string = ""
    for i in range(para.pointer_num):
        string = string + "uint16_t d" + str(i + 1) + "_" + para.var_name + ";\n"
        # fread( & d1_data, sizeof(uint16_t), 1, infile);
        string = string + "fread(&d" + str(i + 1) + "_" + para.var_name + ",sizeof(uint16_t),1,infile);"
    # print(string)
    infile.write(string)
    infile.close()

    return min_size


def read_array_data(para, file_name, min_size):
    """
        generate source code for read data for an array
        :param para: variable
        :param file_name: file written to
        :param min_size: cumulative size
        :return: cumulative size and size to read this data
        """
    string = ""
    for i in range(para.pointer_num):
        string = string + "d" + str(i + 1) + "_" + para.var_name + "*"
    min_size = min_size + "+sizeof("+ para.var_type + ")*" +string[:-1]
    check_file_size(min_size,file_name)
    infile = open(file_name, 'at')
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
    return min_size


def check_file_size(size, file_name):
    """
    compare min_size with file_size
    # if (fileSize < sizeof(uint16_t) * pointer_size) {
    # fclose(infile);
    # return 0;
    # }
    :param size: min_size
    :param file_name: file written to
    :return:
    """
    infile = open(file_name, 'at')
    string = "if(fileSize < " + size + "){fclose(infile);return 0;}"
    infile.write(string)
    infile.close()


def read_const_array_data(para, file_name, min_size, length):
    """
    generate source code for read data for a length-fixed array
    :param para: variable
    :param file_name: file written to
    :param min_size: min_size
    :param length: length of array
    :return: cumulative size and size to read this data
    """
    infile = open(file_name, 'at')
    para.pointer_num = para.pointer_num + 1
    string = "uint16_t d" + str(1) + "_" + para.var_name + "=" + str(length) + ";\n"
    infile.write(string)
    infile.close()
    min_size = read_array_data(para, file_name, min_size)
    para.pointer_num = para.pointer_num - 1
    return min_size


def read_struct_null_pointer(para, file_name):
    infile = open(file_name, 'at')
    string = "struct " + para.var_type + " "
    for star in range(para.pointer_num):
        string += '*'
    string = string + " " + para.var_name + " =NULL;"
    print(string)
    infile.write(string)
    infile.close()


def read_struct(para, struct, file_name, min_size):
    for struct_para in para.struct_info[struct]:
        if not utilites.is_regular_type(struct_para.var_type):
            if struct_para.pointer_num == 0:
                min_size = read_struct(para, struct_para.var_type, file_name, min_size)
            else:
                read_struct_null_pointer(struct_para, file_name)
        else:
            if struct_para.pointer_num == 0:
                if struct_para.array_length == 0:
                    min_size = read_regular_type(struct_para, file_name, min_size)
                else:
                    min_size = read_const_array_data(struct_para, file_name, min_size, para.array_length)
            else:
                min_size = read_array_length(struct_para, file_name, min_size)
                min_size = read_array_data(struct_para, file_name, min_size)

    infile = open(file_name, "at")
    if struct != para.var_type:
        infile.write("struct " + struct + " reference_" + struct + "={ ")
        string = ""
        for struct_para in para.struct_info[struct]:
            string = string + struct_para + ','
        string = string[:-1] + "};"
        string = string + "struct " + struct + " *" + struct + "= &reference_" + struct + ";"
    else:
        infile.write("struct " + struct + " reference_" + para.var_name + "={ ")
        string = ""
        for struct_para in para.struct_info[struct]:
            string = string + struct_para.var_name + ','
        string = string[:-1] + "};"
        string = string + "struct " + para.var_type + " *" + para.var_name + "= &reference_" + para.var_name + ";"
    infile.write(string)
    infile.close()
    return min_size


def input_wrapper(file_name, formalized_fn, function):
    """
    generate main function
    :param file_name: file written to
    :param formalized_fn: formalized function
    :param function: FnInfo Object
    :return:
    """
    infile = open(file_name, "at")
    # Open File and read fileSize
    string = "int main(int argc, char **argv){"
    string += 'FILE *infile = fopen(argv[1],"rb");\n\n'
    infile.write(string)
    string = "fseek(infile,0,SEEK_END);"
    string += "int fileSize = (int)ftell(infile);int minSize = 0;"
    string += "rewind(infile);\n\n"
    infile.write(string)
    infile.close()

    [regular_para_nonepointer, regular_para_pointer, struct_para] = formalized_fn
    string = ""
    min_size = "minSize"

    # generate source code for struct
    if len(struct_para) != 0:
        print(struct_para)
        for para in struct_para:
            min_size = read_struct(para, para.var_type, file_name, min_size)

    if regular_para_pointer is not None:
        for para in regular_para_pointer:
            min_size = read_array_length(para, file_name, min_size)
            min_size = read_array_data(para, file_name, min_size)
    for para in regular_para_nonepointer:
        if para.array_length == 0:
            min_size = read_regular_type(para, file_name, min_size)
        else:
            min_size = read_const_array_data(para, file_name, min_size, para.array_length)


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


def generate_fuzz(file_name, function):
    """
    call the target function
    :param file_name: file writen to
    :param function: FnInfo object
    :return:
    """
    infile = open(file_name, "at")
    string = ""
    for para in function.inputs:
        string += para.var_name+","
    if string[-1] == ",":
        string = string[:-1]
    string = function.fn_name + "(" + string + ");\n"
    infile.write(string)
    infile.write("\n")
    infile.write(r'printf("Test Passed!\n");')
    infile.write("\n\n")
    infile.write("return 0;\n}\n")
    infile.close()


def generate_src(function):
    """
    generate source code for target function
    :param function: FnInfo Object
    :return:
    """
    file_name = generate_filename(function)
    if os.path.exists(file_name):
        os.remove(file_name)
    formalized_fn = utilites.function_checker(function)
    generate_comment(file_name, function)
    generate_header(file_name, function)
    # input_wrapper(filename, formalized_fn)
    input_wrapper(file_name, formalized_fn, function)
    generate_fuzz(file_name, function)
    formatter(file_name)


def formatter(file_name):
    """
    Clang Formatter to format source code
    :param file_name: file written to
    :return:
    """
    os.system(
        'clang-format -style="{BasedOnStyle: Google, IndentWidth: 4}" -sort-includes=false ' + file_name + " > " + file_name + ".format")
    os.system("mv "+file_name + ".format " + file_name)


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