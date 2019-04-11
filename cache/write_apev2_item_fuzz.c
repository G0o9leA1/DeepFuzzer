/*
 * Generate by Deepfuzzer
 * Target Function: write_apev2_item
 * Time: 2019-04-11 16:16:56.081354
 */

#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "apev2.h"
#include "wavutils.h"

#include <inttypes.h>
#include <stdlib.h>

int main(int argc, char** argv) {
    FILE* infile = fopen(argv[1], "rb");

    fseek(infile, 0, SEEK_END);
    int fileSize = (int)ftell(infile);
    rewind(infile);

    write_apev2_item(key_inst, tag_item, data, data_size, item_code);
    return 0;
}
