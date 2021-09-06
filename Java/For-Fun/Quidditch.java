import java.util.*;

public class Quidditch
{
    public static void main(String[] args)
    {
        // Variables: hours and minutes are the time of play, time_weight determines the number of days, snitch_time is the number of minutes until the snitch is caught, play_weight decides what happens during each play down the field, snitch_weight decides who captures the snitch, coin_flip decides who starts with the quaffle, and possession1 determines the status of team 1's possession of the quaffle.
        int hours, minutes, time_weight, snitch_time, play_weight, snitch_weight, coin_flip;
        boolean possession1 = false;

        // Have to define the variables outside the loop to be used later.
        Team team1;
        Team team2;
        // If command-lines arguments are forgotten, get user input.
        if (args.length < 2)
        {
            // Scan in the name of team 1 and create a new team with that name.
            Scanner teamScan = new Scanner(System.in);
            System.out.println("Please enter the name of the first team.");
            team1 = new Team(teamScan.nextLine());

            // Scan in the name of team 2 and create a new team with that name.
            System.out.println("Please enter the name of the second team.");
            team2 = new Team(teamScan.nextLine());
            teamScan.close();
        }
        // Otherwise, can use command line arguments to get team name.
        else
        {
            team1 = new Team(args[0]);
            team2 = new Team(args[1]);
        }

        Random rand = new Random();
        
        // Determine the value of time_weight and hours.
        time_weight = rand.nextInt(10);
        hours = rand.nextInt(25);
        // If hours is 0, then minutes will be generated independently, and the snitch_time will be set to the number of minutes.
        if (hours == 0)
        {
            minutes = rand.nextInt(60);
            snitch_time = minutes;
        }
        // If hours is not 0, then minutes will be set to hours * 60.
        else
        {
            minutes = hours * 60;

            // 70% of the time, the game will end in one day, and snitch_time will be set to the number of minutes.
            if (time_weight < 7)
            {
                snitch_time = minutes;
            }
            // 20% of the time, the game will be more than one day long, but less than two days long. snitch_time will be set to the number of minutes plus the number of minutes in one day.
            else if (time_weight >= 7 && time_weight < 9)
            {
                snitch_time = minutes + 1440;
            }
            // 10% of the time, the game will be more two days long, and snitch_time will be set to the number of minutes plus the number of seconds in two days.
            else
            {
                snitch_time = minutes + 2880;
            }
        }

        // Coin flip to see who starts with the quaffle
        coin_flip = rand.nextInt(2);
        if (coin_flip == 0)
        {
            possession1 = true;
        }
        else
        {
            possession1 = false;
        }

        // One "play" will happen every minute until the snitch is caught.
        for (int i = 0; i < snitch_time; i++)
        {
            play_weight = rand.nextInt(1000);

            // 45% of the time, the other team's chasers will steal the quaffle.
            if (play_weight < 450)
            {
                //chaser turnover
                if (possession1)
                {
                    //System.out.println("Steal by chaser of the " + team2.getTeamName());
                    possession1 = false;
                }
                else
                {
                    //System.out.println("Steal by chaser of the " + team1.getTeamName());
                    possession1 = true;
                }
            }
            // 22.5% of the time, the chasers will take a shot, but the keeper will save it.
            else if (play_weight >= 450 && play_weight < 775)
            {
                //save
                if (possession1)
                {
                    //System.out.println("Shot by chaser of the " + team1.getTeamName() + " was saved by Keeper of the " + team2.getTeamName());
                    possession1 = false;
                }
                else
                {
                    //System.out.println("Shot by chaser of the " + team2.getTeamName() + " was saved by Keeper of the " + team1.getTeamName());
                    possession1 = true;
                }
            }
            // 5% of the time, the chasers will score.
            else if (play_weight >= 775 && play_weight < 815)
            {
                //score
                if (possession1)
                {
                    team1.addScore(10);
                    System.out.println("Shot by chaser of " + team1.getTeamName() + " scored at minute " + Integer.toString(i) + ". Current score is " + team1.getTeamName() + ": " + team1.getScore() + ", " + team2.getTeamName() + ": " + team2.getScore());
                    possession1 = false;
                }
                else
                {
                    team2.addScore(10);
                    System.out.println("Shot by chaser of " + team2.getTeamName() + " scored at minute " + Integer.toString(i) + ". Current score is " + team1.getTeamName() + ": " + team1.getScore() + ", " + team2.getTeamName() + ": " + team2.getScore());
                    possession1 = true;
                }
            }
            //18.5% of the time, the beaters will hit a bludger that distracts the chasers and causes them to lose the quaffle.
            else
            {
                //bludger
                if (possession1)
                {
                    //System.out.println("Chaser of " + team1.getTeamName() + " was distracted by a bludger and lost the quaffle.");
                    possession1 = false;
                }
                else
                {
                    //System.out.println("Chaser of " + team2.getTeamName() + " was distracted by a bludger and lost the quaffle.");
                    possession1 = true;
                }
            }
        }

        // Capture Snitch
        snitch_weight = rand.nextInt(10);
        if (snitch_weight < 5)
        {
            // Team one captures snitch
            team1.addScore(150);
            if (hours == 0)
            {
                System.out.println("After " + snitch_time + " minutes, the Seeker of " + team1.getTeamName() + " captured the snitch to end the game.");
            }
            else
            {
                System.out.println("After " + (snitch_time/60) + " hours, the Seeker of " + team1.getTeamName() + " captured the snitch to end the game.");
            }
        }
        else
        {
            // Team two captures snitch
            team2.addScore(150);
            if (hours == 0)
            {
                System.out.println("After " + snitch_time + " minutes, the Seeker of " + team2.getTeamName() + " captured the snitch to end the game.");
            }
            else
            {
                System.out.println("After " + (snitch_time/60) + " hours, the Seeker of " + team2.getTeamName() + " captured the snitch to end the game.");
            }
        }

        // Print the match's results
        if (team1.getScore() > team2.getScore())
        {
            System.out.println(team1.getTeamName() + " won the match with a final score " + team1.getScore() + "-" + team2.getScore());
        }
        else if (team1.getScore() < team2.getScore())
        {
            System.out.println(team2.getTeamName() + " won the match with a final score " + team2.getScore() + "-" + team1.getScore());
        }
        else
        {
            System.out.println("The match ended in a tie, with both teams scoring " + team1.getScore() + " points.");
        }
    }
}
