#!/usr/bin/perl

use strict;
use CGI qw(:standard);
use CGI::Session;
use File::Spec;

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

print header(-cookie=>$cookie), start_html(-title=>"Transcript Request", -BGCOLOR=>'D7B2F7');

print start_form (-method=>'post', -action=>'/cgi-bin/Transcript.pl');

print "Enter a search term or click All", br, br;

print textfield (-name=>'txtSearch'), br, br;

print submit(-name=>'btnSearch', value=>'Search');
print "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
print submit(-name=>'btnAll', value=>'All');

print end_form(), end_html();
