#include <stdio.h>

/*Output file is named wilsonoutput.dat.*/

/* CS-130
Lance Wilson
Assignment 11
Due April 7, 2015
Purpose:  To read floating point numbers from data files into two 5x5 arrays, perform matrix addition on the two arrays, and output the resulting array to a data file.
*/

void matrixaddf(float [][5], float [][5], float [][5]);

int main(){
	float a[5][5];
	float b[5][5];
	float c[5][5];
	int i, j;
	FILE *fptr1, *fptr2, *fptr3;

	fptr1 = fopen("input1.dat", "r");
	if(fptr1 == NULL){
		printf("File did not open.\n");	
	}
	else{
		for(i=0; i<5; i++){
			for(j=0; j<5; j++){
				fscanf(fptr1, "%f", &a[i][j]);
			}
		}
	}
	fclose(fptr1);

	fptr2 = fopen("input2.dat", "r");
	if(fptr2 == NULL){
			printf("File did not open.\n");	
	}
		else{
			for(i=0; i<5; i++){
				for(j=0; j<5; j++){
					fscanf(fptr2, "%f", &b[i][j]);
				}
			}
		}
	fclose(fptr2);

	matrixaddf(a, b, c);

	fptr3 = fopen("wilsonoutput.dat", "w");
	if(fptr3 == NULL){
		printf("Output file did not open.\n");
	}
	else{
		for(i=0; i<5; i++){
			for(j=0; j<5; j++){
				fprintf(fptr3, "%4.1f ", c[i][j]);
			}
			fprintf(fptr3, "\n");
		}
	}	

	fclose(fptr3);


	return 0;
}



void matrixaddf(float a[5][5], float b[5][5], float c[5][5]){
	int i, j;
	for(i=0; i<5; i++){
		for(j=0; j<5; j++){
			c[i][j] = a[i][j] + b[i][j];
		}
	}

	return;
}
