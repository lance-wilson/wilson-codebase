#include <stdio.h>

/* CS-130
Lance Wilson
Assignment 7
Due March 3, 2015
Purpose:  To calculate the Julian Day using a function.
*/

int J_dayf();

int main(){

	int month, year, day, j_day;
	
	printf("Enter the first date in year month day format.\n");
	scanf("%d %d %d", &year, &month, &day);

	if(month == 1 || month == 3 || month == 5 || month == 7 || month == 8 || month == 10 || month == 12){
		if(day > 31){
			printf("Not a valid date.\n");
		}
		else{
			j_day = J_dayf(year, month, day);
		}
	}
	if(month == 4 || month == 6 || month == 9 || month == 11){
		if(day>30){
			printf("Not a valid date.\n");
		}
		else{
			j_day = J_dayf(year, month, day);
		}
}
	if(month == 2){
		if(year % 4 != 0){
			if(day>28){
				printf("Not a valid date.\n");}
	}
	else{
			j_day = J_dayf(year, month, day);
		}
}
	if(month == 2){
		if(year % 4 = 0 && year % 100 != 0){
			if(day>29){
				printf("Not a valid date.\n");}
		}
		else{
			j_day = J_dayf(year, month, day);
		}
		
}

	printf("The Julian Day for %d/%d/%d is %d.\n", year, month, day, j_day);

	return 0;
}

int J_dayf(year, month, day){

	int j_day, a, y, m;

	a=(14-month)/12;
	y=year+4800-a;
	m=month+12*a-3;

	j_day = day + (153*m+2)/5 + (365*y) + (y/4) - (y/100) + (y/400) - 32045;

	return j_day;
}
