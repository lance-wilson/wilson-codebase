#include <stdio.h>
#include <stdlib.h>

#ifndef _linker_
#define _linker_
struct _data {                                 
   char *name;
   long number;
};
#endif

void FREE(struct _data *BlackBox, int size);
