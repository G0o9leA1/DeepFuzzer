import re
info_file = "test/function_info.txt"


class FnInput:
    def __init__(self, string):
        self.var_name = re.findall(r'[\w]+$', string)[0]
        var_type = re.findall(r'^[\w?\s]+', string)[0]
        var_pointer = re.findall(r'\*', string)
        if var_type[-1] == ' ':
            var_type = var_type[:-1]
        self.var_type = var_type
        self.pointer_num = len(var_pointer)

    def input_dump(self):
        print('    Type: ' + self.var_type)
        print('    Pointer: ' + str(self.pointer_num))
        print('    Name: ' + self.var_name)
        print('')


class FnInfo:
    def __init__(self, name):
        self.fn_name = name
        self.inputs = []
        self.return_type = ""
        self.includes = []

    def info_dump(self):
        print('Function name: '+self.fn_name)
        print('Function parameters: ')
        for input_info in self.inputs:
            input_info.input_dump()
        print('Return type: '+self.return_type)
        print('Include: ')
        for include in self.includes:
            print('    '+include)


def get_function_info(info_file=info_file):
    function_info = open(info_file, 'r')
    for line in function_info:
        if line.split(':')[0] == 'FunctionName':
            fn_name = ((line.split('\n')[0]).split(':')[1])
            fn = FnInfo(fn_name)
        if line.split(':')[0] == 'Input':
            for para in ((line.split('\n')[0]).split(':')[1]).split(','):
                fn.inputs.append(FnInput(para))
        if line.split(':')[0] == 'ReturnType':
            fn.return_type = (line.split('\n')[0]).split(':')[1]
        if line.split(':')[0] == 'Include':
            for include in ((line.split('\n')[0]).split(':')[1]).split(','):
                fn.includes.append(include)
    function_info.close()
    fn.info_dump()

if __name__ == "__main__":
    get_function_info()