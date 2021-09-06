#include <stdio.h>

/*
CS 130
Lance Wilson
Assignment 4
Due February 17, 2015
Purpose:  Find the sum of 20 consecutive integers following the value entered by the user.
*/

int main()
{

	int n, sum, number;

	printf("Enter an integer value: ");
	scanf("%d", &n);

	sum = 0;
	number = n;

	while(number<=(n+20)){
		sum = sum + number;
		number++;
}

	printf("Sum of numbers from %d to %d:  %d\n", n, (n+20), sum);


	return 0;

}
