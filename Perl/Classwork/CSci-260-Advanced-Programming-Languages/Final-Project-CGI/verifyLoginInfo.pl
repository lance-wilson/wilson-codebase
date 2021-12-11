#!/usr/bin/perl

use strict;
use CGI qw(:standard);
use CGI::Session;
use File::Spec;
use DBI;

my $username = param ('txtUsername');
my $password = param ('txtPassword');

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

my $sql = "SELECT login, password, name from tblusers where login=\'$username\' and password=\'$password\'";
my $sth = $dbh->prepare($sql);
my $recordCount = $sth->execute();

if ($recordCount > 0)
{
    my $hashRef = $sth->fetchrow_hashref();
    #create cooke on the server with the user information
    #1st argument - dsn info - leave blank (undef)
    #2nd argument - session id, set to undef to create a new session 
    #3rd argument - where should the cookie be store on the server
    my $session = new CGI::Session (undef, undef,  {Directory=>File::Spec->tmpdir()});
    $session->param ('loggedin', 'yes');
    $session->param('username', $username);
    $session->param('name', $hashRef->{'name'});
    $session->close();

    my $cookie = cookie (-name=>'loggedin',
                         -value => $session->id,
                         -expires => '+1m' );
    print redirect (-cookie=>$cookie, -location=>'/cgi-bin/index.pl'), start_html(), end_html();
}
else
{
    print header (-Refresh=>'3; URL=/cgi-bin/index.pl'), start_html(-title=>"Login failure", -BGCOLOR=>'EEEEEE'), "Login failed, returning to main page", br, end_html();
}
