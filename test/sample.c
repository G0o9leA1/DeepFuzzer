/*
* Generate by Deepfuzzer
* Target binary: lpc.o
* Target function: int32_t check_if_constant(const int16_t *data,int32_t num_elements)
* Time: Sat Mar 30 17:11:21 CDT 2019
*/

/* Steal From source Code */
#include <stdio.h>
#include <stdint.h>
#include <limits.h>
#include <math.h>
#include "lpc.h"

/* Generate by deepfuzzer*/
#include <inttypes.h>
#include <stdlib.h>

#define DEBUG_PRINT 1

int main(int argc, char **argv)
{
    FILE *infile = fopen(argv[1],"rb");
    fseek(infile,0,SEEK_END);

    #ifdef DEBUG_PRINT
        printf("FILE offset:%d\n", (int)ftell(infile));
    #endif

    if((int)ftell(infile)!=sizeof(int16_t)+sizeof(int32_t))
    {
	fclose(infile);
        return 0;
    }
    
    rewind(infile);
    int16_t *buffer=(int16_t*)malloc(sizeof(int16_t));
    fread(buffer,sizeof(int16_t),1,infile);

    #ifdef DEBUG_PRINT
        printf("FILE offset:%d\n", (int)ftell(infile));
    #endif
    int16_t a=*buffer;
    free(buffer);

    int32_t *buffer1=(int32_t*)malloc(sizeof(int32_t));
    fread(buffer1,sizeof(int32_t),1,infile);

    #ifdef DEBUG_PRINT
            printf("FILE offset:%d\n", (int)ftell(infile));
    #endif

    int32_t b=*buffer1;
    free(buffer1);
    fclose(infile);
   
    const int16_t *data=&a;

    #ifdef DEBUG_PRINT
        printf("%"PRId16"\n",a);
        printf("%"PRId32"\n",b);
    #endif

    /* Fuzzing Target*/
    check_if_constant(data,b);

    return 0;
}
