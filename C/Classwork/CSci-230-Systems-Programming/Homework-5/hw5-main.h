#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "hw5-scan.h"
#include "hw5-load.h"
#include "hw5-search.h"
#include "hw5-free.h"

#ifndef _linker_
#define _linker_
struct _data {                                 
   char *name;
   long number;
};
#endif

int main(int argv, char **argc);
