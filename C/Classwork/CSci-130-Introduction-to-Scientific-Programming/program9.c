#include <stdio.h>

/* CS-130
Lance Wilson
Assignment 9
Due March 24, 2015
Purpose:  To set up 3 arrays with 5 numbers each; the first two with values entered by the user, and the third with elements as a sum of the corresponding element in the first two arrays.
*/

void myarraycomp();
int cr[5];

int main(){

	int j, l, m, n;
	int ar[5];
	int br[5];

	printf("Input the five values of the first array.\n");
	scanf("%d %d %d %d %d", &ar[0], &ar[1], &ar[2], &ar[3], &ar[4]);

	printf("Input the five values of the second array.\n");
	scanf("%d %d %d %d %d", &br[0], &br[1], &br[2], &br[3], &br[4]);

	j = 5;	
	myarraycomp(ar, br, j);
		
	printf("First Array:  ");	
	for(l=0; l<5; l++){
		printf("%d ", ar[l]);
	}
	printf("\n");

	printf("Second Array:  ");
	for(m=0; m<5; m++){
		printf("%d ", br[m]);
	}
	printf("\n");

	printf("Third Array:  ");
	for(n=0; n<5; n++){
		printf("%d ", cr[n]);
	}
	printf("\n");


	return 0;

}

void myarraycomp(int a[], int b[], int n){
	int k;

	for(k=0; k<n; k++){
		cr[k] = a[k] + b[k];
	}
	
}



