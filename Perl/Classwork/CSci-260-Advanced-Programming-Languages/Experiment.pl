# Prints the path libraries for perl (located in $INC).

for ($x = 0; $x < scalar @INC; $x++)
{
    print "$INC[$x]\n";
}
