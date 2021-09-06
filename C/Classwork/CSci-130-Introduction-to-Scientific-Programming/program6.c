#include <stdio.h>

/* CS-130
Lance Wilson
Assignment 6
Due February 24, 2015
Purpose:  To take numbers from a data file, find their average, and print the results to a new file.
*/

int main(){

	float a, b, c, d, e, f;

	FILE *in6ptr;
	FILE *out6ptr;
	in6ptr = fopen("input_5.dat", "r");
	out6ptr = fopen("output_6.txt", "w");

	if(!in6ptr){
		printf("File \"input_5.dat\" could not be opened.");
	}

	if(in6ptr){	
		fscanf(in6ptr, "%f%f%f%f%f", &a, &b, &c, &d, &e);
		fclose(in6ptr);
	}

	f = (a + b + c + d + e)/5;

	fprintf(out6ptr, "Numbers:  %.3f %.2f %.1f %.2f %.1f. Average:  %.3f\n", a, b, c, d, e, f);

	fclose(out6ptr);

	return 0;
}
