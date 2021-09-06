#include <stdio.h>
#include <math.h>

int main(){

	float a,b;
	printf("Enter two numbers:");
	scanf("%f, %f", &a, &b);

	if((fabs(a-b))<0.01){
		printf("Yay!\n");}
	else{
		printf("Oh no!\n");}

	return 0;
}
