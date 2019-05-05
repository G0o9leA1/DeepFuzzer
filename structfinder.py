import sys
import os
import re
import glob


class StructureInfo:
    def __init__(self, name, structure, source_dir, header_dir):
        self.components = []  # structure definition in the form of [type, name, pointer, length]
        self.verbose_components = []  # has full structure definition w/o parse
        self.file_list = []
        self.structure = structure
        self.name = name
        self.source_dir = source_dir
        self.header_dir = header_dir
        self.target = 'struct ' + structure
        self.found_location = 'none'

    # clang-check -ast-dump -ast-dump-filter = rice_decode_context apev2.c -- -I.. / include / |
    # perl - pe 's/\e\[?.*?[\@-~]//g'

    def clang_struct_finder(self):
        # clang-check -ast-dump apev2.c -ast-dump-filter=apev2_hdr_ftr -- -I../include/ | perl -pe 's/\e\[?.*?[\@-~]//g'
        no_color = r" | perl -pe 's/\e\[?.*?[\@-~]//g'"
        if self.structure.find('struct ')==-1:
            structure_name = self.structure
        else:
            structure_name = self.structure[self.structure.find('struct ')+7:]
        cmd = 'clang-check -ast-dump ' + self.source_dir + ' -ast-dump-filter=' + structure_name + ' -- -I' + self.header_dir + no_color
        result = os.popen(cmd)
        for line in result:
            if line == '\n':
                break
            if line.find('FieldDecl') != -1:
                m = line[:-2].split('\'',1)
                # print(m)
                var_name = m[-2].split()[-1]
                var_type = m[-1]
                if var_type.find(':') != -1:
                    var_type = var_type[:var_type.find(':')]
                    var_type = var_type[:-1]
                pointer = var_type.count('*')
                var_type=re.sub(r'\s+','',var_type)
                var_type=var_type.replace('*', '')
                length =0
                if var_type.find('[')!=-1:
                    var_name= var_name+ var_type[var_type.find('['):]
                    length = re.search(r"\[([A-Za-z0-9_]+)\]", var_name)
                    length = int(length.group(1))
                    var_type=var_type[:var_type.find('[')]
                compond_info = [var_type, var_name, pointer, length]
                self.components.append(compond_info)
                # print('type: '+var_type+' name: ' + var_name+' pointer: ' + str(pointer) + ' length:'+ str(length))

    def file_lookup(self):
        self.file_list.append(self.source_dir)

        if self.header_dir != "":
            if self.header_dir[-1] == '\\' or self.header_dir[-1] == '/':
                self.header_dir = self.header_dir + "*"
            else:
                self.header_dir = self.header_dir + "/*"

            for filename in glob.glob(self.header_dir):
                self.file_list.append(filename)

    def parser_function(self):
        for filename in self.file_list:
            file = open(filename, "r+")
            line = file.readline()
            while self.target not in line:
                line = file.readline()
                if not line:
                    break

            if self.target in line:
                self.found_location = filename
                # case of struct x {
                if '{' in line:
                    structinfo = line
                    structinfo = file.readline()
                    while '}' not in structinfo:
                        list = structinfo.split()
                        text = list[0] + " " + ' '.join(list[1:]).replace(";", "").partition('//')[0]
                        self.verbose_components.append(text)

                        structinfo = file.readline()
                # case of struct x
                # {
                else:
                    structinfo = file.readline()
                    structinfo = file.readline()
                    while '}' not in structinfo:
                        list = structinfo.split()
                        text = list[0] + " " + ' '.join(list[1:]).replace(";", "").partition('//')[0]
                        self.verbose_components.append(text)

                        structinfo = file.readline()

                file.close()
                break

        file.close()

    def component_split(self):
        for comp in self.verbose_components:
            parts = comp.split()
            typer = parts[0]
            name = parts[1]
            pointer = parts[1].count('*')
            length = 0
            if '[' in parts[1]:
                length = re.search(r"\[([A-Za-z0-9_]+)\]", parts[1])
                length = int(length.group(1))
            if 'struct' in comp:
                typer = parts[0]+" "+parts[1]
                name = parts[2]
                pointer = parts[2].count('*')
            array = [typer, name.replace("*", ""), pointer, length]
            self.components.append(array)

    def set_structure(self,structure):
        self.structure = structure

    def set_source_dir(self, source):
        self.source_dir = source

    def set_header_dir(self, header_dir):
        self.header_dir = header_dir

    def print_verbose_comp(self):
        print(self.verbose_components)

    def print_file_list(self):
        print(self.file_list)

    def print_components(self):
        print(self.components)

    def print_found_location(self):
        print(self.found_location)


def build(name, structure, source_dir, header_dir):
    struct_info = StructureInfo(name, structure, source_dir, header_dir)
    # struct_info.file_lookup()
    # struct_info.parser_function()
    # struct_info.component_split()
    # struct_info.print_components()
    struct_info.clang_struct_finder()
    # struct_info.print_found_location()
    return struct_info


if __name__ == "__main__":
    # filename = sys.argv[1]
    stinfo=StructureInfo('a', 'apev2_item', '../sela/core/apev2.c', '../sela/include')
    stinfo.clang_struct_finder()

# return object containing arrays with Type, Name, Pointer (none,1,2,3), and length if necessary