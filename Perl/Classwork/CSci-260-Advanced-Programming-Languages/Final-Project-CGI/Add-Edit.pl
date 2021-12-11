#!/usr/bin/perl

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
    my $sql = "SELECT classname, department, classnum, grade, credits from tblclasses";
    my $sth = $dbh->prepare($sql);
    my $recordCount = $sth->execute();

    if ($recordCount > 0)
    {
        my @classNames;
        $classNames[0] = "New Class";
        my $counter = 1;

        print header(-cookie=>$cookie), start_html(-title=>'Add/Update Classes', -BGCOLOR=>'C2A8FF');
        print start_form (-method=>'post', -action=>'/cgi-bin/UpdateDB.pl');

        print "<b>", "List of current classes\n", "</b>", br;
        print "<table border = 1>";
        print Tr(td("Class Name"),   td("Department"), 
                 td("Class Number"), td("Grade"), td("Credits"));
        while (my $hashRef = $sth->fetchrow_hashref())
        {
            $classNames[$counter] = $hashRef->{'classname'};
            $counter++;

            print Tr(td("$hashRef->{'classname'}"), 
                     td("$hashRef->{'department'}"), 
                     td("$hashRef->{'classnum'}"), 
                     td("$hashRef->{'grade'}"), 
                     td("$hashRef->{'credits'}"));
        }
        print "</table>";
        print br, br;


        print "Select a class to update or select \"New Class\" to add a new class:\n", br;
        print "Class Name ", popup_menu (-name=>'cboClass', -size=>1,
                                         -values=>[@classNames],
                                         -default=>'New Class'),
                                         br, br, "\n";
    }
    else
    {
        print header(-cookie=>$cookie), start_html(-title=>'Add Classes Only', -BGCOLOR=>'C2A8FF');
        print "Update of classes currently unavailable\n", br;
        print start_form (-method=>'post', -action=>'/cgi-bin/UpdateDB.pl',-cookie=>$cookie);
    }


    print "Enter the class name ", textfield (-name=>'txtClassName'), br, br;

    print "Enter the department ", textfield (-name=>'txtDepartment'), br, br;

    print "Enter the class number ", textfield (-name=>'txtClassNum'), br, br;

    print "Grade ", br, radio_group (-name=>'rdoGrade', -values=>['A', 'B', 'C', 'D', 'F', 'S', 'U'], ), br, br;

    print "Credits", popup_menu (-name=>'cboCredits', -size=>1,
                                 -values=>['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']), br, br;

    print submit(-name=>'btnUpdate', value=>'Update Class List'), br, br;

    print a ( {-cookie=>$cookie, -href=>'/cgi-bin/index.pl', -target=>'_self'}, "Return to main page");

    print end_form();
    print end_html();
}
else
{
    print header (-Refresh=>'5; URL=/cgi-bin/index.pl'), start_html(-title=>"Login failure", -BGCOLOR=>'EEEEEE'), "You are logged out, returning to main page, or log in ", a ( {-href=>'/cgi-bin/Login.pl', -target=>'_self'}, "here."), br, end_html();
}
