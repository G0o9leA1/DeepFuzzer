import sys
import os
import subprocess
import get_function_info as info
import utilites

info_file = "test/function_info.txt"


def generate_filename(function):
    return "cache/" + function.fn_name + "_fuzz.c"


def generate_comment(filename, function):
    infile = open(filename, "at")
    string = "/*\n* Generate by Deepfuzzer\n"
    infile.write(string)
    string = "* Target Function: " +function.prototype + "\n"
    infile.write(string)
    now = os.popen("date").read().split('\n')[0]
    string = "* Time: " + now+"\n*/\n\n"
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
    infile.write(string)
    infile.write("\n")
    if "#include <inttypes.h>" not in function.includes:
        infile.write("#include <inttypes.h>\n")
    if "#include <stdlib.h>" not in function.includes:
        infile.write("#include <stdlib.h>\n")
    infile.write("\n")
    infile.close()


def generate_debug(content):
    exit()


def read_regular_type(var_type, var_name, file_name, minSize):
    minSize = minSize + "+sizeof(" + var_type + ")"
    check_file_size(minSize,file_name)
    infile = open(file_name, 'at')
    # int32_t num_elements;
    string = var_type+" "+var_name+";"
    # fread(&num_elements, sizeof(int32_t), 1, infile);
    string = string + "fread(&" + var_name + ", sizeof(" + var_type + "),1,infile);\n\n"
    infile.write(string)
    infile.close()
    return minSize


def read_array_length(para, file_name, minSize):
    string = "int " + "pointer_size_" + para.var_name + "=" + str(para.pointer_num) + ";"
    infile = open(file_name, 'at')
    infile.write(string)
    infile.close()
    minSize = minSize + "+sizeof(uint16_t) * " + "pointer_size_" + para.var_name
    check_file_size(minSize, file_name)
    infile = open(file_name, 'at')
    # int pointer_size = 1;
    string = ""
    for i in range(para.pointer_num):
        string = string + "uint16_t d" + str(i + 1) + "_" + para.var_name + ";\n"
        # fread( & d1_data, sizeof(uint16_t), 1, infile);
        string = string + "fread(&d" + str(i + 1) + "_" + para.var_name + ",sizeof(uint16_t),1,infile);"
    # print(string)
    infile.write(string)
    infile.close()

    return minSize


def read_array_data(para, file_name, minSize):
    string = ""
    for i in range(para.pointer_num):
        string = string + "d" + str(i + 1) + "_" + para.var_name + "*"
    minSize = minSize + "+sizeof("+ para.var_type + ")*" +string[:-1]
    check_file_size(minSize,file_name)
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
    return minSize


def check_file_size(size, file_name):
    infile = open(file_name, 'at')
    # if (fileSize < sizeof(uint16_t) * pointer_size) {
    # fclose(infile);
    # return 0;
    # }
    string = "if(fileSize < " + size + "){fclose(infile);return 0;}"
    infile.write(string)
    infile.close()


def new_wrapper(filename,formalized_fn):
    infile = open(filename, "at")
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
    minSize = "minSize"
    if len(struct_para) == 0:
        if regular_para_pointer is not None:
            for para in regular_para_pointer:
                minSize = read_array_length(para, filename, minSize)
                minSize = read_array_data(para,filename, minSize)
        for para in regular_para_nonepointer:
            minSize = read_regular_type(para.var_type,para.var_name,filename,minSize)





def input_wrapper(filename,formalized_fn):
    infile = open(filename, "at")
    string = "int main(int argc, char **argv){"
    string += 'FILE *infile = fopen(argv[1],"rb");\n\n'
    infile.write(string)
    string = "fseek(infile,0,SEEK_END);"
    string += "int fileSize = (int)ftell(infile);"
    string += "rewind(infile);\n\n"
    infile.write(string)
    infile.close()
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
    infile.write("\n")
    infile.write(r'printf("Test Passed!\n");')
    infile.write("\n\n")
    infile.write("return 0;\n}\n")
    infile.close()


def generate_src(function):
    filename = generate_filename(function)
    if os.path.exists(filename):
        os.remove(filename)
    formalized_fn = utilites.function_checker(function)
    generate_comment(filename, function)
    generate_header(filename, function)
    # input_wrapper(filename, formalized_fn)
    new_wrapper(filename, formalized_fn)
    generate_fuzz(filename, function)
    formatter(filename)


def formatter(filename):
    os.system(
        'clang-format -style="{BasedOnStyle: Chromium, IndentWidth: 4}" -sort-includes=false ' + filename + " > " + filename + ".format")
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