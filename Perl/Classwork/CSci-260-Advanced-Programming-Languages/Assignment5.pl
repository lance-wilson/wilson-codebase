#!/usr/bin/perl
# Lance Wilson
# Program Assignment 5
#
# Summary: Adds, updates, deletes, and searches for records in a database storing song information.

use strict;
use DBI;

# Database login credentials
my $username = "root";
my $password = "password";

# Database location
my $dsn = "DBI:mysql:prog5:localhost";
my $dbh = DBI->connect($dsn, $username, $password);

if (!$dbh)
{
    print "Unable to connect to the database\n";
    exit;
}

# Subroutine for displaying all records.
sub display_records()
{
    # Collect everything from the songs table.
    my $sql = "SELECT * from songs";
    my $sth = $dbh->prepare($sql);
    my $recordCount = $sth->execute();

    print "List of song records:\n";
    print "-------------------------------------\n";

    if ($sth)
    {
        # Category header.
        printf ("%-7s %-35s %-35s %-25s %-7s\n", "songid", "artist", "title", "album", "time");
        while (my $hashRef = $sth->fetchrow_hashref())
        {
            printf ("%-7d %-35s %-35s %-25s %-7s\n", $hashRef->{songid}, $hashRef->{artist}, $hashRef->{title}, $hashRef->{album}, $hashRef->{'time'});
        }
    }
    else
    {
        print "Unable to display records\n"
    }
    print "\n";
}

# Ensure that menu will print at least once.
my $option = "continue";

