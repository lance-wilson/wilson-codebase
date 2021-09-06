/**
 * The ScheduleGrader Class takes in data from the file created by ScheduleGenerator, and creates a set of courses based on this data, and then determines whether the course load is hard, average, or easy.  
 * The ScheduleGrader requires the Course class.
 * <br><br>
 * @author Lance Wilson
 * @version Lab 2, 2/4/2016
 */
import java.io.*;
import java.util.Scanner;

public class ScheduleGrader
{
    public static void main(String[] args) throws FileNotFoundException
    {
        //Initialize the load variables.
        int load = 0, total_load = 0;

        // Create a scanner for the file.
        File courseFile = new File("Course_dat.txt");
        Scanner courseScanner = new Scanner(courseFile);

        // Loop runs while there are still new lines in the file.
        while (courseScanner.hasNext())
        {
            // Create a new default course for reassignment later.
            Course course = new Course();

            // Scan the next line.
            String line = courseScanner.nextLine();

            // Split the data on a space delimiter and store them in a tokens array.
            String[] tokens = line.split(" ");

            // Send the tokens to a new course.
            course = new Course(tokens[0], Integer.parseInt(tokens[1]), Double.parseDouble(tokens[2]));

            // Calculate the load difficulty
            load = course.load_calc();
            // Add the load difficulty to a running total.
            total_load += load;
        }

        // Close the file.
        courseScanner.close();

        // Determine the difficulty of the schedule.
        if (total_load < 0)
        {
            System.out.println("This is a Hard Schedule");
        }
        else if (total_load > 0)
        {
            System.out.println("This is an Easy Schedule");
        }
        else
        {
            System.out.println("This is an Average Schedule.");
        }

    }
}
