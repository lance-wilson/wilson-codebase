#!/usr/bin/perl
# Lance Wilson
#
# Summary: Determine the olympic standings for golf based on the current world golf ranking.

use strict;

use LWP::Simple;

my ($page, $eligibleGolfers, $url, $source, $theRest, $innerArea, $country_code, $country_name, %country_hash, $key, $thisGolfer, $ranking, $golfName, %golfers, %thisGolfHash, $position, %usedCountries);

$page = 1;
$eligibleGolfers = 60;
# Number to keep track of how many golfers are currently in the field.
$position = 1;

# Header for table.
print "Number\tWR\tGolfer\t\t\tCountry\n";

while ($position <= $eligibleGolfers)
{
    # Web addresses.
    $url = 'http://www.owgr.com/Ranking.aspx?pageNo=' . $page . '&pageSize=300&country=All';

    # Get source code.
    $source = get $url;

    if ($source =~ /<option value="ALA"(.*)Zimbabwe<\/option>/s)
    {
        $innerArea = $1;

        while ($innerArea =~ /<option value="(.*)">(.*)<\/option>/g)
        {
            $country_code = $1;
            $country_name = $2;

            @country_hash{$country_code} = $country_name;
        }

        $country_hash{'ALA'} = 'Aland Islands';
        $country_hash{'JPN'} = 'Japan';
        $country_hash{'ZIM'} = 'Zimbabwe';
    }

    if ($source =~ /<div class="table(.*)<\/table>/s)
    {
        $theRest = $1;

        # Get data up to first 
        while ($theRest =~ /<tr>(.*?)<\/tr>(.*)/s)
        {
            $thisGolfer = $1;
            $theRest = $2;

            # Get this golfer's ranking.
            if ($thisGolfer =~ /<td>.*<\/span>(.*)<\/td>/g)
            {
                $ranking = $1;
            }
            # Get this golfer's country code.
            if ($thisGolfer =~ /<td class="ctry">.*title ="(.*)".*<\/td>/g)
            {
                $country_code = $1;
            }
            # Get this golfer's name.
            if ($thisGolfer =~ /<td class="name"><.*>(.*)<\/a><\/td>/g)
            {
                $golfName = $1;
            }

            # Store the golfer's information, using the world ranking as keys.
            if ($golfName and $country_code and $ranking)
            {
                $thisGolfHash{'name'} = $golfName;
                $thisGolfHash{'country_code'} = $country_code;
                $thisGolfHash{'country'} = $country_hash{$country_code};

                $golfers{$ranking} = {%thisGolfHash};
            }
        }
    }
    else
    {
        print "Could not find match in table.\n";
    }

    # Sort through the golfers and print out the ones eligible for the Olympics.
    # Sort on the world rankings numerically.
    foreach $key (sort {$a <=> $b} keys %golfers)
    {
        if ($page == 1)
        {
            # For the top 15 golfers, there can be 4 from a country.
            if ($key <= 15 and $usedCountries{$golfers{$key}{'country_code'}} < 4)
            {
                printf("%d\t%s\t%-20s\t%s\n", $position, $key, $golfers{$key}{'name'}, $golfers{$key}{'country'});
                $position += 1;
                $usedCountries{$golfers{$key}{'country_code'}} += 1;
            }
            # For the rest, there can be two per country.
            elsif ($position <= $eligibleGolfers and $usedCountries{$golfers{$key}{'country_code'}} < 2)
            {
                printf("%d\t%s\t%-20s\t%s\n", $position, $key, $golfers{$key}{'name'}, $golfers{$key}{'country'});
                $position += 1;
                $usedCountries{$golfers{$key}{'country_code'}} += 1;
            }
        }
        # If we're past the first page, don't include the first page results
        #   to avoid some of the top 15 being duplicated.
        elsif ($page > 1 and $key > 300)
        {
            if ($position <= $eligibleGolfers and $usedCountries{$golfers{$key}{'country_code'}} < 2)
            {
                printf("%d\t%s\t%-20s\t%s\n", $position, $key, $golfers{$key}{'name'}, $golfers{$key}{'country'});
                $position += 1;
                $usedCountries{$golfers{$key}{'country_code'}} += 1;
            }
        }
    }

    $page += 1;
}

print "\nTotals for each country:\n";
foreach $key (sort {$usedCountries{$b} <=> $usedCountries{$a}} keys %usedCountries)
{
    printf("%-20s%d\n", $country_hash{$key}, $usedCountries{$key});
}

