#!/usr/bin/perl
# Lance Wilson
# Program Assignment 3
#
# Summary: Module that has subroutines to store a list with a name and data, along with file input and output capabilities.

package ListUtil;

use strict;
# Export the subroutines.
use Exporter;
our @ISA = qw ( Exporter );
our @EXPORT = qw (&name &addItem &removeItem &isInList &saveToFile &loadFromFile &count &list);

my ($nameOfList, $filename, @data, $item, $false, $true, $index);
$false = 0;
$true = 1;
$index = 0;

# Set the name or return it if there are no arguments.
sub name
{
    if ((scalar @_) == 1)
    {
        $nameOfList = shift;
    }
    else
    {
        return $nameOfList;
    }
}

# Add an item to the list.
sub addItem
{
    my $input = shift;
    my $returnVal = $true;

    # Check for duplicates.
    foreach $item (@data)
    {
        if ($item eq $input && $item == $input)
        {
            $returnVal = $false;
        }
    }

    # Add if the item is unique.
    if ($returnVal)
    {
        @data[$index] = $input;
        $index++;
    }

    return $returnVal;
}

# Remove an item from the list if it exists.
sub removeItem
{
    my $goneItem = shift;
    my $returnVal = $false;

    my $thisIndex;
    for ($thisIndex = 0; $thisIndex < scalar (@data); $thisIndex++)
    {
        if ($data[$thisIndex] eq $goneItem && $data[$thisIndex] == $goneItem)
        {
            splice (@data, $thisIndex, 1);
            $returnVal = $true;
        }
    }

    return $returnVal;
}

# Check if the item is in the list.
sub isInList
{
    my $searchItem = shift;
    my $returnVal = $false;

    foreach $item (@data)
    {
        if ($item eq $searchItem && $item == $searchItem)
        {
            $returnVal = $true;
        }
    }

    return $returnVal;
}

sub saveToFile
{
    $filename = shift;
    # Default file name if none was provided.
    if ($filename eq "")
    {
        $filename = "saveFile.txt";
    }

    open (OUTFILE, ">$filename") or die ("\n");

    print OUTFILE "$nameOfList\n";

    foreach $item (@data)
    {
        print OUTFILE "$item\n";
    }

    close(OUTFILE);
}

sub loadFromFile
{
    $index = 0;

    $filename = shift;
    # Default file name if none provided.
    if ($filename eq "")
    {
        $filename = "saveFile.txt";
    }

    open (INFILE, "$filename") or die ("\n");

    # First line will be the name of the list.
    my $line = <INFILE>;
    name ($line);

    # Remaining lines are data.
    while ($line = <INFILE>)
    {
        addItem ($line);
    }

    close (INFILE);
}

# Number of items in the list.
sub count
{
    return scalar @data;
}

sub list
{
   my %params = (
                   type => '',
                );

    # nextArg checks for -type argument.
    my $nextArg = shift @_;
    # Next argument after that is the type.
    my $nextnextArg = shift;

    $params{type} = $nextArg;
    if ($nextArg eq "-type")
    {
        $params{type} = $nextnextArg;
    }

    if ($params{type} eq "array")
    {
        return @data;
    }
    else
    {
        return \@data
    }
}

1;
