#!/usr/bin/perl

# Takes in data from Add-Edit.pl and updates database, then either returns to Add-Edit automatically or provides links to Add-Edit and Index.pl

use strict;
use CGI qw(:standard);
use CGI::Session;
use File::Spec;
use DBI;

my $dsn = "DBI:mysql:f16final:localhost";
my $dbh = DBI->connect ($dsn, "root", "password", {PrintError => 0});

if (!$dbh)
{
    print header();
    print start_html(-title=>"Database Error", -BGCOLOR=>'EEEEEE');
    print "<body>";
    print "Unable to connect to the database", br;
    print a ( {-href=>'/cgi-bin/index.pl', -target=>'_self'}, "Click to return to main page\n"), br;
    print "</body>";
    print "</html>";
    exit;
}

my $sessionID = cookie ('loggedin');

my $session = new CGI::Session (undef, $sessionID,  {Directory=>File::Spec->tmpdir() } );

my $cookie;

if ($session->param ('loggedin'))
{
   # Get 60 more seconds of "logged in" time
   $cookie = cookie (-name=>'loggedin',
                     -value => $session->id,
                     -expires => '+1m' );
}

my $classToUpdate = param('cboClass');
my $newClassName = param('txtClassName');
my $newDepartment = param('txtDepartment');
my $newClassNum = param('txtClassNum');
my $newGrade = param('rdoGrade');
my $newCredits = param('cboCredits');

unless ($newClassName eq "" || $newDepartment eq "" || $newClassNum eq "")
{
    my $sql;
    if ($classToUpdate eq "New Class")
    {
        $sql = "INSERT INTO tblclasses (classname, department, classnum, grade, credits) VALUES ('$newClassName', '$newDepartment', '$newClassNum', '$newGrade', '$newCredits')";
    }
    else
    {
        my $classID;
        my $sql2 = "SELECT classID FROM tblclasses WHERE classname='$classToUpdate'";
        my $sth = $dbh->prepare($sql2);
        my $recordCount = $sth->execute();
        if ($recordCount > 0)
        {
            my $hashRef = $sth->fetchrow_hashref();
            $classID = $hashRef->{'classID'};
            $sql = "UPDATE tblclasses SET classname='$newClassName', department='$newDepartment', classnum='$newClassNum', grade='$newGrade', credits='$newCredits' WHERE classID = $classID";
        }
        else
        {
            print header(-cookie=>$cookie, -Refresh=>'5;URL=/cgi-bin/Add-Edit.pl'), start_html(-title=>'Update failure', -BGCOLOR=>'DDDDDD'), "Unable to find record to update, returning to edit page", br, end_html();
        }
    }

    my $sth = $dbh->prepare($sql);
    my $recordCount = $sth->execute();

    if ($recordCount > 0)
    {
        print header(-cookie=>$cookie), start_html(-title=>'Update Class', -BGCOLOR=>'C3FAA7');

        print "Add/Update successful\n", br, br;

        print a ( {-cookie=>$cookie, -href=>'/cgi-bin/Add-Edit.pl', -target=>'_self'}, "Return to add/edit page"), br, br;
        print a ( {-cookie=>$cookie, -href=>'/cgi-bin/index.pl', -target=>'_self'}, "Return to main page");

        print end_html();
    }
    else
    {
        print header(-cookie=>$cookie, -Refresh=>'5;URL=/cgi-bin/Add-Edit.pl'), start_html(-title=>'Update failure', -BGCOLOR=>'DDDDDD'), "Unable to update record, returning to edit page", br, end_html();
    }
}
else
{
    print header(-cookie=>$cookie, -Refresh=>'5;URL=/cgi-bin/Add-Edit.pl'), start_html(-title=>'Missing Info', -BGCOLOR=>'DDDDDD'), "Not all information was provided, returning to edit page", br, end_html();
}


