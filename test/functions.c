static void Float32_To_Int16_Clip(
    void *destinationBuffer, signed int destinationStride,
    void *sourceBuffer, signed int sourceStride,
    unsigned int count, struct PaUtilTriangularDitherGenerator *ditherGenerator )
{
    float *src = (float*)sourceBuffer;
    PaInt16 *dest =  (PaInt16*)destinationBuffer;
    (void)ditherGenerator; /* unused parameter */

    while( count-- )
    {
#ifdef PA_USE_C99_LRINTF
        long samp = lrintf((*src * (32767.0f)) -0.5f);
#else
        long samp = (PaInt32) (*src * (32767.0f));
#endif
        PA_CLIP_( samp, -0x8000, 0x7FFF );
        *dest = (PaInt16) samp;

        src += sourceStride;
        dest += destinationStride;
    }
}

/* -------------------------------------------------------------------------- */

static void Float32_To_Int16_DitherClip(
    void *destinationBuffer, signed int destinationStride,
    void *sourceBuffer, signed int sourceStride,
    unsigned int count, struct PaUtilTriangularDitherGenerator *ditherGenerator )
{
    float *src = (float*)sourceBuffer;
    PaInt16 *dest =  (PaInt16*)destinationBuffer;
    (void)ditherGenerator; /* unused parameter */

    while( count-- )
    {

        float dither  = PaUtil_GenerateFloatTriangularDither( ditherGenerator );
        /* use smaller scaler to prevent overflow when we add the dither */
        float dithered = (*src * (32766.0f)) + dither;
        PaInt32 samp = (PaInt32) dithered;
        PA_CLIP_( samp, -0x8000, 0x7FFF );
#ifdef PA_USE_C99_LRINTF
        *dest = lrintf(samp-0.5f);
#else
        *dest = (PaInt16) samp;
#endif

        src += sourceStride;
        dest += destinationStride;
    }
}