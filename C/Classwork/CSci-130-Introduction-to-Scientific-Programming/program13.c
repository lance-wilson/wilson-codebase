#include <stdio.h>
#include <string.h>

/* CS-130
Lance Wilson
Assignment 13
Due April 21, 2015
Purpose:  To input 10 words using strings and then search for a user defined word and, if found, print out its location.
*/

int stringsearchf(char [20], char [20], int);


int main(){

	char words[11][20];
	char search[20];
	int i, found;

	printf("Please enter 10 words:\n");
	for(i=0; i<10; i++){	
		fgets(words[i], sizeof(words[i]), stdin);	
	}

	
	printf("\nPlease enter a word to search for:\n");

	fgets(search, sizeof(search), stdin);

	search[strlen(search)-1] = '\0';

	for(i=0; i<10; i++){
		words[i][strlen(words[i])-1] = '\0';
	}

	int notfound = 1;
	
	for(i=0; i<10; i++){
		found = stringsearchf(words[i], search, i);
			
		if(found == 0){
			i=10;
			notfound = 0;
		}
		
	}

	if(notfound != 0){
		printf("\nThe word %s was not found in the array.\n", search);
	}	

	return 0;
}


int stringsearchf(char words[20], char search[20], int i){
	int f;
	f = strcmp(words, search);

	if(f == 0){
		printf("\nThe word %s was found in array element number %d.\n", search, i);
	}
	

	return f;

}


