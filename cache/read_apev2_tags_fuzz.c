/*
 * Generate by Deepfuzzer
 * Target Function: read_apev2_tags
 * Time: 2019-04-02 17:04:39.337215
 */

#include "apev2.h"
#include "wavutils.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <inttypes.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    FILE *infile = fopen(argv[1], "rb");
    fseek(infile, 0, SEEK_END);
    int fileSize = (int)ftell(infile);
    rewind(infile);
    read_apev2_tags(state, data, data_size, keys, header, list);
    return 0;
}
