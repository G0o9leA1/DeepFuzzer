# DeepFuzzer: 
## To-do list
 - Generate function infos contained in the libs
 - generate the fuzzable executable file
 - Deal with the unconventional target
 
## Dependences:
    sudo apt install ctags
    sudo apt install clang-format

## Test:
    python3 interfaceGen.py
 
 For function in the test/function_info.txt  
 Generated file is in the cache/<function_name>_fuzz.c
    
## Usage
    python3 main.py <filename>
 
