#!/usr/bin/perl

use strict;
use CGI qw(:standard);
use CGI::Session;
use File::Spec;
use DBI;

unless (param('btnAll') || param('btnSearch'))
{
    param('btnAll', 'true');
}

my $sessionID = cookie ('loggedin');
my $search = param ('txtSearch');

my $session = new CGI::Session (undef, $sessionID,  {Directory=>File::Spec->tmpdir() } );

my $cookie;

if ($session->param ('loggedin'))
{
   # Get 60 more seconds of "logged in" time
   $cookie = cookie (-name=>'loggedin',
                     -value => $session->id,
                     -expires => '+1m' );
}

my $dsn = "DBI:mysql:f16final:localhost";
my $dbh = DBI->connect ($dsn, "root", "password", {PrintError => 0});

if (!$dbh)
{
    print header();
    print start_html(-title=>"Database Error", -BGCOLOR=>'EEEEEE');
    print "<body>";
    print "Unable to connect to the database";
    print "</body>";
    print "</html>";
    exit;
}

my $totalcredits = 0;
my $passed = 0;
my $gpapoints = 0;
my $gpacredits = 0;

if (param('btnAll'))
{
    my $sql = "SELECT classname, department, classnum, grade, credits FROM tblclasses";
    my $sth = $dbh->prepare($sql);
    my $recordCount = $sth->execute();

    if ($recordCount > 0)
    {
        print header(-cookie=>$cookie), start_html(-title=>"Transcript", 
                                   -BGCOLOR=>'C3FAA7');
        print "<body>";
        print "<b>", "List of all classes:\n", "</b>", br, br;
        print "<table border = 1>";
        print Tr(td("Class Name"),   td("Department"), 
                 td("Class Number"), td("Grade"), td("Credits"));
        while (my $hashRef = $sth->fetchrow_hashref())
        {
            $totalcredits += $hashRef->{'credits'};
            if ($hashRef->{'grade'} ne "F" and $hashRef->{'grade'} ne "U")
            {
                $passed += $hashRef->{'credits'};
            }
            if ($hashRef->{'grade'} ne "S" and $hashRef->{'grade'} ne "U")
            {
                $gpacredits += $hashRef->{'credits'};
            }

            # Calculate the number of GPA points.
            if ($hashRef->{'grade'} eq "A")
            {
                $gpapoints += (4.0 * $hashRef->{'credits'});
            }
            elsif ($hashRef->{'grade'} eq "B")
            {
                $gpapoints += (3.0 * $hashRef->{'credits'});
            }
            elsif ($hashRef->{'grade'} eq "C")
            {
                $gpapoints += (2.0 * $hashRef->{'credits'});
            }
            elsif ($hashRef->{'grade'} eq "D")
            {
                $gpapoints += (1.0 * $hashRef->{'credits'});
            }

            print Tr(td("$hashRef->{'classname'}"), 
                     td("$hashRef->{'department'}"), 
                     td("$hashRef->{'classnum'}"), 
                     td("$hashRef->{'grade'}"), 
                     td("$hashRef->{'credits'}"));
        }
        print "</table>";
    }
    else
    {
        print header (-cookie=>$cookie, -Refresh=>'; URL=/cgi-bin/Search.pl'), start_html(-title=>"No Match found", -BGCOLOR=>'EEEEEE'), "No classes found, returning to search page\n", br, end_html();
    }
}
elsif (param('btnSearch'))
{
    $search =~ s|\'|\\'|g;

    my $sql = "SELECT classname, department, classnum, grade, credits FROM tblclasses WHERE classname like \'\%$search\%\' or department like \'\%$search\%\'";
    my $sth = $dbh->prepare($sql);
    my $recordCount = $sth->execute();

    if ($recordCount > 0)
    {
        print header(-cookie=>$cookie), start_html(-title=>"Transcript", 
                                   -BGCOLOR=>'C3FAA7');
        print "<body>";
        print "<b>", "List of matching classes:\n", "</b>", br, br;
        print "<table border = 1>";
        print Tr(td("Class Name"),   td("Department"), 
                 td("Class Number"), td("Grade"), td("Credits"));
        while (my $hashRef = $sth->fetchrow_hashref())
        {
            $totalcredits += $hashRef->{'credits'};
            if ($hashRef->{'grade'} ne "F" and $hashRef->{'grade'} ne "U")
            {
                $passed += $hashRef->{'credits'};
            }
            if ($hashRef->{'grade'} ne "S" and $hashRef->{'grade'} ne "U")
            {
                $gpacredits += $hashRef->{'credits'};
            }

            # Calculate the number of GPA points.
            if ($hashRef->{'grade'} eq "A")
            {
                $gpapoints += (4.0 * $hashRef->{'credits'});
            }
            elsif ($hashRef->{'grade'} eq "B")
            {
                $gpapoints += (3.0 * $hashRef->{'credits'});
            }
            elsif ($hashRef->{'grade'} eq "C")
            {
                $gpapoints += (2.0 * $hashRef->{'credits'});
            }
            elsif ($hashRef->{'grade'} eq "D")
            {
                $gpapoints += (1.0 * $hashRef->{'credits'});
            }

            print Tr(td("$hashRef->{'classname'}"), 
                     td("$hashRef->{'department'}"), 
                     td("$hashRef->{'classnum'}"), 
                     td("$hashRef->{'grade'}"), 
                     td("$hashRef->{'credits'}"));
        }
        print "</table>";


    }
    else
    {
    print header (-cookie=>$cookie, -Refresh=>'3; URL=/cgi-bin/Search.pl'), start_html(-title=>'No Match found', -BGCOLOR=>'DDDDDD'), "No classes found with this match, returning to search page", br, end_html();
    }
}

print br;

my $gpa = 0.00;
if ($gpapoints != 0)
{
    $gpa = $gpapoints/$gpacredits;
}

# Print transcript
print "<b>", "Transcript", "</b>", br;
print "<table border = 1>";
print Tr(td("Passed Credits"), td("Attempted Credits"), 
         td("Honor Points"),   td("GPA"));
printf (Tr(td($passed), td($totalcredits),
         td($gpapoints), td("%.2f")), $gpa);
print "</table>";

print br, br;

if ($session->param ('loggedin'))
{
    print a ( {-cookie=>$cookie, -href=>'/cgi-bin/Add-Edit.pl', -target=>'_self'}, "Click to add or update a class\n"), br;
}

print br, br, a ( {-cookie=>$cookie, -href=>'/cgi-bin/index.pl', -target=>'_self'}, "Return to main page");

print "</body>";
print end_html();
