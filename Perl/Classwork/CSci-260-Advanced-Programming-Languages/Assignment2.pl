#!/usr/bin/perl
# Lance Wilson
# Program Assignment 2
#
# Summary: Takes in the name of a student, and class information for a number of classes. Class information will include the course name, number of credits, and letter grade. When the class name is an empty string, the program will then calculate the student's GPA, and print out the student's name, number of credits taken and passed, and the GPA. 

use strict;

# Collect the students name.
print "Please enter the student's name:  ";
my $studentname = <STDIN>;
chomp $studentname;

# Initialize variables needed outside the while loop.
my $classname = "DEFAULT";
my $totalcredits = 0;
my $passed = 0;
my $gpapoints = 0;

# Run while the class name is not empty string.
while ($classname ne "")
{
    # Collect the class name.
    print "Enter a class: ";
    $classname = <STDIN>;
    chomp $classname;

    if ($classname ne "")
    {
        # Collect the number of course credits.
        print "Enter the number of course credits: ";
        my $thiscredits = <STDIN>;
        chomp $thiscredits;
        $totalcredits += $thiscredits;

        # Collect the letter grade.
        print "Enter the letter grade received: ";
        my $grade = <STDIN>;
        chomp $grade;

        # Check for passing credits.
        if ($grade ne "F" and $grade ne "f")
        {
            $passed += $thiscredits;
        }

        # Calculate the number of GPA points.
        if ($grade eq "A" or $grade eq "a")
        {
            $gpapoints += (4.0 * $thiscredits);
        }
        elsif ($grade eq "B" or $grade eq "b")
        {
            $gpapoints += (3.0 * $thiscredits);
        }
        elsif ($grade eq "C" or $grade eq "c")
        {
            $gpapoints += (2.0 * $thiscredits);
        }
        elsif ($grade eq "D" or $grade eq "d")
        {
            $gpapoints += (1.0 * $thiscredits);
        }
    }
    print "\n";
}

# Calculate the GPA.
my $gpa = 0.00;
if ($gpapoints != 0)
{
    $gpa = $gpapoints/$totalcredits;
}

# Print the results.
printf ("Transcript for $studentname\n");
printf ("%-16s %-5d\n", "Credits taken: ", $totalcredits);
printf ("%-16s %-5d\n", "Credits passed: ", $passed);
printf ("%-16s %-5.2f\n", "Semester GPA: ", $gpa);
