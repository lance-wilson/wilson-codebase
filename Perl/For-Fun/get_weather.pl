#!/usr/bin/perl
# Lance Wilson
#
# Summary: Get metar data from weather.rap.ucar.edu and display in terminal.
#
# Syntax: perl get_weather.pl site_id
#
# Example: perl get_weather.pl kfar
#
# Alias: get_wx='perl get_weather.pl'
#

use strict;

use LWP::Simple;

my ($url, $source, $site, $metar, $metars, $innerArea, $lead, $i, $hour);

$site = 'kfar';
if (@ARGV)
{
    $site = $ARGV[0];

    #if ($ARGV[1])
    #{
    #    $hour = $ARGV[1];
    #    #print("$hour\n");
    #}
}
else
{
    print("Using default site $site\n");
}

# Web address.
$url = 'http://weather.rap.ucar.edu/surface/index.php?metarIds=' . $site . '&hoursStr=most+recent+only&std_trans=standard&num_metars=number&submit_metars=Retrieve';

# Code to change url so that you get more than most recent, but need to change regex block to actually get them.
#if ($hour)
#{
#    if ($hour < 1 or $hour > 60)
#    {
#        print("Invalid hour.\n");
#    }
#    elsif ($hour >= 6 or $hour <= 60)
#    {
#        $hour = int($hour/6) * 6;
#        $url = 'http://weather.rap.ucar.edu/surface/index.php?metarIds=' . $site . '&hoursStr=past+' . $hour . '+hours&std_trans=standard&num_metars=number&submit_metars=Retrieve';
#    }
#}

$source = get $url;

# Find the section of the page with METARs.
if ($source =~ /<SPAN CLASS="monospace">\n((.*)<BR>.*;<BR>.*)<\/SPAN>/s)
{
    $metars = $1;
    # If not enough letters are entered, will return every METAR starting with
    #   those letters.
    while ($metars =~ /(.*?)<BR>.*?;<BR>(.*)/gs)
    {
        $metar = $1;
        $metars = $2;
        # Remove trailing newline from METARs.
        $metar =~ tr/\n\t//d;
        print("$metar\n");
    }
}
else
{
    print("Retrieval of METAR failed.\n");
}

