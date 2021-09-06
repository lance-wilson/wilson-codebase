/**
 * The Watercraft class stores data and methods needed by all instances of the Watercraft object.
 * A Watercraft has a name.
 * <br><br>
 * @author Lance Wilson
 * @version Lab 5
 */

public class Watercraft
{
    String name;

    /**
     * Parameter constructor takes in a name and sets the name via the setName method.
     * @param inName is the name of the Watercraft.
     */
    public Watercraft(String inName)
    {
        setName(inName);   
    }

    /**
     * setName sets the name of the Watercraft
     * @param inName is the name of the Watercraft.
     */
    public void setName(String inName)
    {
        name = inName;
    }

    /**
     * getName returns the name of the Watercraft
     * @return the Watercraft's name.
     */
    public String getName()
    {
        return name;
    }

}
