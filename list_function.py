#MUST INSTALL CTAGS PACKAGE BEFORE USE (apt-get install ctags)
import sys, os, re

def main(filename, compiledlib, includefold):


	file = open(filename, "r")

	#gets a list of all functions using ctags
	printout = os.popen("find "+filename+" -type f -name '*.[ch]' -exec ctags -x --c-kinds=f {} ';'").read()
	printout = printout.splitlines()

	functionlist = []

	#parses ctags output for last piece of each line
	for line in printout:
		function = line.split("           ")
		function = function[-1]
		functionlist.append(function)
		print(function)


	#asks user to choose a function
	chosen = input("Choose a function (for full functionality please type the entire function): " )
	chosen = [s for s in functionlist if chosen in s]
	chosen = chosen[0]

	#parses chosen function to output a file output.txt with necessary info
	final = []
	split = re.split("[,()]+", chosen)
	for part in split:
		if re.match(r'\s', part):
			part = part[1:]

		final.append(part)

	name = final[0].split()

	newfile = open("cache/function_info.txt", "w")

	if (len(name) == 2):
		line1 = "FunctionName:" + name[1] + "\n"
	else:
		line1 = "FunctionName:" + name[0] + "\n"
	newfile.write(line1)

	line2 = "Input:"
	bool = False
	final2 = final[1:]
	final2 = final[:-1]
	for part in final2:
		if (bool):
			line2 = line2 + part + ","
		bool = True
	line2 = line2[:-1]
	line2 += "\n"
	newfile.write(line2)

	#line3 = "ReturnType:" + name[0] + "\n"
	#newfile.write(line3)

	#grab the includes
	line4 = "Include:"
	for line in file:
		if "#include" in line:
			line = line.replace("\n", "").replace('\r',"")
			line4 = line4 + line + ","
	line4 = line4[:-1]
	line4 = line4.rstrip('\r\n')
	newfile.write(line4+"\n")

	line5 = "Source:" + filename
	newfile.write(line5+"\n")

	line6 = "Compiled Lib:" + compiledlib
	newfile.write(line6+"\n")

	line7 = "Include Folder" + includefold
	newfile.write(line7+"\n")

	file.close()
	newfile.close()


if __name__ == "__main__":
	# filename = sys.argv[1]
	main(sys.argv[1],sys.argv[2],sys.argv[3])
