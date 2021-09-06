/**
 * The Course Class is used to store data for a course.  
 * A course has a name, an integer number of credit hours, and a number of homework hours.  
 * <br><br>
 * @author Lance Wilson
 * @version Lab 3, 2/11/2016
 */
import java.util.Random;

public class Course
{
    private String name = "";
    private int credit_hours = -1;
    private double homework_hours = -1.0;
    private int open_seats = 0;
    Random rand = new Random();

    /** Default constructor creates a Course with default values and a random number of open seats.
     */
    public Course()
    {
        setName("");
        setCredit(-1);
        setHomework(-1.0);
        setSeats(rand.nextInt(21)+10);
    }

    /** Full parameter constructor takes in a name, number of credit hours, and homework hours and creates a course with those values. It also randomly sets the number of available seats.
     * @param inName is the course's name
     * @param inCredit is the course's credit hours
     * @param inHomework is the course's homework hours
     */
    public Course(String inName, int inCredit, double inHomework)
    {
        setName(inName);
        setCredit(inCredit);
        setHomework(inHomework);
        setSeats(rand.nextInt(21)+10);
    }

    /**
     * setName sets the course's new name.
     * @param inName becomes the new name.
     */
    public void setName(String inName)
    {
        name = inName;
    }

    /**
     * setCredit sets the course's credit hours to an inputted value (if the value is valid), or to -1 
     * (if it is not).
     * @param inCredit becomes the course's credit hour total.
     */
    public void setCredit(int inCredit)
    {
        if (inCredit > 0 && inCredit <= 6)
        {
            credit_hours = inCredit;
        }
        else
        {
            credit_hours = -1;
        }
    }

    /**
     * setHomework sets the course's homework hours to an inputted value (if the value is valid), or 
     * to -1.0 (if it is not).
     * @param inHomework becomes the course's homework hour total.
     */
    public void setHomework(double inHomework)
    {
        if (inHomework >= 0.0 && inHomework <= credit_hours*4.0)
        {
            homework_hours = inHomework;
        }
        else
        {
            homework_hours = -1.0;
        }
    }

    /**
     * setSeats sets the course's number of open seats in the course. 
     * @param inSeats becomes the course's number of open seats.
     */
    public void setSeats(int inSeats)
    {
        open_seats = inSeats;
    }

    /**
     * getName allows access to the course's current name.
     * @return the current course name.
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
     * getCredit allows access to the course's current number of credit hours.
     * @return the current number of course credit hours.
     */
    public int getCredit()
    {
        return credit_hours;
    }

    /**
     * getHomework allows access to the course's current number of homework hours.
     * @return the current number of course homework hours.
     */
    public double getHomework()
    {
        return homework_hours;
    }

    /**
     * getSeats allows access to the course's current number of available seats.
     * @return the current number of seats.
     */
    public int getSeats()
    {
        return open_seats;
    }

    /** load_calc calculates how difficult a course schedule is based on the number of credit and homework hours
     * @return load is the difficulty index of the course.
     */
    public int load_calc()
    {
        int load = 0;
        double loadSum = getCredit() + getHomework();

        if (loadSum > 4 * getCredit())
        {
            load = -2;
        }
        else if (loadSum <= 4*getCredit() && loadSum > 3*getCredit())
        {
            load = -1;
        }
        else if (loadSum <= 3*getCredit() && loadSum > 2*getCredit())
        {
            load = 0;
        }
        else if (loadSum <= 2*getCredit() && loadSum > getCredit())
        {
            load = 1;
        }
        else if (loadSum <= getCredit())
        {
            load = 2;
        }

        return load;
    }

}