# Continue the menu until the user enters exit.
until ($option eq "exit")
{
    # Main menu
    print "Type a command to perform a specified action on the songs table or type \"exit\" to exit:\n";
    print "\tCommand\t\tAction\n";
    print "\tAdd\t\tAdd record\n";
    print "\tUpdate\t\tUpdate record\n";
    print "\tDelete\t\tDelete record\n";
    print "\tTitle\t\tSearch by artist or title\n";
    print "\tAlbum\t\tSearch by album\n";

    $option = <STDIN>;
    chomp $option;
    # Make user entry all lowercase.
    $option = lc ($option);

    print "\n\n";

    # Add a song
    if ($option eq "add")
    {
        my ($artist, $title, $album, $time);
        print "Enter the song artist, title, album, and run time in M:SS format (hit enter between each), or enter \"back\" for artist to return to the main menu\n";
        print "Artist:  ";
        $artist = <STDIN>;
        chomp $artist;
        # If the artist is "back", tell the user that we are returning to the menu.
        if ($artist eq "back")
        {
            print "Returning to menu...\n"
        }
        # Otherwise, collect the other three fields and replace the apostrophes with escaped apostrophes.
        else
        {
            $artist =~ s|\'|\\'|g;

            print "Title:  ";
            $title = <STDIN>;
            chomp $title;
            $title =~ s|\'|\\'|g;

            print "Album:  ";
            $album = <STDIN>;
            chomp $album;
            $album =~ s|\'|\\'|g;

            print "Run Time:  ";
            $time = <STDIN>;
            chomp $time;
            $time =~ s|\'|\\'|g;

            # Add the info only if none of them are empty strings.
            if ($artist ne "" && $title ne "" && $album ne "" && $time ne "")
            {
                my $sql = "INSERT INTO songs (artist, title, album, time) VALUES ('$artist', '$title', '$album', '$time')";
                my $result = $dbh->do ($sql);

                if ($result)
                {
                    print "Info added successfully\n";
                }
                else
                {
                    print "Adding info failed\n";
                }
            }
            # If any fields were left empty, return to menu.
            else
            {
                print "Not all fields were provided. Returning to menu\n";
            }
        }
    }
    # Updating records.
    elsif ($option eq "update")
    {
        # Display all records.
        display_records();

        print "Enter the songid of the song whose information you would like to edit or enter \"back\" to return to the main menu\n";
        my $id = <STDIN>;
        chomp $id;

        if ($id eq "back")
        {
            print "Returning to main menu\n";
        }
        # Update records only if the user did not enter "back".
        else
        {
            # Get the info from the song with that id.
            my $sql = "SELECT * from songs WHERE songid = $id";
            my $sth = $dbh->prepare($sql);
            my $recordCount = $sth->execute();
            if ($sth)
            {
                my ($prevArtist, $prevTitle, $prevAlbum, $prevTime);
                my $hashRef = $sth->fetchrow_hashref();
                # Take note of previous values.
                $prevArtist = $hashRef->{artist};
                $prevTitle = $hashRef->{title};
                $prevAlbum = $hashRef->{album};
                $prevTime = $hashRef->{'time'};

                print "Enter the new artist, title, album, and run time for the song (hit enter after each one). If there is no change, hit enter.\n";
                my ($artist, $title, $album, $time);

                # Collect new data for each field, and replace the apostrophes with escaped apostrophes. If the user entered an empty string, use the previous value.
                print "Artist:  ";
                $artist = <STDIN>;
                chomp $artist;
                $artist =~ s|\'|\\'|g;
                if ($artist eq "")
                {
                    $artist = $prevArtist;
                }

                print "Title:  ";
                $title = <STDIN>;
                chomp $title;
                $title =~ s|\'|\\'|g;
                if ($title eq "")
                {
                    $title = $prevTitle;
                }

                print "Album:  ";
                $album = <STDIN>;
                chomp $album;
                $album =~ s|\'|\\'|g;
                if ($album eq "")
                {
                    $album = $prevAlbum;
                }

                print "Run time:  ";
                $time = <STDIN>;
                chomp $time;
                $time =~ s|\'|\\'|g;
                if ($time eq "")
                {
                    $time = $prevTime;
                }

                $sql = "UPDATE songs SET artist = '$artist', title = '$title', album = '$album', time = '$time' WHERE songid = $id";
                my $result = $dbh->do($sql);
                if ($result)
                {
                    print "Record updated\n";
                    display_records();
                }
                else
                {
                    print "Unable to modify record\n";
                }
            }
            else
            {
                print "Problem finding data for song $id\n";
            }
        }
    }
    # Delete record.
    elsif ($option eq "delete")
    {
        # Display all records.
        display_records();

        print "Select the songid of the song you would like to delete, or enter \"back\" to go back to the main menu\n";
        my $delID = <STDIN>;
        chomp $delID;

        if ($delID eq "back")
        {
            print "Returning to the main menu...\n";
        }
        # Continue only if back wasn't entered.
        else
        {
            my $sql = "DELETE FROM songs WHERE songid = $delID";
            my $sth = $dbh->prepare($sql);
            my $recordCount = $sth->execute();
            if ($sth)
            {
                print "Record deleted\n\n";
                display_records();
            }
            else
            {
                print "Unable to delete record\n";
            }
        }
    }
    # Search for text in artist or title.
    elsif ($option eq "title")
    {
        print "Enter text to search for in song titles or artist names, or enter \"back\" to go back to the main menu\n";

        my $search = <STDIN>;
        chomp $search;

        # Continue if search isn't for "back".
        unless ($search eq "back")
        {
            # Search for any title or artist containing the search string.
            my $sql = "SELECT * FROM songs WHERE title like \'\%$search\%\' or artist like \'\%$search\%\'";
            my $sth = $dbh->prepare($sql);
            my $recordCount = $sth->execute();
            # Print records onlly if some were found.
            if ($sth && $recordCount != 0)
            {
                printf ("%-7s %-35s %-35s %-25s %-7s\n", "songid", "artist", "title", "album", "time");
                # Print rows while there is still data.
                while (my $hashRef = $sth->fetchrow_hashref())
                {
                    printf ("%-7d %-35s %-35s %-25s %-7s\n", $hashRef->{songid}, $hashRef->{artist}, $hashRef->{title}, $hashRef->{album}, $hashRef->{'time'});
                }
            }
            else
            {
                print "No records with this match were found\n";
            }
        }
        else
        {
            print "Returning to main menu...\n";
        }
    }
    # Search by Album title.
    elsif ($option eq "album")
    {
        print "Enter an album title, or enter \"back\" to go back to the main menu\n";

        my $search = <STDIN>;
        chomp $search;

        unless ($search eq "back")
        {
            # Search for the exact match of the entered album.
            my $sql = "SELECT title, time FROM songs WHERE album = \'$search\'";
            my $sth = $dbh->prepare($sql);
            my $recordCount = $sth->execute();
            # Print records only if some were found.
            if ($sth && $recordCount != 0)
            {
                printf ("%-35s %-7s\n", "title", "time");
                while (my $hashRef = $sth->fetchrow_hashref())
                {
                    printf ("%-35s %-7s\n", $hashRef->{title}, $hashRef->{'time'});
                }
            }
            else
            {
                print "No records with this match were found\n";
            }
        }
        else
        {
            print "Returning to main menu...\n";
        }
    }

    print "\n";
}
