/*
 * Lance Wilson
 *
 * Purpose: to calculated the interest made over the lifetime of an arbitrary loan.
 *
 * Input: the monthly payment for the loan.
 *
 * Output: printout of each month's balance and the total interest paid.
 *
 * Compile: gcc -o hw1-LanceWilson hw1-LanceWilson.c
 *
 */
#include <stdio.h>

int main()
{
    const float interest_rate = 0.25;
    float balance = 2000.00;
    float payment;
    float previous_interest, current_interest;
    float total_interest = 0;
    int month = 1;

    previous_interest = (interest_rate/12) * balance;

    printf("Enter your monthly payment: ");
    scanf("%f", &payment);

    printf("Interest rate: %.2f\n", interest_rate);
    printf("Initial Balance: %.2f\n", balance);
    printf("Monthly: %.2f\n\n", payment);

    while (balance > 0)
    {
        printf("%d %.2f %.2f\n", month, previous_interest, balance);

        month++;
        current_interest = (interest_rate/12)*(balance-payment+previous_interest);
        balance = balance - payment + previous_interest;
        total_interest += previous_interest;
        previous_interest = current_interest;
    }

    printf("%d %.2f %.2f\n\n", month, previous_interest, balance);

    printf("Total Interest Paid: %.2f\n", total_interest);   
}
