/**
 * The Course Class is used to store data for a course.  
 * A course has a name, an integer number of credit hours, and a number of homework hours.  
 * <br><br>
 * @author Lance Wilson
 * @version Lab 1, 1/28/2016
 */

public class Course
{
    private String name = "";
    private int credit_hours = -1;
    private double homework_hours = -1.0;

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

}
