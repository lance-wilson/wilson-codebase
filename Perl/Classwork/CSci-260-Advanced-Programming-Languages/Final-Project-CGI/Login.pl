#!/usr/bin/perl

use strict;
use CGI qw(:standard);

print header(), start_html(-title=>"Login Page", -BGCOLOR=>'D7B2F7');

print start_form (-method=>'post', -action=>'/cgi-bin/verifyLoginInfo.pl');

print "Enter your login information", br, br;

print "Username", textfield (-name=>'txtUsername'), br, br;

print "Password", password_field (-name=>'txtPassword'), br, br;

print submit(-name=>'cmdLogin', value=>'Login');

print end_form(), end_html();
