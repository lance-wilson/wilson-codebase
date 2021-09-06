/**
 * The ScheduleGenerator Class is used to generator a random assortment of classes within a specified course load, and write the name, credit hour number, and homework hour number data to a file.  
 * The ScheduleGenerator requires the Course class.
 * <br><br>
 * @author Lance Wilson
 * @version Lab 2, 2/4/2016
 */
import java.util.*;
import java.io.*;

public class ScheduleGenerator
{
    public static void main(String[] args) throws FileNotFoundException
    {

        int credit_gen, credit_hours = 0;  // Number of credit hours to generate and credit hours for one course.
        double homework_hours;  // Number of homework hours.
        String name = "";       // Name of course.

        // Random generator.
        Random rand = new Random();
        // File writer that writes to "Course_dat.txt"
        PrintWriter outCourse = new PrintWriter("Course_dat.txt");

        // Generates a random number of total credit hours and print the total.
        credit_gen = (rand.nextInt(19)+6);
        System.out.println("Credit Hours: " + credit_gen);

        // Runs through the number of credits
        for (int credit_current = 0; credit_current < credit_gen;)
        {
            name = randomWord();
            int credit_max = credit_gen - credit_current;
            
            // If the number of credits remaining to allocate is greater than the maximum size for a course, then generate a random number of credit hours 0 through 6 inclusive.
            if (credit_max > 6)
            {
                credit_hours = rand.nextInt(7);
            }
            // If the number of credits remaining to allocate is less than the maximum size for a course, then generate a random number of credit hours 0 through the number of credit hours left, inclusive.
            else if (credit_max <= 6 && credit_max > 1)
            {
                credit_hours = rand.nextInt(credit_max+1);
            }
            // If there is one credit hour left, it must be set to one to avoid an infinite loop. 
            else if (credit_max == 1)
            {
                credit_hours = 1;
            }
            // Starting value for homework hours that will always be invalid.
            homework_hours = 30.0;

            // If credit_hours is 0, then homework hours must be 0.
            if (credit_hours == 0)
            {
                homework_hours = 0;
            }
            else
            {
                // Randomly generators a number of homework hours that is less than 4 times the credit hours.
                while (homework_hours > 4*credit_hours)
                {
                    homework_hours = (rand.nextDouble()*24);
                }
            }
            
            // Writes data to file.
            outCourse.println(name + " " + credit_hours + " " + homework_hours);
            // Increments the counter variable so that the loop doesn't overshoot.
            credit_current+=credit_hours;
        }
        // Close file
        outCourse.close();

    }

    public static String randomWord()
    {
        char base = 'a';
        Random random = new Random();
        String word = "";
        int length = random.nextInt(13) + 3;
        for (int i = 0; i < length; i++)
        {
            char letter = (char)(random.nextInt(26)+base);
            word = word + letter;
        }

        return word;
    }
}
