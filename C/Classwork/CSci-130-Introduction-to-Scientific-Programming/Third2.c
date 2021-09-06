#include <stdio.h>

int main()
{
	FILE* in_fp;
	int first = 0;
	float second = 0.00;

	in_fp = fopen("datafile.dat", "r");
	
	while(fscanf(in_fp, "%d %f", &first, &second) !=EOF){

		printf("First Value: %4d  and Second Value: %8.2f\n", first, second);
	}









	return 0;
}
