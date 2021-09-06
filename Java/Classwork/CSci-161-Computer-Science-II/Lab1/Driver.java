/**
 * The Driver Class is used to simulate a course load.  
 * The Driver requires the Course class.
 * <br><br>
 * @author Lance Wilson
 * @version Lab 1, 1/28/2016
 */
import java.util.*;

public class Driver
{
    public static void main(String[] args)
    {
        String user_name;   // The name of the user
        int credit_hours, credit_hours_total = 0;   // The number of credit hours, and the running total.
        double homework_hours, homework_hours_total = 0;    //The number of homework hours & running total.
        Scanner cmdLine = new Scanner(System.in);   // Scanner for input.
        Random rand = new Random();     // Random number generator.

        while (credit_hours_total < 22 && homework_hours_total < 168.0)
        {
            Course course = new Course();   // New course class.
            credit_hours = -1;              // Set to -1 to run below while loops.
            homework_hours = -1.0;

            // Ask the user for a course name and enter it into the course's setName method.
            System.out.println("Please enter the course name.");
            course.setName(cmdLine.nextLine());

            // Take a random number -2 to 10 each time through, and try to set it to the number of credit hours until successful.
            while (credit_hours == -1)
            {
                course.setCredit((rand.nextInt(13) - 2));
                credit_hours = course.getCredit();
                if (credit_hours == -1)
                {
                    System.out.println("Bad Credit Hours Input");
                }
            }

            // Take a random number -3.0 to 30 each time through, and try to set it to the number of credit hours until successful.
            while (homework_hours == -1.0)
            {
                course.setHomework((rand.nextDouble() * 33.0) - 3.0);
                homework_hours = course.getHomework();
                if (homework_hours == -1.0)
                {
                    System.out.println("Bad Homework Hours Input");
                }
            }

            // Print the course and credit hours for this course.
            System.out.printf(course.getName() + " has " + course.getCredit() + " credit hours and %2.1f homework hours.\n", course.getHomework());

            // Add course and credit hours to the running total.
            credit_hours_total += credit_hours;
            homework_hours_total += homework_hours;

        }

        // Ask the user for their name.
        System.out.println("\nPlease enter your name.");
        user_name = cmdLine.nextLine();

        // Show the users course load in terms of total credit and total homework hours.
        System.out.printf(user_name + ", your total generated credit hours is " + credit_hours_total + " and your total generated homework hours is %3.1f.\n", homework_hours_total);


    }
}
