/*
 * Generate by Deepfuzzer
 * Target Function: check_if_constant
 * Time: 2019-04-11 16:20:24.620503
 */

#include <limits.h>
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include "lpc.h"

#include <inttypes.h>
#include <stdlib.h>

int pointer_size_data = 1;
uint16_t d1_data;
fread(&d1_data, sizeof(uint16_t), 1, infile);

num_elements int32_t;
fread(&int32_t, sizeof(num_elements), 1, infile);
int main(int argc, char** argv) {
    FILE* infile = fopen(argv[1], "rb");

    fseek(infile, 0, SEEK_END);
    int fileSize = (int)ftell(infile);
    rewind(infile);

    check_if_constant(data, num_elements);
    return 0;
}
