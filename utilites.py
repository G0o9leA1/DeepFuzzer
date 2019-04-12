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

    types = get_regular_types("utilties/types.txt")
    pointer_counter = 0
    regular_para_nonepointer = []
    regular_para_pointer = []
    struct_para = []
    for para in function.inputs:
        if not is_regular_type(types, para.var_type):
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


def is_regular_type(regular_type, var_type):
    return var_type in regular_type