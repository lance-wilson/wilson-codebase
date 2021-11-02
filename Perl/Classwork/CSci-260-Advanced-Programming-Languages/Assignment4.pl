#!/usr/bin/perl
# Lance Wilson
# Program Assignment 4
#
# Summary: Find and display information from various websites.

use strict;

use LWP::Simple;

my ($url1, $url2, $url3, $url4, $url5, $url6, $source1, $source2, $source3, $source4, $source5, $source6, $theRest, $searchArea, $innerArea, $thisProf, $input, $theStandings, $team, $header, $teamFound, $regEx);

# Web addresses.
$url1 = 'https://en.wikipedia.org/wiki/North_Dakota';
$url2 = 'https://www.privateinternetaccess.com/pages/whats-my-ip/';
$url3 = 'http://cs.und.edu/People/';
$url4 = 'https://twitter.com/myUND';
$url5 = 'http://money.cnn.com/data/markets/dow/';
$url6 = 'http://www.nfl.com/standings';

# Get source code.
$source1 = get $url1;
$source2 = get $url2;
#print $source2;
$source3 = get $url3;
$source4 = get $url4;
$source5 = get $url5;
$source6 = get $url6;

# North Dakota population.
if ($source1 =~ /Est. 2017<\/b><\/td>(.*)/s)
{
    $theRest = $1;
    if ($theRest =~ /(\d{3},\d{3})/)
    {
        print "The population of North Dakota is $1.\n";
    }
    else
    {
        print "Could not find North Dakota population.\n"
    }
}
else
{
    print "Could not find match in source1.\n";
}

print "\n\n";


# Check IP address.
if ($source2 =~ /Your IP Address:(.*)/s)
{
    $theRest = $1;
    #print "$theRest";
    if ($theRest =~ /(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/)
    {
        print "My IP Address is $1\n";
    }
    else
    {
        print "IP Address wasn't found\n";
    }
}
else
{
    print "IP Address didn't match\n";
}

print "\n\n";


# Print out CSci faculty and research interests.
if ($source3 =~ />Faculty<\/h3>(.*)/s)
{
    $theRest = $1;
    # Search area is the people between the Faculty header and the
    #   Adjunct Faculty header.
    if ($theRest =~ /(.*)>Adjunct Faculty<\/h3>/s)
    {
        $searchArea = $1;
    }
    else
    {
        print "Could not find Adjunct Faculty header.\n";
    }

    while ($searchArea =~ /<h3>(.*)<\/h3>.*\n(.*)/g)
    {
        print "$1\n";
        $thisProf = $2;

        if ($thisProf =~ /<ul>(.*)<\/ul>/)
        {
            $innerArea = $1;

            while ($innerArea =~ /<li >(.*?)<\/li>/g)
            {
                print "\t$1\n";
            }
        }
    }
}
else
{
    print "Could not find match in source3.\n";
}

print "\n\n";


# Print the number of tweets by @myUND.
if ($source4 =~ /"ProfileNav-label">Tweets<\/span>(.*)/s)
{
    $theRest = $1;
    if ($theRest =~ /(\d+,\d{3})/)
    {
        print "The number of Tweets by \@myUND is $1\n";
    }
    else
    {
        print "Could not find number of Tweets by \@myUND.\n";
    }
}
else
{
    print "Could not find match in source4.\n";
}

print "\n\n";


# Print the current DJIA and the numeric change.
if ($source5 =~ /Dow Jones Global Indexes:INDU(.*)/s)
{
    $theRest = $1;
    # Check the average.
    if ($theRest =~ /(\d+,\d{3}\.\d{2})/)
    {
        print "Today's Dow Jones Industrial Average is $1\n";
    }
    else
    {
        print "Could not find Dow Jones Industrial Average.\n";
    }
    # Check for today's change.
    if ($theRest =~ /(.*)Today&rsquo;s Change/)
    {
        $searchArea = $1;
        if ($searchArea =~ /([+|-]\d+\.\d{2})/)
        {
            print "Today's numeric change is $1\n";
        }
        else
        {
            print "Could not find today's numeric change.\n";
        }
    }
    else
    {
        print "Could not find match in theRest.\n";
    }
}
else
{
    print "Could not find match in source5.\n";
}

print "\n\n";


# Match user input to NFL team or city.
print "Enter an NFL team name or city:\n";
$input = <STDIN>;
chomp $input;

if ($source6 =~ /American Football Conference(.*)x - Clinched playoff/si)
{
    $theStandings = $1;
    $teamFound = 0;
    $regEx = '\/teams\/profile\?team=\w{2,3}">(.*?)<\/a>.*?<\/td>(.*?)<td class';

    # Loop iteration for each match that can be a team name.
    while ($theStandings =~ /$regEx/gsi)
    {
        $team = $1;
        $theRest = $2;
        # Remove non-space white space from the team name.
        $team =~ tr/\n\t//d;

        # Search for the input string within this particular team name.
        if ($team =~ /$input/i)
        {
            printf ("%21s", $team);
            # Find first three occurences of one or two digits in theRest.
            my $x = 0;
            while ($x < 3)
            {
                if ($theRest =~ /<td>(\d{1,2})<\/td>/g)
                {
                    printf ("%5d", $1);
                }
                else
                {
                    print "Couldn't find match\n";
                }
                $x++;
            }
            print "\n";

            # Change to true if a team matched.
            $teamFound = 1;
        }
    }

    if (!$teamFound)
    {
        print "No teams matched this input.\n";
    }
}
else
{
    print "Could not find match in source6.\n";
}

