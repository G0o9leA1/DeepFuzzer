# Example with SELA
This is a detailed example with SELA, an audio library.     
We are assuming user have a clean Ubuntu 16.04    
If you are sure you have already downloaded all library we need, go to Download DeepFuzzer step 
## Update and Upgrade apt Source
    sudo apt-get update
    sudo apt-get upgrade

## Install Required Library
    sudo apt-get install build-essential git
    sudo apt-get install clang
    sudo apt-get install clang-check
    sudo apt-get install cproto

## Install AFL
    wget http://lcamtuf.coredump.cx/afl/releases/afl-latest.tgz
    tar xvf afl-latest.tgz a
    rm afl-latest.tgz 
    cd afl-2.52b/ && make
    sudo make install
    cd ..

## Download DeepFuzzer
    git clone https://github.com/z1Tion/DeepFuzzer.git

## Check Prerequisite
    cd DeepFuzzer
    sh test.sh
    cd ..

## Download Target SELA from GitHub
    git clone https://github.com/sahaRatul/sela.git

## Compile and Instrument SELA with afl-gcc
    cd sela
    export CC=afl-gcc
    make all -e
    export CC=gcc

## Pack .o file into a static library
    ar rc libsela.a
    cd ..

## Add necessary link flag into compile_flag.txt
    cd DeepFuzzer
    vim Utilities/compile_flag.txt
    cd ..
    
## Run DeepFuzzer
    cd DeepFuzzer
    python3 main.py ../sela/core/apev2.c ../sela/include/ ../sela/libsela.a

## Lets Fuzz!
    cd out/bin
    mkdir input output
    echo 'fuzz' > input/input.txt
    afl-fuzz -i input -o output ./init_apev2_fuzz @@