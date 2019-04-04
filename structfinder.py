import sys, os, re

def meepers(struct, sourcecode, headerfolder):
    sourcecode = open(sourcecode, "r+")
    newfile = open("cache/structure_info.txt", "w")
    target = "struct " + struct
    found = False

    line = sourcecode.readline()
    while target not in line:
        line = sourcecode.readline()

    if target in line:
        #case of struct x {
        if '{' in line:
            structinfo = line
            structinfo = sourcecode.readline()
            while '}' not in structinfo:
                list = structinfo.split()
                text = list[0] + ": " + ''.join(list[1:]) + '\n';
                newfile.write(text)

                structinfo = sourcecode.readline()
        #case of struct x
        #{
        else:
            structinfo = sourcecode.readline()
            structinfo = sourcecode.readline()
            while '}' not in structinfo:
                list = structinfo.split()
                text = list[0] + ": " + ''.join(list[1:]) + '\n';
                newfile.write(text)

                structinfo = sourcecode.readline()

    sourcecode.close()
    newfile.close()


meepers('apev2_hdr_ftr', 'test/structtest.c', 'a')
