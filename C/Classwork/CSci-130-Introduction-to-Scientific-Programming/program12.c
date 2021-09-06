#include <stdio.h>

/* CS-130
Lance Wilson
Assignment 12
Due April 14, 2015
Purpose:  To take five names in the format "firstname lastname" entered by the user and output them in the form "lastname, firstname".
*/

int main(){

	char firstnames[6][30], lastnames[6][30];
	int i;

	printf("Please enter five names in the format \"First Last\".\n");
	for(i=0; i<5; i++){
		scanf("%s %s", &firstnames[i], &lastnames[i]);
	}

	printf("\n\nThe names are:\n");
	for(i=0; i<5; i++){
		printf("%s, %s\n", lastnames[i], firstnames[i]);
	}


	return 0;

}
