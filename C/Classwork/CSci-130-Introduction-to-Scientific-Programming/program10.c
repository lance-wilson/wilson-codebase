#include <stdio.h>

/* CS-130
Lance Wilson
Assignment 10
Due March 31, 2015
Purpose:  To store 10 user inputed numbers in array, and then conduct a linear search on the array for another user inputed value.
*/

int searchf();

int main(){

	int a[10];
	int i, n, position;



	printf("Please enter 10 numbers.\n");
	for(i=0; i<10; i++)
		scanf("%d", &a[i]);

	printf("Please enter a number to search for.\n");
	scanf("%d", &n);

	position = searchf(a, 10, n);

	if(position >= 0){
		printf("The number %d was found at position %d.\n", n, position);
	}
	else{
		printf("The number %d was not found in the array.\n", n);
	}


	return 0;
}

int searchf(int a[], int m, int n){
	int k, location = -1;
	for(k=0; k<m; k++){
		if(a[k] == a[k+1]){
			printf("The number %d was found at multiple positions.\n", n);	
		}	
	}
	for(k=0; k<m; k++){
		if(a[k] == n){
			location = k;
			k=m;
		}
	}

	return location;
}
