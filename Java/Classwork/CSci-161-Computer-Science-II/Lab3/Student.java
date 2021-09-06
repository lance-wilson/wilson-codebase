/**
 * The Student Class is used to store data for a student.  
 * A student has a name, a course list, and a number of homework and credit hours.
 * <br><br>
 * @author Lance Wilson
 * @version Lab 3, 2/11/2016
 */
import java.util.*;

public class Student
{
    private String name = "";
    private int current_credit;
    private double current_homework;
    ArrayList <Course> courses = new ArrayList<>();

    /**
     * Default constructor sets the student name to a null string.
     */
    public Student()
    {
        setName("");
    }

    /**
     * Parameter constructor takes in a name and sets it to the student's name.
     */
    public Student(String inName)
    {
        setName(inName);
    }

    /**
     * setName sets the student's new name.
     * @param inName becomes the new name.
     */
    public void setName(String inName)
    {
        name = inName;
    }

    /**
     * getName allows access to the student's current name.
     * @return the current student name.
     */
    public String getName()
    {
        if (name.equals(""))
        {
            return "NOT NAMED YET";
        }
        else
        {
             return name;
        }
    }

    /**
     * getCourse allows access to the courses ArrayList
     * @return the courses ArrayList
     */
    public ArrayList<Course> getCourse()
    {
        return courses;
    }

    /**
     * Calculates the student's total credit hours.
     * @return the current number of credit hours.
     */
    public int totalCred()
    {
        int credit_temp = 0;
        // Calculates the total number of credit hours.
        for (int w = 0; w < courses.size(); w++)
        {
            credit_temp = courses.get(w).getCredit();
            current_credit += credit_temp;
        }

        return current_credit;
    }

    /**
     * Calculates the total homework hours of the student.
     * @return the total number of homework hours.
     */
    public double totalHomework()
    {
        double homework_temp = 0;
        // Calculates the total number of homework hours.
        for (int q = 0; q < courses.size(); q++)
        {
            homework_temp = courses.get(q).getCredit();
            current_homework += homework_temp;
        }

        return current_homework;
    }

    /**
     * Takes in a course and adds it to the Student's course load, but only if that will not put the student's credit's hours over 21, their homework hours over 64, or the number of available seats is 0.
     * @param course is the course to be added.
     * @return a boolean that indicates whether the course add was successful.
     */
    public boolean addCourse(Course course)
    {
        if (course.getCredit() + current_credit > 21 || course.getHomework() + current_homework > 64 || course.getSeats() == 0)
        {
            return false;
        }
        else
        {
            // Add course
            courses.add(course);
            // Reduce the number of seats.
            course.setSeats(course.getSeats()-1);
            return true;
        }
    }

    /**
     * Calculates the course load's difficulty index value.
     * @return the difficulty index.
     */
    public int difficulty_calc()
    {
        //Initialize the load variables.
        int load = 0, total_load = 0;

        // Loop runs while there are still courses left in the schedule.
        for (Course schedule : courses)
        {
            // Calculate the load difficulty
            load = schedule.load_calc();
            // Add the load difficulty to a running total.
            total_load += load;
        }

        return total_load;
    }
}
