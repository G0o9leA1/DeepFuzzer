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
                typer = parts[1]
                name = parts[2]
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
    struct_info.file_lookup()
    struct_info.parser_function()
    struct_info.component_split()
    struct_info.print_found_location()
    return struct_info



if __name__ == "__main__":
    # filename = sys.argv[1]
    build(sys.argv[1], sys.argv[1], sys.argv[2], sys.argv[3]).print_components()

# return object containing arrays with Type, Name, Pointer (none,1,2,3), and length if necessary