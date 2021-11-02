#!/usr/bin/perl
# If I ever attempt to make a 2d Array in perl ever again, this is valuable instructions.

use List::Util qw( min max );

# Creates an array of anonymous references to two arrays of zeroes of size 5.
@residual = ([(0.0) x 5], [(0.0) x 5]);
# Calculates the length of the array (2).
my $length = scalar @residual;

# Calculates the length of the first array in @residual (5). Note that the index is dereferenced.
my $length1 = scalar @{$residual[0]};

# Get the first element in the first row/array (array[0][0])
$first_element_first_row = ${$residual[0]}[0];

print "$length\n";
print "$length1\n";
print "$first_element_first_row\n";

# Assign some values.
${$residual[0]}[0] = 15.0;
${$residual[0]}[1] = 22.0;

$first_element_first_row2 = ${$residual[0]}[0];
print "$first_element_first_row2\n";

# Find the max of the first row.
$max = max @{$residual[0]};

print "$max\n";

# But apparently this works for some reason...
print "$residual[0][0]\n";

# But this doesn't work, so I guess you have to derefence it if you want the whole row, and can use the above if you just want one element.
$max2 = max @residual[0];
print "$max2\n";

# One more test, of a 5 x 10 array.
@fiveByFive = ([(0.0) x 10]) x 5;
$length5 = scalar @fiveByFive;
print "$length5\n";
$length5_0 = scalar @{$fiveByFive[0]};
print "$length5_0\n";

$fiveByFive[3][8] = 6.0;
print "$fiveByFive[3][8]\n";
$max3 = max @{$fiveByFive[3]};
print "$max3\n";
