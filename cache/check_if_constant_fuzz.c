/*
 * Generate by Deepfuzzer
 * Target Function: check_if_constant
 * Time: 2019-04-11 17:08:42.483888
 */

#include <limits.h>
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include "lpc.h"

#include <inttypes.h>
#include <stdlib.h>

int main(int argc, char** argv) {
    FILE* infile = fopen(argv[1], "rb");

    fseek(infile, 0, SEEK_END);
    int fileSize = (int)ftell(infile);
    int minSize = 0;
    rewind(infile);

    int pointer_size_data = 1;
    if (fileSize < minSize + sizeof(uint16_t) * pointer_size_data) {
        fclose(infile);
        return 0;
    }

    uint16_t d1_data;
    fread(&d1_data, sizeof(uint16_t), 1, infile);

    if (fileSize < minSize + sizeof(uint16_t) * pointer_size_data +
                       sizeof(const int16_t) * d1_data) {
        fclose(infile);
        return 0;
    }
    int16_t reference_data[d1_data];
    for (long int i = 0; i < d1_data; ++i) {
        int16_t tmp_data;
        fread(&tmp_data, sizeof(const int16_t), 1, infile);
        reference_data[i] = tmp_data;
    }
    const int16_t* data = reference_data;

    if (fileSize < minSize + sizeof(uint16_t) * pointer_size_data +
                       sizeof(const int16_t) * d1_data + sizeof(int32_t)) {
        fclose(infile);
        return 0;
    }
    int32_t num_elements;
    fread(&num_elements, sizeof(int32_t), 1, infile);
    check_if_constant(data, num_elements);
    return 0;
}
