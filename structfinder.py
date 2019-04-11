import sys, os, re, glob

def main(struct, sourcecode, headerfolder):
    sourcecode = open(sourcecode, "r+")

    found = False

    found = parser(struct, sourcecode)

    if(headerfolder != ""):
        headerfolder = headerfolder + "*"
        for filename in glob.glob(headerfolder):
            if(found == False):
                headerfile = open(filename, "r+")
                found = parser(struct, headerfile)

def parser(struct, file):
    newfile = open("cache/structure_info.txt", "w")

    target = "struct " + struct
    line = file.readline()
    #print(line)
    while target not in line:
        line = file.readline()
        if not line:
            break

    if target in line:
        #case of struct x {
        if '{' in line:
            structinfo = line
            structinfo = file.readline()
            while '}' not in structinfo:
                list = structinfo.split()
                text = list[0] + ": " + ''.join(list[1:]) + '\n'
                newfile.write(text)

                structinfo = file.readline()
        #case of struct x
        #{
        else:
            structinfo = file.readline()
            structinfo = file.readline()
            while '}' not in structinfo:
                list = structinfo.split()
                text = list[0] + ": " + ''.join(list[1:]) + '\n'
                newfile.write(text)

                structinfo = file.readline()

        file.close()
        newfile.close()
        return True

    file.close()
    newfile.close()
    return False

if __name__ == "__main__":
	# filename = sys.argv[1]
	main(sys.argv[1],sys.argv[2],sys.argv[3])


#structfind('apev2_hdr_ftr', 'test/structtest.c', '')
