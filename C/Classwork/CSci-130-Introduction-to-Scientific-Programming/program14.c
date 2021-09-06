#include <stdio.h>
#include <string.h>

/* CS-130
Lance Wilson
Assignment 14
Due April 28, 2015
Purpose:  To input a string into a character pointer, print the string, tell how long the string is, and print the string in reverse order.
*/

int main(){

	char string[512];	
	char *strptr;
	int i;	

	printf("Please input a string.\n");
	fgets(string, sizeof(string), stdin);
	string[strlen(string)-1] = '\0';
	strptr = malloc(strlen(string) + 1);
	strcpy(strptr, string);

	printf("\nYou input: \"%s\"\n", strptr);	

	printf("which is %d characters long.\n", strlen(string));

	printf("\nReversed the string reads:\n");
	
	strptr = strptr + strlen(string);
	for(i=0; i<=strlen(string); i++){
		printf("%c", *strptr);
		strptr--;
	}
	printf("\n");

	
	return 0;
}
