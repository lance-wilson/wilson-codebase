/**
 * The Driver
 * The ScheduleGrader requires the Course and Student classes.
 * <br><br>
 * @author Lance Wilson
 * @version Lab 3, 2/11/2016
 */
import java.util.Random;

public class Driver
{
    public static void main(String[] args)
    {
        int credit_hours = 0;
        double homework_hours = 0.0;

        // Student and course arrays.
        Course[] course_array = new Course[20];
        Student[] student_array = new Student[100];

        Random rand = new Random();

        for (int x = 0; x < course_array.length; x++)
        {
            // Value of homework hours that will never be valid.
            homework_hours = 30;
            // Randomly set credit hours 0 to 6.
            credit_hours = rand.nextInt(7);
            // Set homework hours to 0 if credit_hours is 0.
            if (credit_hours == 0)
            {
                homework_hours = 0.0;
            }
            // Otherwise, set homework_hours to a random number 0 to 24, less than 4 * credit_hours
            else
            {
                while (homework_hours > 4 * credit_hours)
                {
                    homework_hours = rand.nextDouble()*24;
                }
            }
            // Create a new course with the above specifications and a random string title.
            course_array[x] = new Course(randomWord(), credit_hours, homework_hours);
        }

        // Create a set of students, and for each student, attempt to add each course to their schedule.
        for (int y = 0; y < student_array.length; y++)
        {
            student_array[y] = new Student(randomWord());
            for (int z = 0; z < course_array.length; z++)
            {
                student_array[y].addCourse(course_array[z]);
            }
        }

        // Print the results.
        for (int n = 0; n < student_array.length; n++)
        {
            // Print the students name.
            System.out.println("Student Name: " + student_array[n].getName());

            // Determine the difficulty of the schedule and print out the difficulty rating.
            if (student_array[n].difficulty_calc() < 0)
            {
                System.out.println("\tDifficulty: This is a Hard Schedule");
            }
            else if (student_array[n].difficulty_calc() > 0)
            {
                System.out.println("\tDifficulty: This is an Easy Schedule");
            }
            else
            {
                System.out.println("\t Difficulty: This is an Average Schedule.");
            }

            // Print out the list of course names for the student, or unable to get any if they didn't get in to any.
            System.out.println("\tCourses:");
            if (student_array[n].getCourse().size() == 0)
            {
                System.out.println("\t\tUnable to get in to any courses.");
            }
            else
            {
                for (int m = 0; m < student_array[n].getCourse().size(); m++)
                {
                    System.out.println("\t\t" + student_array[n].getCourse().get(m).getName());
                }
            }
        }
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
