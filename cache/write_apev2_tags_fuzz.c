/*
 * Generate by Deepfuzzer
 * Target Function: write_apev2_tags
 * Time: 2019-04-01 14:15:44.189310
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
  int minSize = sizeof(int) + sizeof(double) + sizeof(const int16_t) +
                sizeof(int32_t) + sizeof(char);
  if (minSize > fileSize) {
    fclose(infile);
    return 0;
  }
  int *df_buffer_a = (int *)malloc(sizeof(int));
  fread(df_buffera, sizeof(int), 1, infile);
  int a = *df_buffer_a;
  double *df_buffer_b = (double *)malloc(sizeof(double));
  fread(df_bufferb, sizeof(double), 1, infile);
  double b = *df_buffer_b;
  const int16_t *df_buffer_d = (const int16_t *)malloc(sizeof(const int16_t));
  fread(df_bufferd, sizeof(const int16_t), 1, infile);
  const int16_t d = *df_buffer_d;
  int32_t *df_buffer_f = (int32_t *)malloc(sizeof(int32_t));
  fread(df_bufferf, sizeof(int32_t), 1, infile);
  int32_t f = *df_buffer_f;
  write_apev2_tags(a, b, d, f, arss);
  return 0;
}
