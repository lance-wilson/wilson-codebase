#include <stdio.h>
#include <string.h>

/* CS-130
Lance Wilson
Assignment 15
Due May 5, 2015
Purpose:  Take in a number of strings (inputed by the user), store them in dynamically allocated memory, point to them with an array of character pointers, and print them in reverse order.
*/

int main(){

	int g, i;
	char string[512];

	printf("Input the number of strings (max 20):  ");
	scanf("%d", &g);
	if(g>20){
		g=20;
		printf("Number of strings exceeds the maximum and has been reset to 20.\n");
	}
	char *strptr[g];

	printf("Please input the strings:\n");
	for(i=0; i<=g; i++){
		fgets(string, sizeof(string), stdin);
		string[strlen(string)-1] = '\0';
		strptr[i] = malloc(strlen(string)+1);
		strcpy(strptr[i], string);
	}

	printf("\nThe strings, last to first:\n");
	for(i=g; i>=0; i--){
		puts(strptr[i]);
	}


	return 0;
}
