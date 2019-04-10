/*
 * Generate by Deepfuzzer
 * Target Function: write_apev2_tags
 * Time: 2019-04-09 18:01:10.286210
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
    int f_1d = sizeof(int32_t) + sizeof(int) + sizeof(double) +
               sizeof(const int16_t) + sizeof(uint16_t);
    if (minSize > fileSize) {
        fclose(infile);
        return 0;
    }
    int *df_buffer_a = (int *)malloc(sizeof(int) * 1);
    fread(df_buffer_a, sizeof(int), 1, infile);
    int a = *df_buffer_a;
    free(df_buffer_a);

    double *df_buffer_b = (double *)malloc(sizeof(double) * 1);
    fread(df_buffer_b, sizeof(double), 1, infile);
    double b = *df_buffer_b;
    free(df_buffer_b);

    int16_t *df_buffer_d = (int16_t *)malloc(sizeof(int16_t) * 1);
    fread(df_buffer_d, sizeof(int16_t), 1, infile);
    const int16_t d = *df_buffer_d;
    free(df_buffer_d);

    uint16_t *df_buffer_xs = (uint16_t *)malloc(sizeof(uint16_t) * 1);
    fread(df_buffer_xs, sizeof(uint16_t), 1, infile);
    uint16_t xs = *df_buffer_xs;
    free(df_buffer_xs);

    write_apev2_tags(a, b, d, f, xs);
    return 0;
}
