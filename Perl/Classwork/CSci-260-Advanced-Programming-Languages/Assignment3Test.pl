#!/usr/bin/perl
# Lance Wilson
# Program Assignment 3
#
# Summary: Tests the capabilites of the ListUtil module.

use strict;

use ListUtil;

# Set the name.
name ("The name of the list");
my $current_name = name;
print "Current name is:  $current_name\n";

# Add some items (2 and Item 3 are duplicates).
if (addItem ("Item 1"))
{
    print "Adding Success!\n";
}
else
{
    print "Adding failed\n";
}

if (addItem ("2"))
{
    print "Adding Success!\n";
}
else
{
    print "Adding failed\n";

}

if (addItem (2))
{
    print "Adding Success!\n";
}
else
{
    print "Adding failed\n";

}

if (addItem ("Item 2"))
{
    print "Adding Success!\n";
}
else
{
    print "Adding failed\n";
}

if (addItem ("Blue"))
{
    print "Adding Success!\n";
}
else
{
    print "Adding failed\n";
}

if (addItem ("Item 3"))
{
    print "Adding Success!\n";
}
else
{
    print "Adding failed\n";
}

if (addItem ("Item 3"))
{
    print "Adding Success!\n";
}
else
{
    print "Adding failed\n";
}

if (addItem ("item 3"))
{
    print "Adding Success!\n";
}
else
{
    print "Adding failed\n";
}

print "\n";

# Check that Item 1 is found.
if (isInList ("Item 1"))
{
    print "Item 1 is there\n";
}
else
{
    print "It's NOT there\n";
}

print "\n";

# Show the number of items in the list.
my $numItems = count;
print "Number of items: $numItems\n\n";

# List all of the items when returned as an array.
my @listArray = list (-type=>"array");
print "List from Array:\n";
foreach my $item (@listArray)
{
    print "$item\n";
}

print "\n";

# List all items when returned as a reference.
my $arrayRef = list;
print "List from reference:\n";
foreach my $item (@$arrayRef)
{
    print "$item\n";
}

print "\n";

# Save data to a file.
saveToFile ("List.txt");

# Remove an item.
if (removeItem ("Item 1"))
{
    print "Removal Success!\n";
}
else
{
    print "Removal failed\n";
}

# Remove an item.
if (removeItem ("Item 9"))
{
    print "Removal Success!\n";
}
else
{
    print "Removal failed\n";
}

# Check that the Item 1 is gone but that Item 9 did not crash anything.
my $arrayRef = list;
print "List from reference after removal:\n";
foreach my $item (@$arrayRef)
{
    print "$item\n";
}

print "\n";

# Load data from a file.
loadFromFile ("ExistingList.txt");
# Print the loaded list's name.
my $new_name = name;
print "New name is: $new_name\n";

# Print the data from the loaded list.
my $arrayRef = list;
print "@$arrayRef\n";

