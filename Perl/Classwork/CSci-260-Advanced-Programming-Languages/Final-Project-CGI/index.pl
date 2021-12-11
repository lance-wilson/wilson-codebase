#!/usr/bin/perl

use strict;
use CGI qw(:standard);
use CGI::Session;
use File::Spec;

my $sessionID = cookie ('loggedin');

my $session = new CGI::Session (undef, $sessionID,  {Directory=>File::Spec->tmpdir() } );


print header();

print start_html(-title=>"Home", -BGCOLOR=>'FAD7AE');

print "<body>";

my $cookie;

if ($session->param ('loggedin'))
{
   # Get 60 more seconds of "logged in" time
   $cookie = cookie (-name=>'loggedin',
                     -value => $session->id,
                     -expires => '+1m' );

   my $name = $session->param('name');
   print "Hello, $name\n", br;

}

print a ( {-href=>'/cgi-bin/Login.pl', -target=>'_self'}, "Login"), br;
print a ( {-cookie=>$cookie, -href=>'/cgi-bin/Search.pl', -target=>'_blank'}, "Search/Transcript"), br;

if ($session->param ('loggedin'))
{
	print a ( {-cookie=>$cookie, -href=>'/cgi-bin/Add-Edit.pl', -target=>'_blank'}, "Add or Edit Classes"), br;
}

print "</body>";
print "</html>";

