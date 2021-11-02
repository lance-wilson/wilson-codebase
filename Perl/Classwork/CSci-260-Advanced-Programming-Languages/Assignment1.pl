#!/usr/bin/perl
# Lance Wilson
# Program Assignment 1
#
# Part 1: Takes in a name in the format "first last" and prints out each name separately, in "last, first" format, in all capital letters, and with one name on each line.
# Part 2: Takes in a three digit number, prints out the digit in each place, and prints the original number.

use strict;
my ($name, $first_name, $last_name, $upper_name, $number, $hundreds, $tens, $ones);

# Part 1
print "*******Part 1*******\n";
print "Please enter a name in \"first last\" format.\n";
$name = <STDIN>;
# First name is the substring up until a space is found.
$first_name = substr($name, 0, index($name, ' '));
print "The first name is $first_name.\n";
# Last name is everything after the space.
$last_name = substr($name, index($name, ' ') + 1, -1);
print "The last name is $last_name.\n";
print "The name in \"last, first\" format is $last_name, $first_name.\n";
# Removes the newline character from the end of the name.
chomp $name;
# Converts the name to all caps.
$upper_name = uc $name;
print "The name in all capital letters is $upper_name.\n";
print "$first_name \n$last_name\n";

# Part 2
print "\n\n\n*******Part 2*******\n";
print "Please enter a three digit number.\n";
$number = <STDIN>;
# Set ones equal to the original number.
$ones = $number;
# Initialize tens and hundreds to 0.
$tens = 0;
$hundreds = 0;

my $hundred_string = "Hundreds digit: ";
my $tens_string = "Tens digit: ";
my $ones_string = "Ones digit: ";
my $number_string = "Original number: ";

# Subtract 100 from ones while it is still greater than 100.  Each iteration equates to one greater digit in the hundreds place.
while ($ones >= 100)
{
    $ones -= 100;
    $hundreds += 1;
}

printf("%20s %5d\n", $hundred_string, $hundreds);

# Subtract 10 from ones while it is still greater than 10.  Each iteration equates to one greater digit in the tens place.
while ($ones >= 10)
{
    $ones -= 10;
    $tens += 1;
}

printf("%20s %5d\n", $tens_string, $tens);

# Whatever is left is the ones digit.
printf("%20s %5d\n", $ones_string, $ones);

printf("%20s %5d\n", $number_string, $number);
