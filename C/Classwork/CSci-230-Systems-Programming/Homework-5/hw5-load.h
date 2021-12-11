#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifndef _linker_
#define _linker_
struct _data {                                 
   char *name;
   long number;
};
#endif

struct _data *LOAD(FILE *stream, int size);
